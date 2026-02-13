# FASE 3 — Demo en Vivo, Operaciones Reales y Presentacion

> **Proyecto:** CivicAid Voice / Clara
> **Hackathon:** OdiseIA4Good — UDIT
> **Fecha:** 2026-02-12
> **Objetivo:** Ejecutar una demo presencial de 6-8 minutos ante el jurado, con 2 momentos WOW en vivo, evidencia verificable y narrativa de impacto social.
>
> **Documentos relacionados:**
> [Plan Maestro (Fase 0)](./FASE0-PLAN-MAESTRO-FINAL.md) |
> [Implementacion MVP (Fase 1)](./FASE1-IMPLEMENTACION-MVP.md) |
> [Hardening y Deploy (Fase 2)](./FASE2-HARDENING-DEPLOY-INTEGRATIONS.md) |
> [Runbook Demo](../03-runbooks/RUNBOOK-DEMO.md) |
> [Resumen Ejecutivo / 1-Pager](../00-EXECUTIVE-SUMMARY.md)

---

## 1. Objetivo de Fase

Fases 1 y 2 entregaron un MVP funcional, desplegado y verificado: 96 tests, pipeline de 11 skills, deploy en Render, Twilio configurado, observabilidad activa. Fase 3 convierte todo eso en una **presentacion convincente de 6-8 minutos** que demuestre impacto social y solidez tecnica.

Fase 3 NO modifica codigo. Se enfoca en:

- **Seleccion de concepto de demo** con analisis de pros/cons.
- **Guion minuto a minuto** con cues visuales, verbales y de evidencia.
- **2 momentos WOW** definidos con ruta tecnica verificable.
- **1-pager** para entregar al jurado.
- **Riesgos y mitigaciones** para la demo en vivo.

---

## 2. Tres Conceptos de Demo

### Concepto A: Ciudadano-first (Storytelling)

**Enfoque:** Abrir con la historia de Maria (espanola, madre) y Ahmed (marroqui, recien llegado). El jurado experimenta la demo como si fuera un usuario real. La tecnologia se explica despues del momento emocional.

| Aspecto | Detalle |
|---------|---------|
| **Apertura** | Narrativa emocional: "Imaginad que sois Maria..." |
| **WOW 1** | Maria pregunta por el IMV en texto — respuesta instantanea con audio |
| **WOW 2** | Ahmed envia nota de voz en frances — respuesta en frances con audio |
| **Cierre** | Datos de impacto (3.2M inmigrantes, 40% barrera idiomatica) |

**Pros:**
- Maximo impacto emocional — el jurado "siente" el problema antes de ver la solucion.
- Los momentos WOW son tangibles: ven WhatsApp real en pantalla.
- Facil de seguir para jurados no tecnicos.
- Los datos de impacto cierran con fuerza.

**Contras:**
- Riesgo de parecer "solo storytelling" sin profundidad tecnica.
- Si la demo en vivo falla, la narrativa pierde el ancla emocional.

---

### Concepto B: Institucional (Ayuntamiento / ONG)

**Enfoque:** Abrir con el problema institucional: ayuntamientos saturados, trabajadores sociales desbordados, inmigrantes que no completan tramites. Clara como herramienta de la administracion publica.

| Aspecto | Detalle |
|---------|---------|
| **Apertura** | "En Madrid, la oficina de atencion al ciudadano recibe 2.000 consultas diarias..." |
| **WOW 1** | Demo de texto — Clara como primer filtro de consultas |
| **WOW 2** | Demo de audio multilingue — Clara como traductor automatico |
| **Cierre** | Modelo B2G, coste por consulta ($0.002), escalabilidad |

**Pros:**
- Alineado con la tematica de "4Good" (impacto social verificable).
- Modelo de negocio claro para el jurado.
- Posiciona Clara como producto, no solo como prototipo.

**Contras:**
- Menos emocional — el jurado no "vive" el problema de primera mano.
- Requiere datos institucionales que no tenemos verificados.
- La demo en vivo puede parecer fria.

---

