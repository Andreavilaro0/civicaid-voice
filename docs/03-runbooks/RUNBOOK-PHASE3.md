# RUNBOOK FASE 3 — Incidentes Demo "Clara"

> **Resumen en una linea:** Playbook de incidentes para la demo: si falla X hago Y. Cubre los 8 escenarios mas probables con diagnostico, remediacion y tiempos de recuperacion.

## Que es

Runbook de respuesta a incidentes especifico para el dia de la demo del hackathon. Cada escenario documenta: senal de alerta, diagnostico rapido, accion correctiva y tiempo estimado de recuperacion.

## Para quien

- **Robert** (presentador): saber que decir al jurado si algo falla
- **Marcos** (ops): ejecutar remediaciones en tiempo real
- **Equipo completo**: referencia rapida durante la demo

## Que incluye

- 8 escenarios de incidente con diagnostico y remediacion
- Comandos exactos para cada accion
- Tiempos estimados de recuperacion
- Checklist de smoke test post-deploy

## Que NO incluye

- Procedimientos de deploy (ver `docs/05-ops/RENDER-DEPLOY.md`)
- Guion de la demo (ver `docs/03-runbooks/RUNBOOK-DEMO.md`)
- Configuracion de Twilio (ver `docs/06-integrations/TWILIO-SETUP-GUIDE.md`)

---

## Smoke Test Post-Deploy

Ejecutar despues de cada deploy y antes de la demo. Los 5 checks deben pasar.

```bash
# 1. Health check
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
# Esperado: "status":"ok", "cache_entries":8, "twilio_configured":true, "gemini_key_set":true

# 2. Audio MP3 accesible
curl -s -o /dev/null -w "%{http_code}" https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
# Esperado: 200

# 3. Webhook protegido (403 sin firma Twilio)
curl -s -o /dev/null -w "%{http_code}" -X POST https://civicaid-voice.onrender.com/webhook -d "Body=test"
# Esperado: 403

# 4. Tiempo de respuesta < 1s
curl -s -o /dev/null -w "%{time_total}" https://civicaid-voice.onrender.com/health
# Esperado: < 1.0

# 5. Render dashboard muestra "Live"
# Verificar visualmente en dashboard.render.com
```

**Criterio:** 5/5 checks PASS = smoke test aprobado. Si alguno falla, consultar el escenario correspondiente abajo.

---

## INC-01: Render en cold start (servicio dormido)

| Campo | Detalle |
|---|---|
| **Senal** | `curl /health` tarda > 5 segundos o devuelve timeout |
| **Causa** | El servicio se apago por inactividad (>15 min sin peticiones) |
| **Impacto** | Primera peticion de la demo tarda 15-30 segundos |

**Diagnostico:**

```bash
time curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

Si `time_total > 5s`, el servicio estaba dormido.

**Remediacion:**

```bash
# Opcion 1: Despertar con curl (esperar hasta 30s)
curl -s --max-time 60 https://civicaid-voice.onrender.com/health | python3 -m json.tool

# Opcion 2: Manual deploy desde Render dashboard
# Dashboard > servicio > Manual Deploy > Deploy latest commit
```

**Prevencion:** Verificar que cron-job.org esta activo (cada 14 min). Ejecutar `curl /health` 5 minutos antes de la demo.

**Tiempo de recuperacion:** 15-30 segundos (cold start) o 3-5 minutos (redeploy).

**Frase puente (Robert):** "El servidor se esta despertando, esto pasa con el plan gratuito de Render. En produccion usariamos always-on."

---

## INC-02: Health check devuelve 502

| Campo | Detalle |
|---|---|
| **Senal** | `curl /health` devuelve HTTP 502 |
| **Causa** | La app no arranco (error de Python, OOM kill, crash de Gunicorn) |
| **Impacto** | Servicio completamente caido |

**Diagnostico:**

```bash
# Verificar HTTP code
curl -s -o /dev/null -w "%{http_code}" https://civicaid-voice.onrender.com/health

# Revisar logs en Render Dashboard > servicio > Logs
# Buscar: "MemoryError", "Killed", "ModuleNotFoundError", "ImportError"
```

**Remediacion:**

1. Si OOM: verificar que `WHISPER_ON=false` en Render Environment
2. Si ImportError: trigger manual deploy (Dashboard > Manual Deploy > Clear build cache & deploy)
3. Si persiste: verificar que `requirements.txt` no cambio recientemente

```bash
# Verificar variables de entorno criticas en Render Dashboard:
# WHISPER_ON=false (obligatorio en free tier)
# DEMO_MODE=true
# LLM_LIVE=true
```

**Tiempo de recuperacion:** 3-5 minutos (redeploy).

---

## INC-03: Webhook no recibe mensajes de WhatsApp

| Campo | Detalle |
|---|---|
| **Senal** | Se envia mensaje por WhatsApp pero Clara no responde |
| **Causa** | URL de webhook incorrecta en Twilio, o servicio caido |
| **Impacto** | Demo WOW 1 y WOW 2 no funcionan |

**Diagnostico:**

```bash
# 1. Verificar que el servicio esta vivo
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool

