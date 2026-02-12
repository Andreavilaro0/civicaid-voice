# Toolkit Matrix — CivicAid Voice / Clara

> Comprehensive inventory of tool candidates across observability, structured outputs, guardrails, evals, RAG, red team, and tracing. Each entry is classified by integration level and current status.

---

## Current Stack (requirements.txt)

Already installed and used in production code:

| Package | Version | Role |
|---------|---------|------|
| flask | 3.1.* | Web framework |
| gunicorn | 21.* | WSGI server |
| twilio | 9.* | WhatsApp messaging |
| pydub | 0.25.* | Audio conversion |
| google-generativeai | 0.8.* | Gemini 1.5 Flash LLM |
| langdetect | 1.0.* | Language detection |
| requests | 2.32.* | HTTP client |
| python-dotenv | 1.0.* | Env var loading |
| gTTS | 2.5.* | Text-to-speech MP3 |
| openai-whisper | 20231117 | Audio transcription (optional) |

---

## Toolkit Matrix

### Observability

| Area | Tool Candidate | Purpose | Level | Impact | Requirement | Status |
|------|---------------|---------|-------|--------|-------------|--------|
| Observability | request_id middleware | Per-request correlation | core | high | none | planned |
| Observability | Stage timings (enhanced timing.py) | Latency tracking per skill | core | high | none | planned |
| Observability | OpenTelemetry SDK | Distributed tracing export | optional | medium | OTEL_ENDPOINT env var | stub |
| Observability | Phoenix (Arize) | LLM observability UI | optional | medium | PHOENIX_API_KEY (free tier) | stub |
| Observability | Helicone | LLM proxy logging | optional | low | HELICONE_API_KEY ($) | stub |

### Structured Outputs

| Area | Tool Candidate | Purpose | Level | Impact | Requirement | Status |
|------|---------------|---------|-------|--------|-------------|--------|
| Structured Outputs | Pydantic v2 | Response schema validation | core | high | pip install pydantic | planned |
| Structured Outputs | Instructor | Structured LLM extraction | optional | medium | pip install instructor (Gemini support TBD) | stub |
| Structured Outputs | JSON mode (native Gemini) | Force JSON output | core | medium | none | planned |

### Guardrails

| Area | Tool Candidate | Purpose | Level | Impact | Requirement | Status |
|------|---------------|---------|-------|--------|-------------|--------|
| Guardrails | Custom rules engine | Blocklist + disclaimers + PII | core | high | none | planned |
| Guardrails | NeMo Guardrails (NVIDIA) | Programmable safety rails | optional | medium | pip install nemoguardrails | stub |
| Guardrails | LLM Guard | Input/output scanning | optional | medium | pip install llm-guard | stub |
| Guardrails | Guardrails AI | Validation framework | optional | low | pip install guardrails-ai + API key | stub |

### Evals

| Area | Tool Candidate | Purpose | Level | Impact | Requirement | Status |
|------|---------------|---------|-------|--------|-------------|--------|
| Evals | Custom eval runner | Assertion-based eval | core | high | none | planned |
| Evals | DeepEval | LLM evaluation framework | optional | medium | pip install deepeval | stub |
| Evals | Giskard | ML testing framework | optional | low | pip install giskard | stub |
| Evals | promptfoo | CLI eval tool | optional | low | npm install | stub |

### RAG

| Area | Tool Candidate | Purpose | Level | Impact | Requirement | Status |
|------|---------------|---------|-------|--------|-------------|--------|
| RAG | JSON KB (current) | Keyword matching baseline | core | already integrated | none | installed |
| RAG | FAISS | Vector similarity search | optional | medium | pip install faiss-cpu | stub |
| RAG | Chroma | Vector store | optional | medium | pip install chromadb | stub |
| RAG | LangChain Retriever | Retriever abstraction | optional | low | pip install langchain | stub |

### Red Team

| Area | Tool Candidate | Purpose | Level | Impact | Requirement | Status |
|------|---------------|---------|-------|--------|-------------|--------|
| Red Team | Abuse prompt suite | Safety testing | core | high | none | planned |
| Red Team | Garak | LLM vulnerability scanner | optional | low | pip install garak | stub |

### Tracing

| Area | Tool Candidate | Purpose | Level | Impact | Requirement | Status |
|------|---------------|---------|-------|--------|-------------|--------|
| Tracing | Langfuse | LLM tracing + analytics | optional | medium | LANGFUSE_* env vars | stub |
| Tracing | Weights & Biases | Experiment tracking | optional | low | WANDB_API_KEY | stub |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| **installed** | In requirements.txt and used in production code |
| **integrated** | Code written, tested, and active in the pipeline |
| **stub** | Identified as candidate; no code yet; may require API key or paid tier |
| **planned** | Will be implemented in the current or next phase using existing dependencies |

---

## Decision Criteria

When to upgrade a tool from **stub** to **integrated**:

1. **Demonstrated need** -- A concrete gap in the current pipeline that the tool fills (e.g., unstructured LLM output causing downstream failures justifies Pydantic).
2. **Low friction** -- The tool can be installed with a single `pip install`, requires no paid API key for the MVP, and does not add more than 50 MB to the Docker image.
3. **Team capacity** -- At least one team member has time to own the integration, write tests, and document it.
4. **No vendor lock-in** -- The tool can be swapped out without rewriting core logic. Prefer tools that wrap a standard interface (e.g., OpenTelemetry over a proprietary SDK).
5. **Hackathon scope** -- For the OdiseIA4Good hackathon, prioritize tools that produce visible demo value (observability dashboards, safety disclaimers) over internal-only improvements.

A tool stays as **stub** if it requires a paid key, adds significant complexity, or solves a problem we have not yet encountered in practice.

---

## Integration Priority

Ranked by impact on demo quality, user safety, and pipeline reliability:

| Priority | Area | Rationale |
|----------|------|-----------|
| 1 | **Observability** | request_id and stage timings are prerequisites for debugging every other layer. Without correlation IDs, diagnosing production issues is guesswork. |
| 2 | **Guardrails** | Clara serves vulnerable users. Safety rails (PII filtering, disclaimers, blocklists) are non-negotiable before any public-facing demo. |
| 3 | **Structured Outputs** | Pydantic validation ensures the LLM response is parseable and consistent, reducing brittle string parsing downstream. |
| 4 | **Evals** | Automated eval cases catch regressions in LLM quality before they reach users. Builds on structured outputs. |
| 5 | **RAG** | The current JSON KB with keyword matching works for 3 tramites. Vector search becomes necessary only when the knowledge base grows beyond ~10 documents. |
| 6 | **Red Team** | Abuse prompt testing validates guardrails. Scheduled last because it depends on guardrails being in place first. |
