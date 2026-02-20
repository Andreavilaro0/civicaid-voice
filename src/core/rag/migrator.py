"""Migrate data/tramites/*.json files to PG as ProcedureDoc v1 records."""

import hashlib
import json
import logging
import os
import re
import unicodedata
from datetime import datetime, timezone

from src.core.rag.chunker import chunk_procedure
from src.core.rag.embedder import embed_batch
from src.core.rag.store import PGVectorStore

logger = logging.getLogger(__name__)

_TRAMITES_DIR = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, "data", "tramites"
)

# All 8 tramites expected in data/tramites/
_TRAMITE_NAMES = [
    "imv",
    "empadronamiento",
    "tarjeta_sanitaria",
    "nie_tie",
    "prestacion_desempleo",
    "ayuda_alquiler",
    "certificado_discapacidad",
    "justicia_gratuita",
]

# Known organismo -> abbreviation mappings
_ORG_ABBREV = {
    "seguridad social": "SEGSOCIAL",
    "sepe (servicio público de empleo estatal)": "SEPE",
    "ayuntamiento (madrid)": "AYTOMAD",
    "comunidad de madrid": "COMMAD",
    "oficina de extranjería / dirección general de la policía": "EXTRANJERIA",
    "dirección general de la policía": "DGP",
    "ministerio de vivienda y agenda urbana": "MIVAU",
    "imserso": "IMSERSO",
    "comunidades autónomas / imserso": "IMSERSO",
    "comisión de asistencia jurídica gratuita": "CAJG",
}

# ProcedureDoc v1 required fields (for completeness_score)
_REQUIRED_FIELDS = [
    "id",
    "nombre",
    "source_url",
    "source_type",
    "organismo",
    "descripcion",
    "keywords",
    "idioma",
    "extracted_at",
    "content_hash",
    "word_count",
    "completeness_score",
]


def _slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    # Normalize unicode and strip accents
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    # Collapse multiple dashes
    text = re.sub(r"-+", "-", text)
    return text


def _get_org_abbrev(organismo: str) -> str:
    """Get uppercase abbreviation for an organismo."""
    key = organismo.lower().strip()
    if key in _ORG_ABBREV:
        return _ORG_ABBREV[key]
    # Fallback: take uppercase initials
    words = re.findall(r"[A-Za-zÁÉÍÓÚáéíóú]+", organismo)
    return "".join(w[0].upper() for w in words[:4]) if words else "UNK"


def _generate_id(organismo: str, nombre: str) -> str:
    """Generate a slug id like 'age-segsocial-ingreso-minimo-vital'."""
    org_slug = _slugify(_get_org_abbrev(organismo))
    nombre_slug = _slugify(nombre)
    raw = f"age-{org_slug}-{nombre_slug}"
    # Ensure it matches the schema pattern ^[a-z][a-z0-9_-]{2,80}$
    if len(raw) > 81:
        raw = raw[:81]
    return raw


def _count_words(data: dict) -> int:
    """Count words across all text fields in the tramite data."""
    count = 0
    for value in data.values():
        if isinstance(value, str):
            count += len(value.split())
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    count += len(item.split())
                elif isinstance(item, dict):
                    for v in item.values():
                        if isinstance(v, str):
                            count += len(v.split())
        elif isinstance(value, dict):
            for v in value.values():
                if isinstance(v, str):
                    count += len(v.split())
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            count += len(item.split())
    return max(count, 1)