### Concepto C: Jurado Tecnico (Arquitectura-first)

**Enfoque:** Abrir con el diagrama de arquitectura, explicar el patron TwiML ACK, las 11 skills, los feature flags. Despues hacer la demo en vivo como "prueba" de que funciona.

| Aspecto | Detalle |
|---------|---------|
| **Apertura** | "Hemos construido un pipeline de 11 skills con patron TwiML ACK..." |
| **WOW 1** | Mostrar la ruta tecnica en vivo: webhook → cache hit → <2s |
| **WOW 2** | Mostrar transcripcion + deteccion de idioma + KB lookup → respuesta |
| **Cierre** | 96 tests, 9 feature flags, deploy reproducible, observabilidad |

**Pros:**
- Demuestra solidez de ingenieria y decision-making.
- Cada claim tiene un comando de verificacion.
- Impresiona a jurados tecnicos.

**Contras:**
- Pierde completamente al jurado no tecnico.
- La demo se siente como una "revision de codigo", no una presentacion.
- El impacto social queda relegado al final.

---

### Decision: Concepto A (Ciudadano-first) con refuerzo tecnico

**Razon:** En un hackathon de impacto social (OdiseIA4Good), el jurado evalua tanto la calidad tecnica como el impacto real. El concepto A maximiza el impacto emocional y permite insertar evidencia tecnica en puntos estrategicos sin perder la narrativa.

**Adaptacion:** Intercalar "evidence checkpoints" en momentos naturales de la demo. Cuando Robert dice "en menos de 2 segundos", hay un comando detras que lo prueba. Cuando dice "96 tests", hay un `pytest` que lo respalda.

---

## 3. Alcance

### Dentro del Alcance

| # | Area | Que se hace |
|---|------|-------------|
| 1 | **Concepto de demo** | Analisis de 3 opciones, seleccion con justificacion |
| 2 | **Guion 6-8 min** | Timeline cronometrado con cues MUESTRO/DIGO/EVIDENCIA |
| 3 | **WOW 1 + WOW 2** | Definicion formal con ruta tecnica y evidence checkpoints |
| 4 | **1-pager** | Executive Summary como documento para entregar al jurado |
| 5 | **Riesgos demo** | Lista con mitigaciones concretas y responsables |
| 6 | **Ensayo** | Checklist pre-demo, cronograma de preparacion |

### Fuera del Alcance

| Excluido | Razon |
|----------|-------|
| Cambios al codigo | Pipeline completo y testeado en Fases 1-2 |
| Nuevos tramites o idiomas | Fuera del alcance del hackathon |
| Slides/diapositivas | Responsabilidad de Andrea (coordinacion) |
| Video de backup | Responsabilidad de Daniel |

---

## 4. Gates

Cada gate es un checkpoint de calidad. **No se avanza sin evidencia de que los criterios se cumplen.**

### P3.1 — Twilio WhatsApp Real End-to-End

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| P3.1.1 | Texto en espanol funciona en vivo | "Que es el IMV?" → respuesta correcta via WhatsApp real | Screenshot o log de Render con `[CACHE] HIT imv_es` |
| P3.1.2 | Audio en frances funciona en vivo | Nota de voz → transcripcion → respuesta en frances | Screenshot o log con `[PIPELINE]` skills ejecutadas |
| P3.1.3 | Audio MP3 se reproduce en WhatsApp | Audio adjunto audible en el dispositivo | `curl -I .../static/cache/imv_es.mp3` → HTTP 200 |
| P3.1.4 | Latencia cache <2s | Tiempo de respuesta aceptable para demo | Logs con timing o cronometro manual |

### P3.2 — Deploy y Ops Demo-Grade

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| P3.2.1 | Render activo sin cold start | /health responde en <2s | `curl -s -w "%{time_total}" .../health` → <2s |
| P3.2.2 | Cron warm-up operativo | Historial de pings exitosos | cron-job.org historial o similar |
| P3.2.3 | Feature flags configurados | DEMO_MODE=true, LLM_LIVE=true, WHISPER_ON=true | Render Dashboard → Environment verificado |
| P3.2.4 | Logs operativos para debug | Logs visibles en Render Dashboard | Render → Logs → lineas con `[ACK]`, `[CACHE]`, `[PIPELINE]` |

