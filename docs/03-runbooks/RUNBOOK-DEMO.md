# RUNBOOK — Demo "Clara" Chatbot WhatsApp

> **Resumen en una linea:** Guia paso a paso para ejecutar la demo de Clara en vivo ante el jurado (6-8 minutos), con 2 momentos WOW (texto + audio), evidence checkpoints verificables, 8 entradas de cache documentadas y procedimientos de fallback.

## Que es

Este runbook describe el procedimiento completo para ejecutar la demo de Clara, el asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar tramites de servicios sociales (IMV, Empadronamiento, Tarjeta Sanitaria). La demo dura **6-8 minutos** y contiene 2 momentos WOW en vivo con evidence checkpoints que respaldan cada claim.

> **Concepto elegido:** Ciudadano-first (storytelling) con refuerzo tecnico. Analisis de los 3 conceptos evaluados en [FASE3-DEMO-OPS-REAL.md](../01-phases/FASE3-DEMO-OPS-REAL.md).

## Para quien

- **Robert** (presentador principal)
- **Equipo tecnico** (operador de movil, backup tecnico)
- Cualquier miembro del equipo (Andrea, Marcos, Lucas, Daniel) que necesite entender el flujo completo

## Que incluye

- Checklist pre-demo con comandos de verificacion
- Guion WOW 1 (flujo texto en espanol) y WOW 2 (flujo audio en frances)
- Documentacion de las 8 entradas de cache con triggers y respuestas esperadas
- Procedimientos de fallback y troubleshooting

## Que NO incluye

- Configuracion inicial de Twilio (ver `docs/06-integrations/TWILIO-SETUP-GUIDE.md`)
- Deploy a Render (ver `docs/05-ops/RENDER-DEPLOY.md`)
- Configuracion de cron warm-up (ver `docs/03-runbooks/RUNBOOK-PHASE2.md`)

---

## 1. Comandos de Verificacion Previos

Ejecutar estos comandos **antes** de cualquier otra cosa. Si alguno falla, resolver antes de continuar.

```bash
# 1. Verificar que Render esta despierto
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
# Esperado: "status": "ok", "cache_entries": 8

# 2. Verificar que los audios MP3 son accesibles
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
# Esperado: HTTP/2 200, Content-Type: audio/mpeg

# 3. Verificar webhook (devolvera 200 o 403 por signature validation)
curl -s -o /dev/null -w "%{http_code}" \
  -X POST https://civicaid-voice.onrender.com/webhook \
  -d "Body=test" -d "From=whatsapp:+34600000000" -d "NumMedia=0"
# Esperado: 200 o 403

# 4. Verificar tests localmente (si hay acceso al repo)
pytest tests/ -v --tb=short
# Esperado: 96 tests (91 passed + 5 xpassed)
```

---

## 2. Checklist Pre-Demo

Verificar **todos** los puntos antes de subir al escenario. Sin excepciones.

| # | Verificacion | Comando / Accion | Estado |
|---|---|---|---|
| 1 | Render despierto (sin cold start) | `curl https://civicaid-voice.onrender.com/health` devuelve 200 OK | - |
| 2 | WhatsApp Sandbox unido | Enviar "join <codigo>" al +1 415 523 8886 desde el movil de demo | - |
| 3 | Movil cargado >80% | Verificar bateria del dispositivo de demo | - |
| 4 | Video de backup cargado | Tener `demo-backup.mp4` en el portatil, listo para reproducir | - |
| 5 | Feature flags configurados | Verificar en Render Dashboard -> Environment | - |
| 6 | Audio demo pre-grabado listo | Tener nota de voz en frances grabada en el movil | - |
| 7 | WiFi estable | Conectar al WiFi del venue, verificar velocidad | - |
| 8 | Pantalla compartida lista | Proyector/TV mostrando WhatsApp Web o mirror del movil | - |

### Feature Flags Requeridos

Configurar en Render Dashboard -> Environment **antes** de la demo:

```env
DEMO_MODE=true
LLM_LIVE=true
WHISPER_ON=true
```

- `DEMO_MODE=true` — Activa respuestas de cache optimizadas para la demo, reduce latencia.
- `LLM_LIVE=true` — Permite llamadas al LLM (Gemini) en tiempo real si no hay cache hit.
- `WHISPER_ON=true` — Activa transcripcion de audio para el flujo de Ahmed.

