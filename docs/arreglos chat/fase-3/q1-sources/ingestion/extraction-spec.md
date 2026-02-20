# Extraction Specification

> **Scope:** Detailed rules for extracting structured text from each document type in Clara's ingestion pipeline.
> **Status:** Research / Design (no code changes)
> **Date:** 2026-02-18
> **Related:** `ingestion-playbook.md`, `normalization-schema.md`

---

## Overview

The extraction stage takes raw fetched content (HTML, PDF, XML) and produces clean, structured text suitable for normalization into the ProcedureDoc schema. Each document type requires a different extraction strategy and toolchain.

### Common Intermediate Output Format

All extractors produce the same intermediate JSON:

```json
{
  "source_url": "https://...",
  "document_type": "html|pdf|boe_xml|form_html|form_pdf|docx",
  "title": "Extracted page/document title",
  "extracted_text": "Full extracted text as clean markdown",
  "headings": ["h1 text", "h2 text"],
  "tables": [{"caption": "...", "markdown": "| ... |"}],
  "links": [{"text": "...", "url": "..."}],
  "form_fields": [],
  "metadata": {
    "word_count": 1234,
    "language_detected": "es",
    "language_confidence": 0.97,
    "has_text_layer": true,
    "page_count": null,
    "extraction_tool": "trafilatura",
    "extraction_duration_ms": 450,
    "encoding_issues": false
  }
}
```

---

## 1. HTML Pages

### Context

Most Spanish government procedure information lives on HTML web pages -- sede electronica portals, administracion.gob.es, CCAA portals, and municipal websites. These pages have heavy navigation, sidebars, cookie banners, and legal footers wrapping a relatively small main content area.

### Primary Tool: trafilatura

```python
import trafilatura

result = trafilatura.extract(
    html_content,
    include_links=True,
    include_tables=True,
    include_comments=False,
    include_images=False,
    output_format="markdown",
    favor_recall=True,
    deduplicate=True,
)
```

**Why trafilatura:** Purpose-built for main content extraction. Handles boilerplate removal (nav, footer, sidebar, cookie banners) automatically. Outputs clean markdown preserving headings and lists. Actively maintained with good Spanish content handling.

### Fallback: readability-lxml

If trafilatura returns None or fewer than 50 words:

```python
from readability import Document
from bs4 import BeautifulSoup

doc = Document(html_content)
main_html = doc.summary()
soup = BeautifulSoup(main_html, "lxml")
text = soup.get_text(separator="\n")
```

### Fallback for Forms: BeautifulSoup

When the page contains `<form>` elements, use BeautifulSoup to extract form structure (see Section 4 below).

### Elements to Strip

- `<nav>`, `<header>`, `<footer>`, `<aside>` -- structural boilerplate
- `<script>`, `<style>` -- JS/CSS
- `.cookie-banner`, `#cookie-consent` -- cookie notices
- `.breadcrumb` -- breadcrumb navigation
- `.share-buttons`, `.social-links` -- social sharing widgets
- `[role="navigation"]`, `[role="banner"]`, `[role="contentinfo"]` -- ARIA landmarks

### Elements to Preserve

- `<h1>` through `<h6>` -- heading hierarchy (crucial for section detection)
- `<ul>`, `<ol>`, `<li>` -- lists (requisitos, documentos are typically lists)
- `<table>` -- tables (cuantias, plazos are often in tables)
- `<a href>` -- hyperlinks (links to forms, sedes, related procedures)
- `<strong>`, `<em>` -- emphasis markers
- `<dl>`, `<dt>`, `<dd>` -- definition lists (used in some procedure pages)

### Spanish Government Site Patterns

**administracion.gob.es:**
```html
<div class="contenido_pagina">
  <h1>Nombre del Tramite</h1>
  <div class="apartado">
    <h2>Que es y para que sirve</h2>
    <p>...</p>
  </div>
</div>
```

**SEPE (sede.sepe.gob.es):**
```html
<div id="contenido">
  <div class="cuerpoContenido">
    <h1>...</h1>
    <div class="bloqueContenido">...</div>
  </div>
</div>
```

**Madrid (madrid.es):**
```html
<div class="noticia-contenido">
  <h1>...</h1>
  <div class="apartado-titulo"><h2>...</h2></div>
  <div class="apartado-contenido"><p>...</p></div>
</div>
```

**Seguridad Social (sede.seg-social.gob.es):**
```html
<div class="wpsPortletBody">
  <div class="lotusWidget">
    <h1>...</h1>
    <div class="lotusBody">...</div>
  </div>
</div>
```

