# Q2/Q3/Q4 Backlog — RAG Universal System

> Generated from Q1 research findings
> Date: 2026-02-18

---

## Q2: Ingestion Pipeline + Vector Foundation

Goal: Build the ingestion pipeline defined in Q1, index initial procedures, add vector search.

| ID | Title | Priority | Depends on |
|----|-------|----------|------------|
| Q2-ING-01 | Implement fetch stage (requests + rate limiting + caching) | High | Q1 ingestion playbook |
| Q2-ING-02 | Implement HTML extraction (trafilatura + readability fallback) | High | Q2-ING-01 |
| Q2-ING-03 | Implement PDF extraction (pdfplumber + pymupdf) | Medium | Q2-ING-01 |
| Q2-ING-04 | Implement BOE XML parser | Medium | Q2-ING-01 |
| Q2-ING-05 | Implement normalization stage (ProcedureDoc v1 schema) | High | Q2-ING-02 |
| Q2-ING-06 | Implement URL canonicalization module | High | Q1 canonicalization policy |
| Q2-ING-07 | Implement allowlist checker | High | Q1 allowlist |
| Q2-ING-08 | Migrate existing 8 tramites to ProcedureDoc format | Medium | Q2-ING-05 |
| Q2-ING-09 | Ingest top 20 AGE procedure pages (SEPE, Seg Social, etc.) | High | Q2-ING-02/05 |
| Q2-ING-10 | Ingest 5 CCAA procedure pages per P0 community | Medium | Q2-ING-02/05 |
| Q2-VEC-01 | Choose embedding model (OpenAI ada-002 vs local) | High | - |
| Q2-VEC-02 | Set up vector store (FAISS or ChromaDB) | High | Q2-VEC-01 |
| Q2-VEC-03 | Implement semantic chunking for ProcedureDocs | High | Q2-ING-05, Q2-VEC-02 |
| Q2-VEC-04 | Upgrade retriever.py from JSONKBRetriever to VectorRetriever | High | Q2-VEC-02/03 |
| Q2-VEC-05 | Implement metadata pre-filtering (territory, source_type, canal) | Medium | Q2-VEC-04 |
| Q2-QA-01 | Retrieval accuracy eval (50+ queries, precision@3) | High | Q2-VEC-04 |
| Q2-QA-02 | End-to-end RAG eval (user query -> Clara response quality) | High | Q2-VEC-04 |
| Q2-LINK-01 | Implement link health checker (daily/weekly/monthly) | Medium | Q1 link-checking spec |
| Q2-LINK-02 | First full URL health check across all registries | Medium | Q2-LINK-01 |

**Q2 Exit criteria:**
- Ingestion pipeline processes HTML + PDF from at least 30 real government pages
- Vector retriever returns relevant results for 80%+ of test queries
- Existing 8 KB tramites migrated to ProcedureDoc format
- Link health checker runs at least once against full registry

---

## Q3: Coverage Expansion + Quality

Goal: Expand coverage to CCAA + municipal sources, improve retrieval quality.

| ID | Title | Priority | Depends on |
|----|-------|----------|------------|
| Q3-COV-01 | Ingest all P0 CCAA sources (Madrid, Cataluna, Andalucia, Valencia, Canarias) | High | Q2 pipeline |
| Q3-COV-02 | Ingest P1 CCAA sources (8 P1 communities) | Medium | Q3-COV-01 |
| Q3-COV-03 | Ingest Tier 1 municipal sources (top 20 cities, 5 procedures each) | High | Q2 pipeline |
| Q3-COV-04 | Ingest Tier 2 municipal sources (provincial capitals) | Medium | Q3-COV-03 |
| Q3-COV-05 | BOE daily monitoring pipeline (RSS + API) | Medium | Q2-ING-04 |
| Q3-COV-06 | Implement OCR for scanned PDFs (Tesseract/EasyOCR) | Low | Q2-ING-03 |
| Q3-QUAL-01 | LLM-assisted extraction for complex pages | Medium | Q2-ING-02 |
| Q3-QUAL-02 | Implement territorial disambiguation in retriever | High | Q2-VEC-04 |
| Q3-QUAL-03 | Re-ranking with cross-encoder | Medium | Q2-VEC-04 |
| Q3-QUAL-04 | Citation quality audit (informative links vs home pages) | High | Q2-VEC-04 |
| Q3-QUAL-05 | Multi-language support in retriever (es + ca + eu + gl) | Low | Q2-VEC-04 |
| Q3-QA-01 | Retrieval eval with 100+ queries, precision@3 >= 0.85 | High | Q3-COV-01/03 |
| Q3-QA-02 | Municipal disambiguation eval (20+ test cases) | High | Q3-QUAL-02 |
| Q3-LINK-01 | Automated weekly link health reports | Medium | Q2-LINK-01 |

**Q3 Exit criteria:**
- 100+ procedures indexed across AGE + 5 P0 CCAA + top 20 cities
- Retrieval precision@3 >= 0.85 on eval set
- Territorial disambiguation works for municipal-level queries
- Link health checker running on schedule with alerts

---

## Q4: Production Hardening + Scale

Goal: Production-ready RAG with monitoring, freshness, and full coverage.

| ID | Title | Priority | Depends on |
|----|-------|----------|------------|
| Q4-PROD-01 | Scheduled ingestion pipeline (weekly re-fetch with conditional requests) | High | Q3 pipeline |
| Q4-PROD-02 | Content drift detection and alerting | High | Q2-LINK-01 |
| Q4-PROD-03 | RAG response caching layer | Medium | Q3 retriever |
| Q4-PROD-04 | Retriever fallback chain (vector -> keyword -> directory) | High | Q3-QUAL-02 |
| Q4-PROD-05 | Monitoring dashboard (ingestion metrics, retrieval metrics, link health) | Medium | Q3 all |
| Q4-COV-01 | Ingest Tier 3 municipal sources (cities >50k) | Medium | Q3-COV-04 |
| Q4-COV-02 | Implement Tier 4 directory fallback (DIR3 + INE registry) | High | Q3 pipeline |
| Q4-COV-03 | Full CCAA coverage (all 19 communities, all P1+P2 procedures) | Medium | Q3-COV-02 |
| Q4-FRESH-01 | BOE monitoring -> auto-update affected procedures | High | Q3-COV-05 |
| Q4-FRESH-02 | Content staleness scoring (flag docs not re-fetched in 90+ days) | Medium | Q4-PROD-01 |
| Q4-QA-01 | Production RAG eval (200+ queries, precision@3 >= 0.90) | High | Q4-PROD-04 |
| Q4-QA-02 | User satisfaction tracking (thumbs up/down on RAG responses) | Medium | Q4-PROD-04 |
| Q4-TTS-01 | Premium TTS integration (ElevenLabs) | Low | Independent |

**Q4 Exit criteria:**
- 300+ procedures indexed and retrievable
- Freshness: all P0 sources re-checked weekly, P1 monthly
- Fallback chain covers 95%+ of municipality queries
- Production monitoring in place with automated alerts