---

## 3. Cronograma de Preparacion

| Tiempo antes de demo | Accion |
|---|---|
| -30 min | Verificar WiFi, cargar video backup, unir sandbox WhatsApp |
| -15 min | `curl /health` para despertar Render |
| -10 min | Probar WOW 1 (enviar "Que es el IMV?" y verificar respuesta) |
| -5 min | Probar WOW 2 (enviar audio en frances y verificar respuesta) |
| -2 min | Limpiar chat de WhatsApp (borrar mensajes de prueba) |
| -1 min | `curl /health` final, abrir pantalla compartida |
| t=0:00 | **Comenzar demo** |

---

## 4. WOW 1 — Flujo Texto (Espanol)

**Duracion:** ~1 minuto
**Objetivo:** Demostrar que Clara responde a texto en espanol desde cache en menos de 2 segundos.

### Paso 1: Enviar "Hola"

**Accion:** El operador escribe y envia en WhatsApp:

```
Hola
```

**Respuesta esperada (< 2 segundos):**

Clara responde con un mensaje de bienvenida:

> Hola! Soy Clara, tu asistente para tramites de servicios sociales en Espana.
>
> Puedo ayudarte con:
> 1. **Ingreso Minimo Vital (IMV)** — ayuda economica
> 2. **Empadronamiento** — registro en tu municipio
> 3. **Tarjeta Sanitaria** — acceso a la sanidad publica
>
> Sobre que te gustaria saber?

**Ruta tecnica:** `POST /webhook` -> cache hit (`saludo_es`) -> respuesta texto -> Twilio REST -> WhatsApp.

### Paso 2: Enviar "Que es el IMV?"

**Accion:** El operador escribe y envia:

```
Que es el IMV?
```

**Respuesta esperada (< 2 segundos):**

1. Clara responde con un mensaje de texto detallado explicando el Ingreso Minimo Vital:
   - Que es (prestacion economica de la Seguridad Social)
   - Requisitos principales (edad, residencia, vulnerabilidad economica)
   - Cuantia 2024: desde 604,21 EUR/mes
   - Como solicitarlo (online, presencial, telefono)
   - Enlace a mas informacion
2. Clara envia un **audio MP3** con la misma respuesta narrada (`imv_es.mp3`).

**Robert dice (mientras aparece la respuesta):**

> "En menos de dos segundos, Maria tiene toda la informacion que necesita: texto claro y un audio que puede escuchar mientras cocina o va en el metro. Sin descargar ninguna app. Sin esperar en una cola telefonica. Solo WhatsApp."

**Ruta tecnica:** `POST /webhook` -> cache hit (`imv_es`) -> respuesta texto + audio pre-generado -> Twilio REST -> WhatsApp.

### Paso 3: Enviar "Empadronamiento"

**Accion:** El operador escribe y envia:

```
Empadronamiento
```

**Respuesta esperada (< 2 segundos):**

Clara responde con informacion detallada sobre el empadronamiento:
- Que es (registro obligatorio en el municipio)
- Documentos necesarios (DNI/NIE/pasaporte, contrato de alquiler)
- Como hacerlo en Madrid (cita, oficina OAC, documentos originales)
- Dato importante: es un DERECHO, incluso sin contrato
- Telefono y enlace oficial

Ademas envia audio MP3 (`empadronamiento_es.mp3`).

**Ruta tecnica:** `POST /webhook` -> cache hit (`empadronamiento_es`) -> respuesta texto + audio -> Twilio REST -> WhatsApp.

---

## 5. WOW 2 — Flujo Audio (Frances)

**Duracion:** ~1 minuto
**Objetivo:** Demostrar que Clara transcribe audio en frances, detecta el idioma y responde en frances.

### Paso 1: Nota de voz preguntando por el IMV

**Accion:** El operador envia una **nota de voz en frances** preguntando:

> "Bonjour, qu'est-ce que l'IMV, s'il vous plait?"

**Respuesta esperada (~10 segundos):**