For high-priority domains where trafilatura misses content, custom BeautifulSoup selectors targeting these patterns serve as domain-specific fallbacks.

---

## 2. PDF Documents

### Context

Government procedures often link to PDFs: form instructions, regulatory texts, resolution templates, informational guides. Most procedure-related PDFs on government sites have embedded text layers.

### Text Layer Detection

Before choosing extraction strategy, detect whether the PDF has a text layer:

```python
import fitz  # pymupdf

doc = fitz.open(pdf_path)
has_text = False
for page in doc:
    text = page.get_text().strip()
    if len(text) > 20:
        has_text = True
        break
doc.close()
```

If `has_text` is False: flag the document as `requires_ocr` and defer to Q2. Store the raw PDF and metadata but skip text extraction.

### Primary Tool: pdfplumber (text + tables)

```python
import pdfplumber

with pdfplumber.open(pdf_path) as pdf:
    full_text = []
    tables = []

    for i, page in enumerate(pdf.pages):
        text = page.extract_text(x_tolerance=3, y_tolerance=3)
        if text:
            full_text.append(text)

        page_tables = page.extract_tables()
        for table in page_tables:
            tables.append({"page": i + 1, "rows": table})
```

**Why pdfplumber:** Excellent table extraction (cuantias, baremos, plazos often in tables). Handles multi-column layouts. Good support for Spanish characters.

### Fallback Tool: pymupdf (fitz)

Faster for simple text extraction when pdfplumber struggles:

```python
import fitz

doc = fitz.open(pdf_path)
full_text = []
for page in doc:
    blocks = page.get_text("blocks")
    blocks.sort(key=lambda b: (b[1], b[0]))  # top-to-bottom, left-to-right
    for block in blocks:
        if block[6] == 0:  # text block, not image
            full_text.append(block[4])
doc.close()
```

### OCR Detection (Flag for Q2)

Scanned PDFs without text layers are logged but not processed in Q1:

```python
def assess_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_pages = 0
    image_pages = 0
    for page in doc:
        if len(page.get_text().strip()) > 20:
            text_pages += 1
        elif len(page.get_images()) > 0:
            image_pages += 1
    doc.close()
    return {
        "has_text_layer": text_pages > 0,
        "requires_ocr": image_pages > 0 and text_pages == 0,
        "mixed": text_pages > 0 and image_pages > 0,
        "text_pages": text_pages,
        "image_pages": image_pages,
        "total_pages": text_pages + image_pages,
    }
```

### Common PDF Challenges

| Challenge | Solution |
|-----------|----------|
| Multi-column layouts | pdfplumber: extract by spatial position, sort blocks per column |
| Headers/footers | Detect repeated text in same position across pages, remove |
| Page numbers | Regex removal of isolated numbers at page boundaries |
| Hyphenation at line breaks | Rejoin: `"requi-\nsitos"` -> `"requisitos"` |
| Spanish characters (n, accents) | Ensure UTF-8; verify with spot-check regex |
| Ligatures (fi, fl, ff) | Map to individual characters |
| Scanned pages mixed with text | Process text pages normally, flag scanned for OCR (Q2) |

---

## 3. BOE XML

### Context

The Boletin Oficial del Estado publishes legislation in structured XML via `https://boe.es/datosabiertos/`. BOE documents define the legal basis for procedures (`base_legal` field in ProcedureDoc).

### BOE XML Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<documento>
  <metadatos>
    <identificador>BOE-A-2024-12345</identificador>
    <titulo>Real Decreto 100/2024, de 15 de enero, por el que...</titulo>
    <diario>BOE</diario>
    <seccion>I. Disposiciones generales</seccion>
    <departamento>Ministerio de Trabajo y Economia Social</departamento>
    <rango>Real Decreto</rango>
    <fecha_publicacion>20240120</fecha_publicacion>
    <url_pdf>https://www.boe.es/boe/dias/2024/01/20/pdfs/BOE-A-2024-12345.pdf</url_pdf>
    <url_html>https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-12345</url_html>
  </metadatos>
  <analisis>
    <notas>
      <nota>Modifica el Real Decreto 200/2020...</nota>
    </notas>
    <materias>
      <materia>Prestaciones por desempleo</materia>
    </materias>
    <referencias>
      <anterior referencia="BOE-A-2020-5678">Real Decreto 200/2020</anterior>
    </referencias>
  </analisis>
  <texto>
    <p>Articulo 1. Objeto.</p>
    <p>El presente real decreto tiene por objeto...</p>
  </texto>