### P3.3 — QA y Evidencia

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| P3.3.1 | 96 tests pasan | Suite completa verde | `pytest tests/ -v --tb=short` → 96 tests (91 passed + 5 xpassed) |
| P3.3.2 | Lint limpio | ruff sin errores | `ruff check src/ tests/ --select E,F,W --ignore E501` → 0 errores |
| P3.3.3 | Script de verificacion | Script automatizado pasa | `bash scripts/phase2_verify.sh` → PASS |
| P3.3.4 | Evidencia capturada | Outputs guardados en docs/07-evidence/ | Archivos de evidencia actualizados |

### P3.4 — Observabilidad Demo-Grade

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| P3.4.1 | Logs estructurados activos | request_id y timings en cada peticion | Log de Render con `[OBS]` tags |
| P3.4.2 | /health completo | 8 componentes en respuesta JSON | `curl .../health` → JSON con 8 keys en components |

### P3.5 — Notion PMO Actualizado

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| P3.5.1 | 3 DBs consistentes | Backlog, KB, Testing con datos actuales | Query a Notion MCP o screenshot |
| P3.5.2 | Estado Fase 3 reflejado | Entradas de Fase 3 en Backlog | Entradas creadas en Notion |

### P3.6 — Comms y Demo (este gate)

| # | Criterio | DoD | Evidencia requerida |
|---|----------|-----|---------------------|
| P3.6.1 | 3 conceptos analizados | Pros/cons documentados, 1 elegido | Seccion 2 de este documento |
| P3.6.2 | Guion 6-8 min escrito | Timeline con MUESTRO/DIGO/EVIDENCIA | Seccion 7 de este documento + RUNBOOK-DEMO.md seccion 7 |
| P3.6.3 | WOW 1 y WOW 2 definidos | Ruta tecnica + evidence checkpoint por cada WOW | Seccion 6 de este documento |
| P3.6.4 | 1-pager actualizado | Problema → Solucion → Arquitectura → Validaciones → Impacto | `docs/00-EXECUTIVE-SUMMARY.md` |
| P3.6.5 | Riesgos documentados | Lista con mitigaciones y responsables | Seccion 8 de este documento |
| P3.6.6 | Checklist pre-demo | 12 items con timing y responsable | Seccion 9 de este documento |

---

## 5. Asignacion de Equipos

| # | Agente | Gate | Alcance de archivos | Salidas |
|---|--------|------|-------------------|---------|
| A | Backend/Pipeline | P3.1 | src/ (read-only), WhatsApp real | Test e2e en vivo, logs capturados |
| B | DevOps/Deploy | P3.2 | Dockerfile, render.yaml, scripts/ | Deploy verificado, cron operativo |
| C | QA/Testing | P3.3 | tests/, scripts/, docs/07-evidence/ | Script verificacion, evidencia |
| D | Observability | P3.4 | src/utils/observability.py (read-only) | Logs verificados |
| E | Notion/PMO | P3.5 | docs/06-integrations/, Notion MCP | DBs actualizadas |
| F | Comms/Demo | P3.6 | docs/01-phases/FASE3*, docs/03-runbooks/RUNBOOK-DEMO.md, docs/00-EXECUTIVE-SUMMARY.md | Guion, 1-pager, riesgos |

**Regla:** El lead solo coordina y sintetiza. Todo trabajo lo hacen los teammates. Ningun teammate edita fuera de su scope.

---

## 6. Definicion de WOW 1 y WOW 2

### WOW 1 — Texto en Espanol (Maria)