1. Whisper (o Gemini) transcribe el audio del frances.
2. Clara detecta el idioma (frances).
3. Clara busca informacion sobre el IMV en la base de conocimiento.
4. Clara responde **en frances** con texto explicando el tramite.
5. Clara envia un **audio MP3 en frances** con la respuesta.

**Robert dice (frases puente mientras Clara procesa):**

> "Clara esta procesando el audio de Ahmed..."
>
> "Whisper esta transcribiendo del frances..."
>
> "Lo que esta pasando ahora es fascinante: se convierte la voz a texto, detectamos que es frances, buscamos la informacion en nuestra base de conocimiento, generamos la respuesta en frances y la convertimos de nuevo a audio. Todo automatico."

### Paso 2: Nota de voz en frances sobre empadronamiento

**Accion:** El operador envia una **nota de voz en frances** preguntando:

> "Bonjour, je viens d'arriver en Espagne et j'ai besoin de savoir comment faire le empadronamiento, s'il vous plait."

**Respuesta esperada (~10 segundos):**

1. Transcripcion del audio en frances.
2. Deteccion de idioma: frances.
3. Busqueda de informacion sobre empadronamiento en la KB.
4. Respuesta **en frances** con texto explicando el empadronamiento con analogias culturales.
5. Audio MP3 en frances (`ahmed_fr.mp3`).

**Robert dice (al llegar la respuesta):**

> "Y ahi esta. Ahmed tiene su respuesta en frances. Sin traductor. Sin intermediarios."

**Ruta tecnica:** `POST /webhook` -> Twilio media -> descarga OGG -> transcripcion (Whisper/Gemini) -> detect lang (`fr`) -> KB lookup (`empadronamiento`) -> Gemini genera respuesta en frances -> audio MP3 -> Twilio REST -> WhatsApp.

---

## 6. Las 8 Entradas de Cache

A continuacion se documentan las 8 entradas del archivo `data/cache/demo_cache.json` con sus triggers exactos y respuestas esperadas.

### 6.1 — `saludo_es` (Saludo en espanol)

| Campo | Valor |
|---|---|
| **ID** | `saludo_es` |
| **Triggers** | `hola`, `buenos dias`, `buenas tardes`, `buenas noches`, `que tal`, `hey` |
| **Modo** | `any_keyword` |
| **Idioma** | `es` |
| **Audio** | No (null) |
| **Respuesta** | Saludo de bienvenida de Clara con lista de 3 tramites disponibles (IMV, Empadronamiento, Tarjeta Sanitaria) |

### 6.2 — `imv_es` (Ingreso Minimo Vital en espanol)

| Campo | Valor |
|---|---|
| **ID** | `imv_es` |
| **Triggers** | `imv`, `ingreso minimo`, `ingreso minimo`, `renta minima`, `ayuda economica` |
| **Modo** | `any_keyword` |
| **Idioma** | `es` |
| **Audio** | `imv_es.mp3` |
| **Respuesta** | Explicacion completa del IMV: que es, requisitos (edad, residencia, vulnerabilidad, demandante de empleo), cuantia (604,21 EUR/mes), como solicitarlo (online, presencial, telefono 900 20 22 22), enlace oficial |

### 6.3 — `empadronamiento_es` (Empadronamiento en espanol)

| Campo | Valor |
|---|---|
| **ID** | `empadronamiento_es` |
| **Triggers** | `empadron`, `empadronamiento`, `padron`, `padron`, `registrar domicilio`, `certificado padron` |
| **Modo** | `any_keyword` |
| **Idioma** | `es` |
| **Audio** | `empadronamiento_es.mp3` |
| **Respuesta** | Explicacion del empadronamiento: que es, documentos necesarios (DNI/NIE/pasaporte, contrato), como hacerlo en Madrid (cita en madrid.es/padron, OAC), dato clave: es un DERECHO, telefono 010 / 915 298 210, enlace oficial |

### 6.4 — `tarjeta_sanitaria_es` (Tarjeta Sanitaria en espanol)