</documento>
```

### Custom Parser

```python
import xml.etree.ElementTree as ET

def extract_boe_xml(xml_content: str) -> dict:
    root = ET.fromstring(xml_content)
    meta = root.find("metadatos")

    boe_id = meta.findtext("identificador", "")
    titulo = meta.findtext("titulo", "")
    seccion = meta.findtext("seccion", "")
    departamento = meta.findtext("departamento", "")
    rango = meta.findtext("rango", "")
    fecha = meta.findtext("fecha_publicacion", "")

    referencias = []
    for ref in root.findall(".//referencias/anterior"):
        referencias.append({
            "boe_id": ref.get("referencia", ""),
            "text": ref.text or "",
        })

    materias = [m.text for m in root.findall(".//materias/materia") if m.text]

    texto_elem = root.find("texto")
    paragraphs = []
    if texto_elem is not None:
        for p in texto_elem.findall(".//p"):
            if p.text:
                paragraphs.append(p.text)
    full_text = "\n\n".join(paragraphs)

    return {
        "boe_id": boe_id,
        "titulo": titulo,
        "seccion": seccion,
        "departamento": departamento,
        "rango": rango,
        "fecha_publicacion": fecha,
        "materias": materias,
        "referencias": referencias,
        "texto": full_text,
    }
```

### BOE Open Data API Endpoints

- `/buscar/documento/{id}` -- Single document by BOE ID
- `/buscar/diario/{date}` -- All documents from a given date
- `/sumario/{date}` -- Summary of daily publication

---

## 4. HTML Forms

### Context

Many procedures require filling out forms on sede electronica pages. Extracting form structure helps Clara describe what information the user needs to prepare.

### Extraction with BeautifulSoup

```python
from bs4 import BeautifulSoup

def extract_html_forms(html_content: str) -> list[dict]:
    soup = BeautifulSoup(html_content, "lxml")
    forms = []

    for form in soup.find_all("form"):
        form_data = {
            "action": form.get("action", ""),
            "method": form.get("method", "GET"),
            "fields": [],
        }

        for field in form.find_all(["input", "select", "textarea"]):
            field_info = {
                "type": field.get("type", field.name),
                "name": field.get("name", ""),
                "id": field.get("id", ""),
                "required": field.has_attr("required"),
                "placeholder": field.get("placeholder", ""),
            }

            # Find associated label
            field_id = field.get("id")
            if field_id:
                label = soup.find("label", attrs={"for": field_id})
                if label:
                    field_info["label"] = label.get_text(strip=True)

            # Extract options for select elements
            if field.name == "select":
                options = [
                    opt.get_text(strip=True)
                    for opt in field.find_all("option")
                ]
                field_info["options"] = options

            form_data["fields"].append(field_info)

        # Extract instructions near the form
        instructions = []
        for marker in ["required", "obligatorio", "*"]:
            legend = form.find("legend")
            if legend:
                instructions.append(legend.get_text(strip=True))
        form_data["instructions"] = instructions

        forms.append(form_data)

    return forms
```

### Field Name Extraction and Required Markers

The extractor identifies required fields via:
- HTML `required` attribute
- Asterisk `*` next to label text
- Text containing "obligatorio" near the field
- CSS class `required` or `campo-obligatorio`

### Output Example

```json
{
  "form_action": "/solicitud/prestacion-desempleo",
  "fields": [
    {
      "label": "Numero de identificacion (DNI/NIE)",
      "type": "text",
      "name": "nif",
      "required": true
    },
    {
      "label": "Causa del cese",
      "type": "select",
      "name": "causa_cese",
      "required": true,
      "options": ["Despido", "Fin de contrato", "ERE", "Otros"]
    }
  ]
}
```

---

## 5. Section Boundary Detection for Spanish Government Pages

Spanish government procedure pages use predictable section patterns. The normalizer detects these headings (case-insensitive, accent-insensitive matching):

| Target ProcedureDoc field | Heading patterns to match |
|---------------------------|--------------------------|
| `descripcion` | "Que es", "Descripcion", "Informacion general", "Objeto", "En que consiste" |
| `requisitos` | "Requisitos", "Quien puede solicitar", "Condiciones", "Beneficiarios" |
| `documentos_necesarios` | "Documentacion", "Documentos necesarios", "Que necesitas", "Documentacion requerida" |
| `plazos` | "Plazos", "Cuando solicitar", "Fechas", "Plazo de presentacion" |
| `tasas` | "Tasas", "Precio", "Coste", "Cuanto cuesta", "Importe" |
| `base_legal` | "Normativa", "Base legal", "Legislacion aplicable", "Marco legal" |
| `como_solicitar` | "Como solicitar", "Tramitacion", "Pasos", "Como hacerlo", "Procedimiento" |
| `donde_solicitar` | "Donde solicitar", "Oficinas", "Puntos de atencion", "Donde dirigirse" |

### Detection Algorithm

```python
import re
import unicodedata