# 2. Probar webhook directamente (esperado: 403 por falta de firma)
curl -s -o /dev/null -w "%{http_code}" -X POST \
  https://civicaid-voice.onrender.com/webhook \
  -d "Body=test" -d "From=whatsapp:+34600000000" -d "NumMedia=0"

# 3. Verificar URL en Twilio Console:
# console.twilio.com > Messaging > Try it out > Send a WhatsApp message > Sandbox settings
# URL debe ser: https://civicaid-voice.onrender.com/webhook
# Metodo debe ser: POST
```

**Remediacion:**

1. Corregir URL en Twilio Console si es incorrecta
2. Si 403 en el test anterior: webhook funciona (la firma falta porque es curl, no Twilio)
3. Si 502/timeout: resolver INC-01 o INC-02 primero
4. Verificar que el telefono de demo tiene el sandbox activo: enviar `join <codigo>` al +1 415 523 8886

**Tiempo de recuperacion:** 1-2 minutos (correccion de URL) o depende de INC-01/INC-02.

---

## INC-04: Audio MP3 no se reproduce en WhatsApp

| Campo | Detalle |
|---|---|
| **Senal** | El texto llega pero el audio no se reproduce o no aparece |
| **Causa** | Archivo MP3 inaccesible, Content-Type incorrecto, o AUDIO_BASE_URL mal configurada |
| **Impacto** | Demo sin audio (texto sigue funcionando) |

**Diagnostico:**

```bash
# 1. Verificar accesibilidad del archivo
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
# Esperado: HTTP/2 200, Content-Type: audio/mpeg

# 2. Verificar todos los MP3
for f in imv_es empadronamiento_es tarjeta_es ahmed_fr fatima_fr maria_es; do
  echo -n "$f.mp3: "
  curl -s -o /dev/null -w "%{http_code}" https://civicaid-voice.onrender.com/static/cache/${f}.mp3
  echo
done

