# Backlog Post-Fase 1

**Ultima actualizacion:** 2026-02-18
**Contexto:** Tickets pendientes tras el cierre de Fase 1 (Estabilizacion + Salida de Demo)

## Tickets Cerrados en Fase 1 (referencia)

| ID | Prioridad | Estado |
|----|-----------|--------|
| TICKET-01 | P0 | CERRADO — DEMO_MODE=false |
| TICKET-02 | P0 | CERRADO — Fix truncamiento KB |
| TICKET-03 | P0 | CERRADO — Expandir KB a 8 tramites |
| TICKET-04 | P1 | CERRADO — Hardening inyeccion prompt |
| TICKET-05 | P0/P1 | CERRADO — Accent normalization KB |
| TICKET-07 | P1 | CERRADO — Fix test_redteam collection |
| OBS-01 | P1 | CERRADO — Observabilidad pipeline |

## Tickets Pendientes

| ID | Prioridad | Descripcion | Evidencia / Contexto | Criterios de Aceptacion | Owner Sugerido |
|----|-----------|-------------|---------------------|------------------------|----------------|
| TICKET-06 | P1 | Renombrar WHISPER_ON a STT_ENABLED | Flag legacy: config.py:27 usa WHISPER_ON pero STT real es Gemini Flash (transcribe.py). Confusion semantica. | Flag renombrado en config.py, render.yaml, conftest.py. Tests pasan. | Backend |
| TICKET-08 | P2 | Cache hit ratio monitoring | Observabilidad basica implementada (OBS-01). Falta dashboard/metrica persistente de ratio cache hit vs miss. | Metrica cache_hit_ratio visible en logs o dashboard. Alerta si ratio < 30%. | DevOps |
| TICKET-09 | P2 | TTS upgrade: gTTS a voz de mayor calidad | gTTS produce voz robotica. Para publico vulnerable (mayores, migrantes) se necesita voz mas natural. | Evaluar alternativas: Google Cloud TTS, ElevenLabs, Edge TTS. Implementar con A/B test. | Backend |
| TICKET-10 | P2 | RAG retriever real (reemplazar stub) | retriever.py es un stub. JSONKBRetriever wrappea kb_lookup. VectorRetriever comentado. Pipeline no usa retriever.py. | Vector store funcional (ej: ChromaDB) con embeddings de tramites. Fallback a keyword si vector falla. | Backend |
| TICKET-11 | P1 | Expandir KB a 15+ tramites | Cobertura actual: 8/31 (26%). Faltan: reagrupacion_familiar, asilo, pension_no_contributiva, subsidio_mayores_52, renta_minima_ccaa, beca_estudios, ayuda_dependencia. | 15+ tramites en data/tramites/ con keywords ES+FR. Tests unitarios para cada uno. | KB/Research |
| TICKET-12 | P2 | Fuzzy/semantic KB matching | kb_lookup.py usa substring matching. Consultas vagas ("necesito ayuda economica") no matchean. | Implementar fuzzy matching (Levenshtein) o embeddings semanticos. Mantener keyword como fallback. | Backend |
| TICKET-13 | P2 | Rate limiting per user | Sin rate limiting. Un usuario puede enviar mensajes ilimitados y consumir cuota de Gemini. | Rate limit por numero de telefono (ej: 10 msgs/min). Respuesta amigable al exceder. | Backend/DevOps |
| TICKET-14 | P1 | Fix test_pipeline_text_cache_miss hanging | Test no mockea send_final_message. Con API keys en .env, llama a Gemini/Twilio real y cuelga. Actualmente deselected con -k flag. | Test mockea todas las llamadas externas. Puede ejecutarse sin -k exclusion. 0 tests deselected. | QA |
| TICKET-15 | P2 | Image input pipeline (OCR) | Pipeline detecta IMAGE input pero no hay procesamiento. detect_input_type retorna IMAGE pero pipeline no tiene branch para ello. | OCR funcional (Gemini Vision o Tesseract). Puede leer documentos y extraer texto relevante. | Backend |
| TICKET-16 | P2 | Multilingual system prompt variants | system_prompt.py tiene un unico prompt en espanol con placeholder {language}. Para FR necesita prompt nativo. | Prompt separado por idioma. Evaluado con evals bilingues. | Backend/KB |
| TICKET-17 | P1 | Verificar DEMO_MODE en runtime (produccion) | render.yaml dice false, pero Render Dashboard puede sobreescribir. No hay evidencia de verificacion en prod real. | Log o screenshot confirmando source=llm en un cache miss real en prod. Documentar en evidence/. | DevOps |
| TICKET-18 | P1 | Vectores residuales de inyeccion (tag breaking) | Hardening usa XML tags <user_query>. Un atacante podria cerrar el tag con </user_query> dentro del input. | Sanitizar/escapar < y > dentro del user_text antes de insertar en prompt. Test de red-team para tag breaking. | Security |
| TICKET-19 | P2 | KB schema unificado | 3 tramites originales usan como_hacerlo_madrid/como_solicitarla_madrid; 5 nuevos usan como_solicitar. _build_kb_context maneja ambos pero es fragil. | Migrar los 3 originales al schema nuevo. Documentar schema en data/tramites/SCHEMA.md. | KB/Backend |

## Priorizacion Sugerida para Fase 2

### Sprint 1 (P0-P1 criticos)
1. TICKET-11 — Expandir KB a 15+
2. TICKET-14 — Fix test colgado
3. TICKET-17 — Verificar DEMO_MODE en prod
4. TICKET-18 — Tag breaking injection

### Sprint 2 (P1 mejoras)
5. TICKET-06 — Renombrar WHISPER_ON
6. TICKET-12 — Fuzzy/semantic matching
7. TICKET-19 — KB schema unificado

### Sprint 3 (P2 funcionalidad)
8. TICKET-09 — TTS upgrade
9. TICKET-10 — RAG real
10. TICKET-13 — Rate limiting
11. TICKET-15 — Image/OCR pipeline
12. TICKET-16 — Multilingual prompts
13. TICKET-08 — Cache monitoring