SECTION_PATTERNS = {
    "descripcion": [
        r"qu[eé]\s+es", r"descripci[oó]n", r"informaci[oó]n\s+general",
        r"objeto", r"en\s+qu[eé]\s+consiste",
    ],
    "requisitos": [
        r"requisitos", r"qui[eé]n\s+puede", r"condiciones",
        r"beneficiarios",
    ],
    "documentos_necesarios": [
        r"documentaci[oó]n", r"documentos?\s+necesarios?",
        r"qu[eé]\s+necesitas", r"documentaci[oó]n\s+requerida",
    ],
    "plazos": [
        r"plazos?", r"cu[aá]ndo\s+solicitar", r"fechas",
        r"plazo\s+de\s+presentaci[oó]n",
    ],
    "tasas": [
        r"tasas?", r"precio", r"coste", r"cu[aá]nto\s+cuesta",
        r"importe",
    ],
    "base_legal": [
        r"normativa", r"base\s+legal", r"legislaci[oó]n\s+aplicable",
        r"marco\s+legal",
    ],
    "como_solicitar": [
        r"c[oó]mo\s+solicitar", r"tramitaci[oó]n", r"pasos",
        r"c[oó]mo\s+hacerlo", r"procedimiento",
    ],
    "donde_solicitar": [
        r"d[oó]nde\s+solicitar", r"oficinas",
        r"puntos?\s+de\s+atenci[oó]n", r"d[oó]nde\s+dirigirse",
    ],
}