| Campo | Valor |
|---|---|
| **ID** | `tarjeta_sanitaria_es` |
| **Triggers** | `tarjeta sanitaria`, `tarjeta salud`, `sanidad`, `medico`, `medico`, `seguro medico`, `asistencia sanitaria` |
| **Modo** | `any_keyword` |
| **Idioma** | `es` |
| **Audio** | `tarjeta_es.mp3` |
| **Respuesta** | Explicacion de la tarjeta sanitaria: quien tiene derecho (empadronados, residentes, sin recursos), documentos necesarios (empadronamiento reciente, DNI/NIE, num. Seguridad Social), como solicitarla en Madrid (Centro de Salud), telefono 900 102 112, enlace oficial |

### 6.5 — `saludo_fr` (Saludo en frances)

| Campo | Valor |
|---|---|
| **ID** | `saludo_fr` |
| **Triggers** | `bonjour`, `salut`, `bonsoir`, `allo`, `coucou` |
| **Modo** | `any_keyword` |
| **Idioma** | `fr` |
| **Audio** | No (null) |
| **Respuesta** | Saludo de bienvenida de Clara en frances con lista de 3 tramites: IMV (aide financiere), Empadronamiento (inscription a la mairie), Tarjeta Sanitaria (acces aux soins) |

### 6.6 — `ahmed_empadronamiento_fr` (Empadronamiento en frances)

| Campo | Valor |
|---|---|
| **ID** | `ahmed_empadronamiento_fr` |
| **Triggers** | `inscrire`, `mairie`, `empadron`, `enregistr`, `domicile`, `commune`, `inscription` |
| **Modo** | `any_keyword` |
| **Idioma** | `fr` |
| **Audio** | `ahmed_fr.mp3` |
| **Respuesta** | Explicacion del empadronamiento en frances: que es (inscription obligatoire a la mairie), documentos necesarios (passeport, contrat de location), como hacerlo en Madrid (rendez-vous sur madrid.es/padron, OAC), dato clave: c'est un DROIT, telefono 010 / 915 298 210, enlace oficial |

### 6.7 — `fatima_tarjeta_fr` (Tarjeta Sanitaria en frances)