def _content_hash(data: dict) -> str:
    """SHA-256 of json.dumps(data, sort_keys=True)."""
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _map_to_procedure_doc(data: dict) -> dict:
    """Map a tramite JSON dict to ProcedureDoc v1 format."""
    organismo = data.get("organismo", "")
    nombre = data.get("nombre", "")
    now = datetime.now(timezone.utc)

    doc = {
        "id": _generate_id(organismo, nombre),
        "nombre": nombre,
        "descripcion": data.get("descripcion", ""),
        "organismo": organismo,
        "organismo_abrev": _get_org_abbrev(organismo),
        "source_url": data.get("fuente_url", ""),
        "source_type": "age",
        "idioma": "es",
        "keywords": data.get("keywords", []),
        "content_hash": _content_hash(data),
        "word_count": _count_words(data),
        "extracted_at": now,
    }

    # Direct copy fields
    if "requisitos" in data:
        doc["requisitos"] = data["requisitos"]

    # documentos -> documentos_necesarios (field rename)
    if "documentos" in data:
        value = data["documentos"]
        if isinstance(value, dict):
            # Flatten dict of lists into a single list
            flat = []
            for items in value.values():
                if isinstance(items, list):
                    flat.extend(items)
                elif isinstance(items, str):
                    flat.append(items)
            doc["documentos_necesarios"] = flat
        elif isinstance(value, list):
            doc["documentos_necesarios"] = value

    if "como_solicitar" in data:
        doc["como_solicitar"] = data["como_solicitar"]

    if "plazos" in data:
        doc["plazos"] = data["plazos"]

    # Verified info
    if data.get("verificado") and data.get("fecha_verificacion"):
        try:
            dt = datetime.strptime(data["fecha_verificacion"], "%Y-%m-%d")
            doc["verified_at"] = dt.replace(tzinfo=timezone.utc)
            doc["verified_by"] = "manual"
        except ValueError:
            pass

    # Completeness score: count filled required fields / total required
    filled = sum(1 for f in _REQUIRED_FIELDS if doc.get(f))
    doc["completeness_score"] = round(filled / len(_REQUIRED_FIELDS), 2)

    return doc


def migrate_tramite(json_path: str, store: PGVectorStore = None) -> dict:
    """Migrate one tramite JSON to PG. Returns stats dict."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tramite_name = os.path.splitext(os.path.basename(json_path))[0]
    logger.info("Migrating tramite: %s", tramite_name)

    # 1. Map to ProcedureDoc v1
    doc_data = _map_to_procedure_doc(data)

    # 2. Chunk
    chunks = chunk_procedure(doc_data)
    logger.info("  %s: %d chunks generated", tramite_name, len(chunks))

    # 3. Embed
    texts = [c.content for c in chunks]
    embeddings = embed_batch(texts)
    for chunk, embedding in zip(chunks, embeddings):
        chunk.metadata["embedding"] = embedding
    logger.info("  %s: %d embeddings generated", tramite_name, len(embeddings))

    # 4. Insert into PG
    if store is None:
        store = PGVectorStore()

    stats = store.insert_procedure(doc_data, chunks)
    stats["tramite"] = tramite_name
    stats["word_count"] = doc_data["word_count"]
    logger.info(
        "  %s: inserted (replaced=%s, chunks=%d)",
        tramite_name, stats["replaced"], stats["chunks_inserted"],
    )

    return stats


def migrate_all(store: PGVectorStore = None) -> dict:
    """Migrate all 8 tramites. Returns total stats."""
    if store is None:
        store = PGVectorStore()

    tramites_dir = os.path.normpath(_TRAMITES_DIR)
    results = []
    errors = []

    for name in _TRAMITE_NAMES:
        json_path = os.path.join(tramites_dir, f"{name}.json")
        if not os.path.exists(json_path):
            logger.warning("Tramite file not found: %s", json_path)
            errors.append({"tramite": name, "error": "file not found"})
            continue

        try:
            stats = migrate_tramite(json_path, store=store)
            results.append(stats)
        except Exception as exc:
            logger.error("Failed to migrate %s: %s", name, exc)
            errors.append({"tramite": name, "error": str(exc)})

    total_chunks = sum(r["chunks_inserted"] for r in results)
    total_words = sum(r.get("word_count", 0) for r in results)

    summary = {
        "migrated": len(results),
        "failed": len(errors),
        "total_chunks": total_chunks,
        "total_words": total_words,
        "results": results,
        "errors": errors,
    }

    logger.info(
        "Migration complete: %d migrated, %d failed, %d total chunks",
        summary["migrated"], summary["failed"], summary["total_chunks"],
    )

    return summary