def normalize_text(text: str) -> str:
    """Remove accents and lowercase for matching."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()

def classify_heading(heading: str) -> str | None:
    """Match a heading to a ProcedureDoc field name."""
    normalized = normalize_text(heading)
    for field, patterns in SECTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, normalized):
                return field
    return None
```

---

## 6. Table Extraction Strategy

Government procedure pages frequently present data in tables (cuantias, baremos, plazos). Tables must be converted to markdown for storage or to structured data for specific fields.

### Conversion to Markdown

```python
def table_to_markdown(rows: list[list[str]]) -> str:
    if not rows or not rows[0]:
        return ""
    header = "| " + " | ".join(str(cell or "") for cell in rows[0]) + " |"
    separator = "| " + " | ".join("---" for _ in rows[0]) + " |"
    data = []
    for row in rows[1:]:
        data.append("| " + " | ".join(str(cell or "") for cell in row) + " |")
    return "\n".join([header, separator] + data)
```

### When to Use Structured Data Instead

If a table appears under a recognized section heading (e.g., "Cuantias", "Plazos"), convert it to a key-value dict rather than markdown, so it maps directly to ProcedureDoc fields.

---

## 7. Image Handling

- **Skip images:** Do not download or store image binary data.
- **Extract alt text:** Capture `alt` attributes from `<img>` tags -- alt text sometimes contains useful descriptions.
- **Log image presence:** Record whether the page contained images, in case manual review is needed.

```python
def extract_image_alt_texts(soup) -> list[str]:
    return [
        img.get("alt", "").strip()
        for img in soup.find_all("img")
        if img.get("alt", "").strip()
    ]
```

---

## 8. Quality Scoring

After extraction, each document receives a quality score to determine whether it is usable or needs manual review.

### Scoring Criteria

| Criterion | Weight | Pass condition | Fail action |
|-----------|--------|----------------|-------------|
| Word count | 0.30 | >= 50 words | Skip document; likely extraction failure |
| Section completeness | 0.25 | >= 2 recognized section headings detected | Flag for review |
| Language detection confidence | 0.20 | langdetect confidence >= 0.80 for `es` | Flag for review |
| Clean encoding | 0.15 | Zero mojibake patterns detected | Attempt fix with ftfy, then re-score |
| Structural integrity | 0.10 | At least 1 heading (`#`) in output | Flag for review |

### Quality Score Calculation

```python
from langdetect import detect_langs

def calculate_quality_score(extracted: dict) -> float:
    score = 0.0
    text = extracted["extracted_text"]

    # Word count (weight 0.30)
    wc = len(text.split())
    if wc >= 50:
        score += 0.30

    # Section completeness (weight 0.25)
    headings = extracted.get("headings", [])
    recognized = sum(1 for h in headings if classify_heading(h) is not None)
    if recognized >= 2:
        score += 0.25

    # Language confidence (weight 0.20)
    try:
        langs = detect_langs(text)
        es_conf = next((l.prob for l in langs if l.lang == "es"), 0.0)
        if es_conf >= 0.80:
            score += 0.20
    except Exception:
        pass

    # Clean encoding (weight 0.15)
    mojibake_patterns = ["Ã±", "Ã¡", "Ã©", "Ã³", "Ãº", "Ã"]
    has_mojibake = any(p in text for p in mojibake_patterns)
    if not has_mojibake:
        score += 0.15

    # Structural integrity (weight 0.10)
    if any(line.startswith("#") for line in text.split("\n")):
        score += 0.10

    return round(score, 2)
```

### Thresholds

| Score | Verdict |
|-------|---------|
| >= 0.70 | Accept. Proceed to normalization. |
| 0.40 - 0.69 | Partial. Store with `quality_flag: "review"`. |
| < 0.40 | Reject. Log extraction failure. Queue for manual review. |

---

## 9. Error Handling

### Partial Extraction

If only part of a page extracts successfully (e.g., top half of an HTML page, first 5 of 12 PDF pages):
- Store what was extracted.
- Set `metadata.partial = true`.
- Log the failure boundary (page number or byte offset).
- Queue for manual review.

### Encoding Issues

1. Attempt UTF-8 decode.
2. If fails, try `latin-1` (common on older Spanish government servers).
3. If mojibake detected in UTF-8 output, run through `ftfy.fix_text()`.
4. Log encoding resolution for audit.

### JavaScript-Rendered Content

Some sede electronica pages render content via JavaScript (React, Angular, or legacy JSP/AJAX). Trafilatura and readability cannot extract this content.

Detection: if trafilatura returns fewer than 50 words but the raw HTML contains `<script>` tags with substantial code, flag as `requires_js_rendering`.

Resolution (Q2): use a headless browser (Playwright/Selenium) to render the page before extraction. For Q1, these pages are flagged and skipped.

---

## 10. Output Format

Every extractor produces two artifacts:

### 1. Markdown Text

Clean markdown preserving document structure:

```markdown
# Prestacion por Desempleo (Paro)

Prestacion economica para personas que han perdido su empleo...

## Requisitos

- Estar afiliado y en situacion de alta...
- Encontrarse en situacion legal de desempleo...

## Documentacion necesaria

- DNI o NIE en vigor
- Certificado de empresa

## Como solicitar

### Online
Sede electronica del SEPE: sede.sepe.gob.es
Requisito: Certificado digital, cl@ve permanente
```

### 2. Metadata JSON

```json
{
  "source_url": "https://www.sepe.es/HomeSepe/Personas/...",
  "document_type": "html",
  "extraction_tool": "trafilatura",
  "extraction_duration_ms": 312,
  "word_count": 1250,
  "language_detected": "es",
  "language_confidence": 0.98,
  "quality_score": 0.85,
  "headings_found": 6,
  "sections_recognized": 4,
  "tables_extracted": 1,
  "forms_found": 0,
  "encoding_issues": false,
  "partial": false,
  "requires_ocr": false,
  "requires_js_rendering": false
}
```

---

## Extraction Pipeline Flow

```
Raw Document (HTML/PDF/XML/DOCX)
       |
       v
  Detect Type (Content-Type, extension, magic bytes)
       |
       +--> HTML ------> trafilatura ---------> Clean Markdown
       |                     |
       |               (if < 50 words)
       |                     v
       |              readability-lxml -------> Clean Markdown
       |                     |
       |              (forms detected?)
       |                     v
       |              BeautifulSoup ----------> Field List
       |
       +--> PDF -------> text layer? ---------> pdfplumber --> Text + Tables
       |                     |
       |               (no text layer)
       |                     v
       |              Flag: requires_ocr (defer Q2)
       |
       +--> BOE XML ---> custom parser -------> Structured Fields
       |
       +--> DOCX ------> python-docx ----------> Clean Markdown
       |
       v
  Quality Scoring (word count, sections, language, encoding)
       |
       +--> PASS (>= 0.70) --> Intermediate JSON --> Normalization
       |
       +--> PARTIAL (0.40-0.69) --> Store + Flag for Review
       |
       +--> FAIL (< 0.40) --> Log + Manual Review Queue
```