| Campo | Valor |
|-------|-------|
| **Persona** | Maria, madre espanola, desconoce el IMV |
| **Canal** | WhatsApp texto |
| **Idioma** | Espanol |
| **Input** | `Que es el IMV?` |
| **Output esperado** | Texto detallado IMV + audio MP3 (`imv_es.mp3`) |
| **Latencia objetivo** | < 2 segundos |
| **Ruta tecnica** | `POST /webhook` → cache hit (`imv_es`) → Twilio REST → WhatsApp |
| **Evidence checkpoint** | `curl -s https://civicaid-voice.onrender.com/health \| python3 -m json.tool` → `cache_entries: 8` |

**Por que es WOW:** El jurado ve en tiempo real como una persona recibe informacion verificada sobre un tramite complejo en menos de 2 segundos, con texto y audio, sin instalar nada.

### WOW 2 — Audio en Frances (Ahmed)

| Campo | Valor |
|-------|-------|
| **Persona** | Ahmed, inmigrante marroqui, habla frances |
| **Canal** | WhatsApp nota de voz |
| **Idioma** | Frances |
| **Input** | Nota de voz: "Bonjour, je viens d'arriver en Espagne et j'ai besoin de savoir comment faire le empadronamiento, s'il vous plait." |
| **Output esperado** | Texto en frances sobre empadronamiento + audio MP3 en frances (`ahmed_fr.mp3`) |
| **Latencia objetivo** | ~10 segundos (transcripcion + LLM + TTS) |
| **Ruta tecnica** | `POST /webhook` → Twilio media → descarga OGG → transcripcion Gemini → detect lang (`fr`) → cache hit/KB lookup → respuesta en frances → audio MP3 → Twilio REST → WhatsApp |
| **Evidence checkpoint** | Los logs de Render muestran `[PIPELINE]` con cada skill ejecutada y timings |

**Por que es WOW:** El jurado ve como una persona que NO habla espanol recibe orientacion sobre un tramite espanol, en SU idioma, usando solo la voz. Sin traductor, sin intermediarios.

---

## 7. Guion de Demo — 6-8 Minutos

### Formato de cues

Cada entrada sigue el formato:

> **MUESTRO** → lo que se ve en pantalla
> **DIGO** → lo que dice Robert
> **EVIDENCIA** → comando o archivo que respalda el claim

---

### t=0:00 — Apertura: El Problema (1 minuto)

**MUESTRO** → Slide con datos: "3.2M inmigrantes en Espana. 40% no completa tramites por barrera idiomatica."

**DIGO** →
> "En Espana hay 3 coma 2 millones de inmigrantes. El 40 por ciento no consigue completar tramites basicos como el empadronamiento o la solicitud del Ingreso Minimo Vital. El problema no es que no quieran. Es que la informacion esta en espanol tecnico, repartida en 20 webs distintas, y las colas telefonicas duran horas."
>
> "Hoy os voy a presentar a Clara. Un asistente de WhatsApp que habla el idioma del usuario, entiende voz y texto, y da informacion verificada sobre tramites reales. Nada de descargar apps. Solo WhatsApp."

**EVIDENCIA** → Datos de INE 2025 sobre poblacion inmigrante en Espana. KB verificada contra fuentes oficiales: `data/tramites/imv.json`, `data/tramites/empadronamiento.json`, `data/tramites/tarjeta_sanitaria.json`.

---

### t=1:00 — Presentacion de Clara (30 segundos)

**MUESTRO** → Slide de arquitectura simplificado (usuario → WhatsApp → Clara → respuesta) o transicion directa al movil.

**DIGO** →
> "Clara funciona asi de simple: tu abres WhatsApp, le escribes o le hablas, y Clara te responde en tu idioma con informacion verificada. Veamoslo en vivo."

**EVIDENCIA** → Diagrama en `docs/02-architecture/ARCHITECTURE.md` seccion 2.

---

### t=1:30 — WOW 1: Maria pregunta por el IMV (2 minutos)

**MUESTRO** → Pantalla del movil proyectada con WhatsApp abierto, conversacion con Clara.

**Paso 1 — Saludo:**

**MUESTRO** → Operador escribe y envia: `Hola`

