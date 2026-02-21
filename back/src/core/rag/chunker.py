"""Structured section-based chunker for ProcedureDoc documents."""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Token estimation factor: rough word-to-token ratio for Spanish text
_TOKEN_FACTOR = 1.3

# Chunk size boundaries (in estimated tokens)
_MIN_TOKENS = 200
_MAX_TOKENS = 600
_OVERLAP_TOKENS = 50

# Sections to chunk, in order
_SECTIONS = [
    "descripcion",
    "requisitos",
    "documentos_necesarios",
    "plazos",
    "como_solicitar",
    "donde_solicitar",
    "base_legal",
]


@dataclass
class ChunkData:
    content: str
    section_name: str
    heading_path: str
    token_count: int
    chunk_index: int
    metadata: dict = field(default_factory=dict)


def _estimate_tokens(text: str) -> int:
    """Estimate token count from text using word-based heuristic."""
    return int(len(text.split()) * _TOKEN_FACTOR)


def _format_list(items: list, label: str | None = None) -> str:
    """Convert a list of strings to numbered bullets."""
    lines = []
    if label:
        lines.append(f"{label}:")
    for i, item in enumerate(items, 1):
        lines.append(f"  {i}. {item}")
    return "\n".join(lines)


def _format_dict(data: dict, label: str | None = None) -> str:
    """Convert a dict to 'key: value' lines."""
    lines = []
    if label:
        lines.append(f"{label}:")
    for key, value in data.items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def _format_como_solicitar_array(items: list) -> str:
    """Format como_solicitar when it's an array of via/detalle objects."""
    blocks = []
    for item in items:
        parts = [f"Via: {item.get('via', '')}"]
        if item.get("detalle"):
            parts.append(f"Detalle: {item['detalle']}")
        if item.get("requisito"):
            parts.append(f"Requisito: {item['requisito']}")
        blocks.append("\n".join(parts))
    return "\n\n".join(blocks)


def _section_to_text(section_name: str, value) -> str:
    """Convert a section value to readable text."""
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if section_name == "requisitos":
        if isinstance(value, list):
            return _format_list(value, "Requisitos")
        return str(value)

    if section_name in ("documentos_necesarios", "base_legal"):
        if isinstance(value, list):
            label = "Documentos necesarios" if section_name == "documentos_necesarios" else "Base legal"
            return _format_list(value, label)
        return str(value)

    if section_name == "plazos":
        if isinstance(value, dict):
            return _format_dict(value, "Plazos")
        return str(value)

    if section_name == "como_solicitar":
        if isinstance(value, list):
            return _format_como_solicitar_array(value)
        if isinstance(value, dict):
            return _format_dict(value, "Como solicitar")
        return str(value)

    if section_name == "donde_solicitar":
        if isinstance(value, dict):
            parts = []
            if value.get("urls"):
                parts.append(_format_list(value["urls"], "URLs"))
            if value.get("direcciones"):
                parts.append(_format_list(value["direcciones"], "Direcciones"))
            if value.get("cita_previa_url"):
                parts.append(f"Cita previa: {value['cita_previa_url']}")
            return "\n\n".join(parts) if parts else ""
        return str(value)

    # Fallback for unknown types
    if isinstance(value, list):
        return _format_list(value)
    if isinstance(value, dict):
        return _format_dict(value)
    return str(value)


def _build_metadata(doc: dict, section_name: str) -> dict:
    """Extract metadata for a chunk from the source document."""
    meta = {
        "procedure_id": doc.get("id", doc.get("tramite", "")),
        "section_name": section_name,
        "source_type": doc.get("source_type", ""),
        "idioma": doc.get("idioma", "es"),
    }
    territorio = doc.get("territorio")
    if isinstance(territorio, dict):
        meta["territorio_nivel"] = territorio.get("nivel", "")
        if territorio.get("ccaa"):
            meta["territorio_ccaa"] = territorio["ccaa"]
        if territorio.get("municipio"):
            meta["territorio_municipio"] = territorio["municipio"]
    return meta


def _split_text_with_overlap(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    """Split text into chunks of ~max_tokens with overlap_tokens overlap."""
    words = text.split()
    if not words:
        return []

    max_words = int(max_tokens / _TOKEN_FACTOR)
    overlap_words = int(overlap_tokens / _TOKEN_FACTOR)
    step = max(max_words - overlap_words, 1)

    chunks = []
    start = 0
    while start < len(words):
        end = start + max_words
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        if end >= len(words):
            break
        start += step

    return chunks


def chunk_procedure(doc: dict) -> list[ChunkData]:
    """Split a ProcedureDoc dict into structured chunks.

    Args:
        doc: A dictionary conforming to ProcedureDoc v1 schema
             (or a tramite JSON with compatible fields).

    Returns:
        List of ChunkData objects ready for embedding and storage.
    """
    doc_name = doc.get("nombre", "")
    procedure_id = doc.get("id", doc.get("tramite", "unknown"))

    # Build raw sections as (section_name, text) pairs
    raw_sections: list[tuple[str, str]] = []
    for section_name in _SECTIONS:
        # Handle alternate field names from legacy tramite format
        key = section_name
        if key == "documentos_necesarios" and key not in doc and "documentos" in doc:
            key = "documentos"

        value = doc.get(key)
        if value is None:
            continue

        text = _section_to_text(section_name, value)
        if not text.strip():
            continue

        raw_sections.append((section_name, text))

    if not raw_sections:
        logger.warning("No chunkable sections found for procedure %s", procedure_id)
        return []

    # Merge small sections with the next one
    merged: list[tuple[str, str]] = []
    i = 0
    while i < len(raw_sections):
        sec_name, sec_text = raw_sections[i]
        tokens = _estimate_tokens(sec_text)

        # Merge with next section if under minimum and not the last
        if tokens < _MIN_TOKENS and i + 1 < len(raw_sections):
            next_name, next_text = raw_sections[i + 1]
            combined_name = f"{sec_name}+{next_name}"
            combined_text = f"{sec_text}\n\n{next_text}"
            merged.append((combined_name, combined_text))
            i += 2
        else:
            merged.append((sec_name, sec_text))
            i += 1

    # Generate final chunks: split large sections, keep small ones as-is
    chunks: list[ChunkData] = []
    chunk_index = 0

    for section_name, text in merged:
        heading_path = f"{doc_name} > {section_name}"
        tokens = _estimate_tokens(text)
        metadata = _build_metadata(doc, section_name)

        if tokens > _MAX_TOKENS:
            sub_texts = _split_text_with_overlap(text, _MAX_TOKENS, _OVERLAP_TOKENS)
            for sub_text in sub_texts:
                sub_tokens = _estimate_tokens(sub_text)
                chunks.append(ChunkData(
                    content=sub_text,
                    section_name=section_name,
                    heading_path=heading_path,
                    token_count=sub_tokens,
                    chunk_index=chunk_index,
                    metadata=metadata,
                ))
                chunk_index += 1
        else:
            chunks.append(ChunkData(
                content=text,
                section_name=section_name,
                heading_path=heading_path,
                token_count=tokens,
                chunk_index=chunk_index,
                metadata=metadata,
            ))
            chunk_index += 1

    logger.info(
        "Chunked procedure %s into %d chunks (sections: %d)",
        procedure_id, len(chunks), len(merged),
    )
    return chunks