# 3. Verificar AUDIO_BASE_URL en Render Dashboard > Environment
# Debe ser: https://civicaid-voice.onrender.com/static/cache
```

**Remediacion:**

1. Si 404: los MP3 no estan en la imagen Docker. Verificar que `data/cache/*.mp3` existe en el repo y hacer redeploy
2. Si Content-Type incorrecto: verificar `src/routes/static_files.py`
3. Si AUDIO_BASE_URL incorrecta: corregir en Render Dashboard y reiniciar servicio

**Fallback:** Robert lee el texto en voz alta: "El audio esta ahi pero a veces WhatsApp tarda en cachearlo. Lo importante es el texto."

**Tiempo de recuperacion:** 3-5 minutos (redeploy) o inmediato (fallback verbal).

---

## INC-05: Transcripcion de audio falla (WOW 2)

| Campo | Detalle |
|---|---|
| **Senal** | Se envia nota de voz en frances pero no hay respuesta despues de 15 segundos |
| **Causa** | Timeout de transcripcion, Gemini API rate limit, o formato de audio incompatible |
| **Impacto** | WOW 2 (flujo audio frances) no funciona |

**Diagnostico:**

```bash
# 1. Verificar que Gemini key esta configurada
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
# gemini_key_set debe ser true

# 2. Revisar logs de Render buscando errores de transcripcion
# Dashboard > servicio > Logs > buscar "transcri" o "gemini" o "ERROR"
```

**Remediacion:**

1. Si `gemini_key_set: false`: agregar GEMINI_API_KEY en Render Dashboard > Environment
2. Si rate limit: esperar 60 segundos e intentar de nuevo
3. Si timeout persistente: verificar LLM_TIMEOUT >= 6 en variables de entorno

**Fallback:** Robert dice: "Parece que la transcripcion esta ocupada. Dejadme mostraros lo que normalmente devuelve." Mostrar captura de pantalla pre-preparada con la conversacion en frances.

**Tiempo de recuperacion:** 60 segundos (rate limit) o inmediato (fallback visual).

---

## INC-06: WiFi del venue falla

| Campo | Detalle |
|---|---|
| **Senal** | Sin conexion a internet en el portatil o movil de demo |
| **Causa** | WiFi del venue saturado o caido |
| **Impacto** | Demo completamente offline |

**Remediacion:**

1. Cambiar a datos moviles (hotspot desde telefono personal)
2. Si no hay datos: reproducir `demo-backup.mp4` desde el portatil
3. Si no hay video: usar capturas de pantalla pre-preparadas

**Prevencion:** Antes de la demo, verificar velocidad del WiFi. Tener hotspot preparado como backup.

**Tiempo de recuperacion:** 30 segundos (hotspot) o inmediato (video backup).

---

## INC-07: Sandbox de WhatsApp desconectado

| Campo | Detalle |
|---|---|
| **Senal** | WhatsApp muestra "mensaje enviado" pero Clara no responde, y el webhook no recibe POST |
| **Causa** | El sandbox de Twilio expira tras 72 horas de inactividad |
| **Impacto** | Mensajes no llegan al webhook |

**Diagnostico:**

Verificar en Twilio Console > Messaging > Try it out > Send a WhatsApp message > que el numero de demo aparezca como "connected".

**Remediacion:**

```
# Desde el telefono de demo, enviar al +1 415 523 8886:
join <codigo-sandbox>

# Esperar confirmacion de Twilio: "You are now connected to sandbox..."
# Reenviar el mensaje de demo
```

**Tiempo de recuperacion:** 30 segundos.

---

## INC-08: Cache miss inesperado (respuesta lenta o generica)

| Campo | Detalle |
|---|---|
| **Senal** | Clara responde pero la respuesta es generica o tarda > 5 segundos |
| **Causa** | El texto enviado no coincide con los triggers del cache, o DEMO_MODE=false |
| **Impacto** | Respuesta mas lenta y menos optimizada que la esperada |

**Diagnostico:**

```bash
# 1. Verificar que DEMO_MODE esta activo
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
# demo_mode debe ser true, cache_entries debe ser 8

# 2. Verificar los triggers exactos del cache
# Triggers WOW 1: "Hola", "Que es el IMV?", "Empadronamiento"
# Triggers WOW 2: audio en frances sobre empadronamiento
```

**Remediacion:**

1. Usar los triggers exactos documentados en RUNBOOK-DEMO.md seccion 6
2. Si `demo_mode: false`: activar en Render Dashboard > Environment > DEMO_MODE=true y reiniciar
3. Si `cache_entries: 0`: redeploy (archivos de cache no incluidos en la imagen)

**Prevencion:** Ensayar con los textos exactos antes de la demo.

**Tiempo de recuperacion:** Inmediato (corregir texto) o 3-5 minutos (redeploy si cache falta).

---

## Matriz de escalamiento

| Severidad | Descripcion | Accion | Responsable |
|---|---|---|---|
| **P1 Critico** | Servicio completamente caido (502, timeout) | Redeploy + fallback video | Marcos |
| **P2 Alto** | Webhook o Twilio no conectan | Corregir config + reconectar sandbox | Marcos |
| **P3 Medio** | Audio no se reproduce o transcripcion falla | Fallback verbal + capturas | Robert |
| **P4 Bajo** | Cache miss, respuesta generica | Corregir texto trigger | Operador movil |

---

## Checklist 5 minutos antes de la demo

- [ ] `curl /health` devuelve 200 con `cache_entries: 8`
- [ ] Audio MP3 accesible: `curl -I .../static/cache/imv_es.mp3` devuelve 200
- [ ] Sandbox WhatsApp activo (enviar mensaje de prueba y recibir respuesta)
- [ ] Video backup `demo-backup.mp4` listo en portatil
- [ ] Hotspot movil preparado como backup de WiFi
- [ ] Cron-job.org muestra ejecuciones recientes con HTTP 200

---

## Como se verifica

1. Ejecutar el smoke test post-deploy (5 checks, todos PASS).
2. Simular al menos 2 escenarios de incidente (INC-01 y INC-03) antes de la demo real.
3. Verificar que todos los fallbacks estan preparados (video, capturas, hotspot).

## Referencias

- [Runbook Demo](./RUNBOOK-DEMO.md)
- [Runbook Fase 2](./RUNBOOK-PHASE2.md)
- [Deploy en Render](../05-ops/RENDER-DEPLOY.md)
- [Guia de Twilio](../06-integrations/TWILIO-SETUP-GUIDE.md)
- [Evidencia Fase 3](../07-evidence/PHASE-3-EVIDENCE.md)