**DIGO** →
> "Imaginad que sois Maria. Es una madre espanola que acaba de recibir una carta del gobierno sobre algo llamado IMV. No tiene ni idea de que es. Abre WhatsApp y escribe 'Hola'."

**MUESTRO** → Respuesta de Clara en <2 segundos: saludo + lista de 3 tramites.

**EVIDENCIA** → Cache entry `saludo_es` en `data/cache/demo_cache.json`. Verificar: `curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool` → `cache_entries: 8`.

**Paso 2 — Pregunta clave:**

**MUESTRO** → Operador escribe y envia: `Que es el IMV?`

**DIGO** →
> "Maria pregunta directamente: 'Que es el IMV?'"

**MUESTRO** → Clara responde con texto detallado + envia audio MP3.

**DIGO** (mientras aparece la respuesta) →
> "En menos de dos segundos, Maria tiene toda la informacion que necesita: que es el IMV, los requisitos, la cuantia — 604 euros al mes —, como solicitarlo, y un audio que puede escuchar mientras cocina o va en el metro. Sin descargar ninguna app. Sin esperar en una cola telefonica. Solo WhatsApp."

**EVIDENCIA** →
- Cache entry `imv_es` con audio `imv_es.mp3`.
- Audio accesible: `curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3` → HTTP 200 + `Content-Type: audio/mpeg`.
- KB oficial: `data/tramites/imv.json` con fuente verificada.

---

### t=3:30 — Transicion a Ahmed (30 segundos)

**MUESTRO** → Misma pantalla de WhatsApp (o slide breve de transicion).

**DIGO** →
> "Pero Clara no solo habla espanol. Pensad ahora en Ahmed. Acaba de llegar de Marruecos. Habla frances. Necesita empadronarse para poder acceder a la sanidad publica, pero no sabe por donde empezar. No va a escribir en espanol. Le envia una nota de voz en frances a Clara."

**EVIDENCIA** → Clara soporta 2 idiomas: ES, FR. Deteccion automatica via `langdetect`. Ver `src/core/skills/detect_lang.py`.

---

### t=4:00 — WOW 2: Ahmed envia audio en frances (2 minutos)

**MUESTRO** → Operador envia nota de voz en frances preguntando por el empadronamiento.

**DIGO** (frases puente mientras Clara procesa, ~10 segundos) →
> "Ahora Clara esta haciendo algo fascinante. Primero, convierte la voz de Ahmed a texto. Luego detecta que esta hablando en frances. Busca informacion sobre el empadronamiento en nuestra base de conocimiento verificada. Genera una respuesta en frances. Y la convierte de nuevo a audio. Todo automatico."

**MUESTRO** → Clara responde con texto en frances + audio MP3 en frances.

**DIGO** →
> "Y ahi esta. Ahmed tiene su respuesta en frances. Le explica que es el empadronamiento, que documentos necesita, donde ir en Madrid, y que es un derecho — incluso sin contrato de alquiler. Sin traductor. Sin intermediarios. Solo WhatsApp y Clara."

**EVIDENCIA** →
- Pipeline completo: 11 skills ejecutadas secuencialmente. Ver `src/core/pipeline.py`.
- Cache entry `ahmed_empadronamiento_fr` con audio `ahmed_fr.mp3`.
- Ruta tecnica: webhook → fetch_media → transcribe (Gemini) → detect_lang → cache_match → send_response.
- 96 tests verifican el pipeline: `pytest tests/ -v --tb=short`.

---

### t=6:00 — Evidencia Tecnica (1 minuto)

**MUESTRO** → Terminal o slide con datos clave.

**DIGO** →
> "Esto no es un mockup. Es un sistema real desplegado en produccion. Dejadme mostraros los numeros:"
>
> "96 tests automatizados que verifican cada parte del sistema."
> "Un pipeline de 11 skills especializadas — desde la deteccion del tipo de entrada hasta el envio de la respuesta."
> "9 feature flags que nos permiten controlar el comportamiento sin tocar codigo."
> "Base de conocimiento con informacion verificada de fuentes oficiales del gobierno."
> "Deploy en Render con health check cada 14 minutos."
> "Coste por consulta: 0 coma 2 centimos en cache, 1 centimo con IA."

