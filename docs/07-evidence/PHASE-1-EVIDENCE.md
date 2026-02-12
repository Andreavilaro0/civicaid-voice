# Evidencia Fase 1 — CivicAid Voice / Clara

## Tests ejecutados

```
Comando: pytest tests/ -v --tb=short
Resultado: 32/32 PASSED
Fecha: 2026-02-12
```

### Desglose
| Nivel | Tests | Resultado |
|---|---|---|
| Unit (T1-T5 + extras) | 21 | 21/21 PASS |
| Integration (T6-T8 + extras) | 7 | 7/7 PASS |
| E2E (T9-T10 + extras) | 4 | 4/4 PASS |

## Archivos creados (63)
- src/ — 22 archivos Python (app, routes, core, skills, utils, prompts)
- data/ — 9 archivos (demo_cache.json, 6 MP3s, 3 tramites JSON)
- tests/ — 12 archivos (5 unit, 3 integration, 1 e2e, 3 __init__.py)
- config — 8 archivos (.gitignore, .env.example, Dockerfile, requirements.txt, render.yaml, pyproject.toml, ci.yml, project-settings.json)
- docs/ — 12+ archivos (architecture, runbooks, testing, ops, evidence)
- .claude/ — 5 archivos (3 agents, project-settings, NOTION-SETUP-MANUAL)

## Componentes verificados

| Componente | Archivo | Verificacion | Estado |
|---|---|---|---|
| /webhook TwiML ACK | src/routes/webhook.py | curl POST → XML Response | ✅ |
| Cache-first (8 entries) | data/cache/demo_cache.json | cache_match("Que es el IMV?") → HIT imv_es | ✅ |
| 6 MP3 audios | data/cache/*.mp3 | ls -lh → 110-164KB each | ✅ |
| Twilio REST send | src/core/skills/send_response.py | Mock test pasa | ✅ |
| Logs estructurados | src/utils/logger.py | [ACK] [CACHE] [WHISPER] [LLM] [REST] [ERROR] | ✅ |
| Fetch media auth | src/core/skills/fetch_media.py | requests.get(auth=(SID,TOKEN)) | ✅ |
| OGG→WAV pydub | src/core/skills/convert_audio.py | lazy import pydub | ✅ |
| Whisper + timeout | src/core/skills/transcribe.py | ThreadPoolExecutor + WHISPER_TIMEOUT | ✅ |
| /health JSON | src/routes/health.py | 8 component fields | ✅ |
| 6 feature flags | src/core/config.py | DEMO_MODE, LLM_LIVE, WHISPER_ON, timeouts, AUDIO_BASE_URL | ✅ |
| KB 3 tramites | data/tramites/*.json | IMV, empadronamiento, tarjeta_sanitaria verified data | ✅ |
| Pipeline orchestrator | src/core/pipeline.py | audio + text + fallback flows | ✅ |
| System prompt | src/core/prompts/system_prompt.py | Anti-hallucination, 10 rules, 200 word limit | ✅ |
| Verify response | src/core/skills/verify_response.py | URL injection, word limit enforcement | ✅ |

## Pendiente para cierre completo

- [ ] git commit + push a GitHub
- [ ] Deploy a Render
- [ ] Configurar Twilio webhook
- [ ] Configurar cron-job.org
- [ ] Test WA real desde movil
- [ ] Demo rehearsal
- [ ] Video backup