| Campo | Valor |
|---|---|
| **ID** | `fatima_tarjeta_fr` |
| **Triggers** | `carte sante`, `carte sanitaire`, `medecin`, `docteur`, `sante`, `securite sociale`, `soins` |
| **Modo** | `any_keyword` |
| **Idioma** | `fr` |
| **Audio** | `fatima_fr.mp3` |
| **Respuesta** | Explicacion de la tarjeta sanitaria en frances: quien tiene derecho (inscrits au padron, permis de sejour, sans ressources), documentos necesarios (certificat d'empadronamiento, passeport, num. Securite Sociale), como solicitarla en Madrid (Centre de Sante), telefono 900 102 112, enlace oficial |

### 6.8 — `maria_carta_vision` (Imagen / documento)

| Campo | Valor |
|---|---|
| **ID** | `maria_carta_vision` |
| **Triggers** | (ninguno — se activa con cualquier imagen cuando `DEMO_MODE=true`) |
| **Modo** | `image_demo` |
| **Idioma** | `any` |
| **Audio** | `maria_es.mp3` |
| **Respuesta** | Analisis de imagen/documento oficial: identificacion del tipo de carta, recomendaciones segun el tipo (carta de Seguridad Social, notificacion del Ayuntamiento), sugerencia de acudir a orientacion social gratuita, telefono 012 |

---

## 7. Guion 6-8 Minutos (con Evidence Checkpoints)

> **Formato de cues:** Cada seccion incluye MUESTRO (lo visible en pantalla), DIGO (lo que dice Robert) y EVIDENCIA (comando + archivo que respalda el claim). Guion completo con analisis de conceptos en [FASE3-DEMO-OPS-REAL.md](../01-phases/FASE3-DEMO-OPS-REAL.md).

### t=0:00 — Apertura: El Problema (1 minuto)

**MUESTRO** → Slide con datos: "3.2M inmigrantes en Espana. 40% no completa tramites por barrera idiomatica."

**DIGO** →

> "En Espana hay 3 coma 2 millones de inmigrantes. El 40 por ciento no consigue completar tramites basicos como el empadronamiento o la solicitud del Ingreso Minimo Vital. El problema no es que no quieran. Es que la informacion esta en espanol tecnico, repartida en 20 webs distintas, y las colas telefonicas duran horas."
>
> "Hoy os voy a presentar a Clara. Un asistente de WhatsApp que habla el idioma del usuario, entiende voz y texto, y da informacion verificada sobre tramites reales. Nada de descargar apps. Solo WhatsApp."

**EVIDENCIA** → INE 2025 poblacion inmigrante. KB oficial: `data/tramites/imv.json`, `data/tramites/empadronamiento.json`, `data/tramites/tarjeta_sanitaria.json`.

### t=1:00 — Presentacion de Clara (30 segundos)

**MUESTRO** → Slide de arquitectura simplificado o transicion directa al movil.

**DIGO** →

> "Clara funciona asi de simple: tu abres WhatsApp, le escribes o le hablas, y Clara te responde en tu idioma con informacion verificada. Veamoslo en vivo."

**EVIDENCIA** → Diagrama de secuencia en `docs/02-architecture/ARCHITECTURE.md` seccion 2.

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
- Cache entry `imv_es` con audio `imv_es.mp3` en `data/cache/demo_cache.json`.
- Audio accesible: `curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3` → HTTP 200 + `Content-Type: audio/mpeg`.
- KB oficial: `data/tramites/imv.json`.

### t=3:30 — Transicion a Ahmed (30 segundos)

**MUESTRO** → Misma pantalla de WhatsApp.

**DIGO** →

> "Pero Clara no solo habla espanol. Pensad ahora en Ahmed. Acaba de llegar de Marruecos. Habla frances. Necesita empadronarse para poder acceder a la sanidad publica, pero no sabe por donde empezar. No va a escribir en espanol. Le envia una nota de voz en frances a Clara."

**EVIDENCIA** → Clara soporta 2 idiomas (ES, FR). Deteccion automatica: `src/core/skills/detect_lang.py`.

### t=4:00 — WOW 2: Ahmed envia audio en frances (2 minutos)

**MUESTRO** → Operador envia nota de voz en frances preguntando por el empadronamiento.

**DIGO** (frases puente mientras Clara procesa, ~10 segundos) →

> "Ahora Clara esta haciendo algo fascinante. Primero, convierte la voz de Ahmed a texto. Luego detecta que esta hablando en frances. Busca informacion sobre el empadronamiento en nuestra base de conocimiento verificada. Genera una respuesta en frances. Y la convierte de nuevo a audio. Todo automatico."

**MUESTRO** → Clara responde con texto en frances + audio MP3 en frances.

**DIGO** →

> "Y ahi esta. Ahmed tiene su respuesta en frances. Le explica que es el empadronamiento, que documentos necesita, donde ir en Madrid, y que es un derecho — incluso sin contrato de alquiler. Sin traductor. Sin intermediarios. Solo WhatsApp y Clara."

**EVIDENCIA** →
- Pipeline: 11 skills en `src/core/pipeline.py`.
- Cache entry `ahmed_empadronamiento_fr` con audio `ahmed_fr.mp3`.
- Ruta: webhook → fetch_media → transcribe (Gemini) → detect_lang → cache_match → send_response.
- 96 tests verifican el pipeline: `pytest tests/ -v --tb=short`.

### t=6:00 — Evidencia Tecnica (1 minuto)

**MUESTRO** → Terminal o slide con datos clave.

**DIGO** →

> "Esto no es un mockup. Es un sistema real desplegado en produccion."
>
> "96 tests automatizados. Un pipeline de 11 skills. 9 feature flags. Base de conocimiento con informacion verificada del gobierno. Deploy en Render con health check cada 14 minutos. Coste por consulta: 0 coma 2 centimos en cache, 1 centimo con IA."

**EVIDENCIA** →

| Claim | Comando | Output esperado |
|-------|---------|-----------------|
| 96 tests | `pytest tests/ -v --tb=short` | 96 passed (91+5 xpassed) |
| 11 skills | `ls src/core/skills/*.py` | 11 archivos |
| 9 flags | Ver `src/core/config.py` | 9 flags |
| KB oficial | `ls data/tramites/` | 3 JSON |
| Deploy activo | `curl -s https://civicaid-voice.onrender.com/health` | `"status": "ok"` |
| 8 cache | health output | `"cache_entries": 8` |
| Lint limpio | `ruff check src/ tests/ --select E,F,W --ignore E501` | 0 errores |

### t=7:00 — Cierre: Impacto y Vision (1 minuto)

**MUESTRO** → Slide final o pantalla de WhatsApp con las conversaciones visibles.

**DIGO** →

> "Hoy Clara cubre 3 tramites en 2 idiomas. Pero la arquitectura esta disenada para escalar. Manana pueden ser cientos de tramites en decenas de idiomas."
>
> "Lo mas importante: Clara funciona en el canal que ya usan mil millones de personas. No hay que instalar nada. No hay que aprender nada. Solo abrir WhatsApp y preguntar."
>
> "Para Maria, eso significa entender una carta del gobierno. Para Ahmed, eso significa poder empadronarse y acceder a la sanidad publica. Para millones de personas vulnerables, eso significa dejar de estar solas frente a la burocracia."
>
> "Esto es Clara. Gracias."

**EVIDENCIA** →
- WhatsApp: 95% penetracion en Espana.
- 3 tramites: `data/tramites/`. 2 idiomas: ES, FR.
- Arquitectura stateless: `docs/02-architecture/ARCHITECTURE.md`.
- Repo completo: codigo + tests + docs + deploy verificable.

---

## 8. Procedimientos de Fallback

### Fallback A: Render en Cold Start (respuesta > 5 segundos)

| Senal | Accion |
|---|---|
| La primera peticion tarda mas de 5 segundos | Robert dice: "El servidor se esta despertando, esto pasa con el plan gratuito de Render. En produccion usariamos always-on." |
| Si tarda mas de 15 segundos | Cambiar a capturas de pantalla pre-preparadas en el portatil |
| Si no responde en 30 segundos | Reproducir `demo-backup.mp4` |

**Prevencion:** Hacer `curl /health` **5 minutos antes** de la demo y otra vez **1 minuto antes**. Verificar que el cron de 14 minutos esta activo.

### Fallback B: Transcripcion falla (WOW 2 no transcribe)

| Senal | Accion |
|---|---|
| No hay respuesta tras 15 segundos del audio | Robert dice: "Parece que la transcripcion esta ocupada. Dejadme mostraros lo que normalmente devuelve." |
| Mostrar respuesta pre-grabada | Abrir captura de pantalla con la conversacion completa en frances |
| Reproducir audio de backup | Reproducir MP3 pre-grabado con la respuesta en frances |

### Fallback C: Audio no se reproduce en WhatsApp

| Senal | Accion |
|---|---|
| El MP3 no carga o no suena | Robert dice: "El audio esta ahi pero a veces WhatsApp tarda en cachearlo. Lo importante es el texto." |
| Leer la respuesta en voz alta | Robert lee el texto de la respuesta que si aparece en pantalla |

### Fallback D: WiFi del venue falla

| Senal | Accion |
|---|---|
| Sin conexion WiFi | Cambiar a datos moviles (hotspot) |
| Sin datos moviles | Reproducir `demo-backup.mp4` directamente |

---

## 9. Troubleshooting

### Render no responde al health check

```bash
curl -s https://civicaid-voice.onrender.com/health
# Si no responde o devuelve error:
# 1. Verificar en Render Dashboard -> Logs si hay errores
# 2. Si 502: la app no arranco. Verificar que WHISPER_ON=false si hay problemas de RAM
# 3. Si timeout: el servicio esta dormido. Esperar 15-30 segundos para el cold start
```

### WhatsApp no envia mensajes

1. Verificar que el sandbox esta activo: enviar "join <codigo>" al +1 415 523 8886.
2. Verificar que el numero de telefono esta registrado en el sandbox de Twilio.
3. Verificar en Twilio Console -> Messaging -> que el webhook URL apunta a `https://civicaid-voice.onrender.com/webhook`.

### La respuesta de cache no llega

1. Verificar que `DEMO_MODE=true` en las variables de entorno de Render.
2. Verificar que `demo_cache.json` tiene las 8 entradas: el health check debe mostrar `"cache_entries": 8`.
3. Revisar los logs de Render buscando `[CACHE] HIT` o `[CACHE] MISS`.

### El audio MP3 no se reproduce

```bash
# Verificar que el archivo es accesible:
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
# Esperado: HTTP/2 200 con Content-Type: audio/mpeg

# Si 404: los MP3 no estan en la imagen Docker. Verificar que data/cache/ contiene los 6 archivos .mp3
# Si 200 pero no suena: verificar Content-Type es audio/mpeg
# Verificar que AUDIO_BASE_URL coincide con la URL real de Render
```

### La transcripcion de audio tarda demasiado

- Si usa Whisper: puede consumir hasta 12 segundos. Esto es normal.
- Si tarda mas de 15 segundos: considerar desactivar Whisper (`WHISPER_ON=false`) y usar solo texto.
- En Render free tier (512 MB RAM), Whisper puede ser inestable. Gemini transcription es alternativa con menos consumo de RAM.

---

## 10. Puntos de Conversacion Post-Demo

Despues de los 6-8 minutos, Robert puede expandir sobre estos temas si hay preguntas:

### Tecnologia

- **Gemini** (Google) como LLM para generar respuestas contextuales y transcripcion de audio.
- **Whisper** (OpenAI) como alternativa para speech-to-text multilingue — soporta 99 idiomas.
- **Twilio** como gateway de WhatsApp — escalable a millones de usuarios.
- **Base de conocimiento verificada** — informacion oficial de fuentes gubernamentales.
- **gTTS** para generacion de audio en tiempo real en cache miss.

### Impacto Social

- **40% de inmigrantes** en Espana no completan tramites por barrera idiomatica.
- Clara reduce esta barrera a **cero** — responde en el idioma del usuario.
- WhatsApp tiene **penetracion del 95%** en Espana — no hay que instalar nada.
- El audio es clave para personas con **baja alfabetizacion digital**.

### Escalabilidad

- Hoy: 3 tramites (IMV, Empadronamiento, Tarjeta Sanitaria). KB extensible a cientos.
- 2 idiomas (espanol, frances). Ampliable a mas.
- Coste por consulta: ~$0.002 (cache hit) a ~$0.01 (LLM + transcripcion).
- Arquitectura stateless — escala horizontalmente.
- Plan: integrar con APIs oficiales de la administracion publica.

### Modelo de Negocio

- B2G (Business to Government): ayuntamientos pagan por usuario atendido.
- ONG/cooperacion: funding de programas de integracion.
- Freemium: consultas basicas gratis, tramites asistidos premium.

---

## 11. Contactos de Emergencia

| Rol | Persona | Responsabilidad |
|---|---|---|
| Presentador | Robert | Narrar y cubrir tiempos de espera con frases puente |
| Operador movil | (asignado) | Enviar mensajes de WhatsApp a tiempo |
| Backup tecnico | Marcos | Monitorizar logs de Render durante la demo |
| Video backup | Daniel | Tener video listo para reproducir si todo falla |
| Coordinacion | Andrea | Slides y soporte general |

---

## Como se verifica

1. Ejecutar los comandos de verificacion de la seccion 1 — todos deben devolver los resultados esperados.
2. Ejecutar el cronograma de preparacion completo (seccion 3) al menos una vez como ensayo.
3. Verificar que las 8 entradas de cache responden correctamente enviando cada trigger por WhatsApp.

## Referencias

- [Fase 3 — Demo en Vivo (conceptos, guion, riesgos)](../01-phases/FASE3-DEMO-OPS-REAL.md)
- [Resumen Ejecutivo / 1-Pager](../00-EXECUTIVE-SUMMARY.md)
- [Arquitectura](../02-architecture/ARCHITECTURE.md)
- [Implementacion MVP (Fase 1)](../01-phases/FASE1-IMPLEMENTACION-MVP.md)
- [Plan Maestro (Fase 0)](../01-phases/FASE0-PLAN-MAESTRO-FINAL.md)
- [Runbook Fase 2 (Deploy y Operaciones)](./RUNBOOK-PHASE2.md)
- [Guia de Twilio](../06-integrations/TWILIO-SETUP-GUIDE.md)
- [Deploy en Render](../05-ops/RENDER-DEPLOY.md)

---

> **Regla de oro:** Si algo falla, nunca parar. Siempre hay un fallback. La demo debe fluir sin importar que pase con la tecnologia.