**EVIDENCIA** →

| Claim | Comando de verificacion | Output esperado |
|-------|------------------------|-----------------|
| 96 tests | `pytest tests/ -v --tb=short` | 96 passed (91 passed + 5 xpassed) |
| 11 skills | `ls src/core/skills/*.py` | 11 archivos |
| 9 feature flags | Ver `src/core/config.py` | 9 flags documentadas |
| KB verificada | `ls data/tramites/` | 3 archivos JSON |
| Deploy activo | `curl -s https://civicaid-voice.onrender.com/health` | `"status": "ok"` |
| 8 cache entries | health output | `"cache_entries": 8` |
| Lint limpio | `ruff check src/ tests/ --select E,F,W --ignore E501` | 0 errores |

---

### t=7:00 — Cierre: Impacto y Vision (1 minuto)

**MUESTRO** → Slide final o pantalla de WhatsApp con las conversaciones de Maria y Ahmed visibles.

**DIGO** →
> "Hoy Clara cubre 3 tramites en 2 idiomas. Pero la arquitectura esta disenada para escalar. Manana pueden ser cientos de tramites en decenas de idiomas."
>
> "Lo mas importante: Clara funciona en el canal que ya usan mil millones de personas. No hay que instalar nada. No hay que aprender nada. Solo abrir WhatsApp y preguntar."
>
> "Para Maria, eso significa entender una carta del gobierno. Para Ahmed, eso significa poder empadronarse y acceder a la sanidad publica. Para millones de personas vulnerables, eso significa dejar de estar solas frente a la burocracia."
>
> "Esto es Clara. Gracias."

**EVIDENCIA** →
- WhatsApp: 95% penetracion en Espana (Statista 2025).
- 3 tramites cubiertos: IMV, Empadronamiento, Tarjeta Sanitaria.
- 2 idiomas: ES, FR.
- Arquitectura stateless: escala horizontalmente.
- Repo completo: codigo, tests, docs, deploy — todo verificable.

---

## 8. Riesgos y Mitigaciones

| # | Riesgo | Probabilidad | Impacto | Mitigacion | Responsable |
|---|--------|-------------|---------|------------|-------------|
| R1 | Render en cold start (respuesta > 5s) | Media | Alto | `curl /health` T-15 min y T-1 min antes de demo. Cron cada 14 min activo. | Marcos |
| R2 | WiFi del venue inestable | Media | Critico | Tener hotspot movil como backup. Probar antes de empezar. | Andrea |
| R3 | Transcripcion de audio falla | Baja | Alto | Tener capturas de pantalla pre-grabadas con la conversacion completa en frances. Reproducir MP3 de backup. | Robert |
| R4 | Audio MP3 no se reproduce en WhatsApp | Baja | Medio | Robert lee el texto en voz alta. El texto siempre llega aunque el audio falle. | Robert |
| R5 | Twilio sandbox expirado | Baja | Critico | Re-enviar `join <codigo>` al sandbox 30 min antes. Tener screenshots de backup. | Marcos |
| R6 | Todo falla (sin internet, sin Render) | Muy baja | Critico | Video de backup `demo-backup.mp4` listo en el portatil. Daniel lo reproduce. | Daniel |
| R7 | Demo excede el tiempo (>8 min) | Media | Medio | Robert ensaya con cronometro. Secciones opcionales marcadas. Cortar evidencia tecnica si es necesario. | Robert |
| R8 | Jurado interrumpe con preguntas | Media | Bajo | Robert responde brevemente y retoma el guion. Puntos de conversacion post-demo preparados. | Robert |

---

## 9. Checklist Pre-Demo

| # | Verificacion | Comando / Accion | Cuando | Responsable |
|---|---|---|---|---|
| 1 | Cron warm-up activo | Verificar historial en cron-job.org | T-60 min | Marcos |
| 2 | Render despierto | `curl https://civicaid-voice.onrender.com/health` → 200 OK | T-15 min | Marcos |
| 3 | WhatsApp Sandbox unido | Enviar `join <codigo>` al +1 415 523 8886 | T-30 min | Marcos |
| 4 | Movil cargado >80% | Verificar bateria | T-30 min | Operador |
| 5 | Video backup cargado | `demo-backup.mp4` en el portatil | T-30 min | Daniel |
| 6 | Audio frances pre-grabado | Nota de voz en frances lista en el movil | T-30 min | Lucas |
| 7 | WiFi estable | Conectar al WiFi del venue, probar | T-15 min | Andrea |
| 8 | Pantalla compartida | Proyector/TV mostrando WhatsApp | T-10 min | Andrea |
| 9 | Probar WOW 1 | Enviar "Que es el IMV?" → verificar respuesta | T-10 min | Operador |
| 10 | Probar WOW 2 | Enviar audio en frances → verificar respuesta | T-5 min | Operador |
| 11 | Limpiar chat | Borrar mensajes de prueba de WhatsApp | T-2 min | Operador |
| 12 | Health check final | `curl /health` | T-1 min | Marcos |

---

## 10. Feature Flags para Demo

Configurar en Render Dashboard -> Environment **antes** de la demo:

```env
DEMO_MODE=true
LLM_LIVE=true
WHISPER_ON=true
GUARDRAILS_ON=true
OBSERVABILITY_ON=true
```

---

## 11. Puntos de Conversacion Post-Demo

Si el jurado hace preguntas tras los 6-8 minutos, Robert puede expandir sobre:

| Tema | Puntos clave | Evidencia |
|------|-------------|-----------|
| **Tecnologia** | Gemini 1.5 Flash, gTTS, pipeline 11 skills, patron TwiML ACK | `docs/02-architecture/ARCHITECTURE.md` |
| **Seguridad** | Guardrails pre/post, signature validation, scan de secretos | Gate P2.6 PASS |
| **Escalabilidad** | Stateless, KB extensible, coste $0.002-$0.01/consulta | `src/core/config.py` |
| **Modelo de negocio** | B2G (ayuntamientos), ONG/cooperacion, freemium | 1-pager |
| **Observabilidad** | request_id por peticion, timings por skill, /health con 8 componentes | `docs/05-ops/OBSERVABILITY-QUICKSTART.md` |
| **Testing** | 96 tests (unit + integration + e2e), ruff lint clean | `pytest tests/ -v` |

---

## 12. Criterio de Cierre de Fase 3

Fase 3 se considera cerrada cuando:

1. Guion de 6-8 min escrito con cues MUESTRO/DIGO/EVIDENCIA.
2. WOW 1 y WOW 2 definidos con ruta tecnica y evidence checkpoints.
3. 1-pager Markdown actualizado en `docs/00-EXECUTIVE-SUMMARY.md`.
4. Riesgos documentados con mitigaciones.
5. Checklist pre-demo completada.
6. Ensayo de demo ejecutado al menos una vez.
7. Video de backup grabado.

---

## Como se verifica

```bash
# Verificar que el deploy esta activo
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool

# Verificar que los audios MP3 son accesibles
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3

# Verificar que los tests pasan
pytest tests/ -v --tb=short

# Verificar lint limpio
ruff check src/ tests/ --select E,F,W --ignore E501
```

## Referencias

- [Runbook Demo](../03-runbooks/RUNBOOK-DEMO.md)
- [Resumen Ejecutivo / 1-Pager](../00-EXECUTIVE-SUMMARY.md)
- [Arquitectura](../02-architecture/ARCHITECTURE.md)
- [Fase 2](./FASE2-HARDENING-DEPLOY-INTEGRATIONS.md)
- [Fase 1](./FASE1-IMPLEMENTACION-MVP.md)
- [Estado de Fases](../07-evidence/PHASE-STATUS.md)

---

> **Regla de oro:** Si algo falla, nunca parar. Siempre hay un fallback. La demo debe fluir sin importar que pase con la tecnologia. Cada claim tiene un comando que lo respalda.
