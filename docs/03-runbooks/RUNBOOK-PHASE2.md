# RUNBOOK FASE 2 — Deploy, Verificacion y Warm-up

> **Resumen en una linea:** Procedimientos operativos para configurar el entorno local, construir Docker, desplegar en Render, verificar el deploy, configurar el cron warm-up de 14 minutos y resolver problemas comunes.

## Que es

Este runbook contiene los procedimientos operativos completos para llevar Clara desde el entorno de desarrollo local hasta un deploy funcional en Render, incluyendo la verificacion post-deploy y la configuracion del cron para evitar cold starts.

## Para quien

- **Marcos** (deploy, Twilio, infraestructura)
- **Robert** (verificacion, feature flags)
- Cualquier miembro del equipo (Andrea, Lucas, Daniel) que necesite levantar el entorno

## Que incluye

- Setup del entorno de desarrollo local
- Construccion y prueba con Docker
- Deploy en Render con todas las variables de entorno
- Comandos de verificacion post-deploy
- Configuracion del cron warm-up (cada 14 minutos)
- Guia de troubleshooting

## Que NO incluye

- Guion de la demo (ver `docs/03-runbooks/RUNBOOK-DEMO.md`)
- Configuracion detallada de Twilio (ver `docs/06-integrations/TWILIO-SETUP-GUIDE.md`)
- Arquitectura del pipeline (ver `docs/02-architecture/ARCHITECTURE.md`)

---

## 1. Setup del Entorno Local

### 1.1 Pre-requisitos

| Requisito | Version | Comando de verificacion |
|-----------|---------|------------------------|
| Python | 3.11+ | `python3 --version` |
| pip | ultima version | `pip --version` |
| ffmpeg | cualquiera (opcional) | `ffmpeg -version` |
| Docker | 20+ | `docker --version` |
| Git | 2+ | `git --version` |

### 1.2 Pasos de instalacion

```bash
# Paso 1: Clonar el repositorio
git clone <url-del-repo> civicaid-voice
cd civicaid-voice

# Paso 2: Crear archivo .env desde el ejemplo
cp .env.example .env
# Editar .env y rellenar las siguientes variables:
#   TWILIO_ACCOUNT_SID   -> Twilio Console -> Account Info
#   TWILIO_AUTH_TOKEN     -> Twilio Console -> Account Info
#   GEMINI_API_KEY        -> Google AI Studio -> API Keys

# Paso 3: Ejecutar con el script automatizado
bash scripts/run-local.sh
```

El script `run-local.sh` automaticamente:
- Crea un virtualenv (`venv/`) si no existe
- Instala las dependencias de `requirements.txt`
- Inicia Flask en `http://localhost:5000` con hot-reload

### 1.3 Verificar que funciona localmente

```bash
curl http://localhost:5000/health | python3 -m json.tool
```

**Salida esperada:**

```json
{
  "status": "ok",
  "uptime_s": 5,
  "components": {
    "cache_entries": 8,
    "demo_mode": false,
    "llm_live": true
  }
}
```

Puntos clave: `"status": "ok"` y `"cache_entries": 8`.

### 1.4 Ejecutar los tests

```bash
pytest tests/ -v --tb=short
```

**Salida esperada:** 93 tests pasados (88 passed + 5 xpassed).

### 1.5 Ejecutar el linter

```bash
ruff check src/ tests/ --select E,F,W --ignore E501
```

**Salida esperada:** Sin errores criticos.

---

## 2. Docker Build y Test

### 2.1 Construir la imagen

```bash
docker build -t civicaid-voice:test .
```

**Salida esperada:** Build exitoso en ~30 segundos (con cache) o ~2 minutos (sin cache). Un warning sobre JSON args en CMD es cosmetico y puede ignorarse (shell form necesaria para la expansion de `${PORT}`).

### 2.2 Ejecutar el contenedor

```bash
docker run -d --name civicaid-test \
  -p 5000:5000 \
  -e PORT=5000 \
  -e DEMO_MODE=true \
  civicaid-voice:test
```

### 2.3 Verificar el contenedor

```bash
# Health check
curl -s http://localhost:5000/health | python3 -m json.tool
```

**Salida esperada:**

```json
{
  "status": "ok",
  "uptime_s": 8,
  "components": {
    "whisper_loaded": false,
    "whisper_enabled": true,
    "ffmpeg_available": false,
    "gemini_key_set": false,
    "twilio_configured": false,
    "cache_entries": 8,
    "demo_mode": true,
    "llm_live": true
  }
}
```

Sin secrets configurados, `gemini_key_set` y `twilio_configured` son `false` (esperado en test local sin .env).

```bash
# Ver los logs del contenedor
docker logs civicaid-test
```

**Salida esperada en logs:**

```
16:32:53 INFO Loaded 8 cache entries
16:32:53 INFO Starting gunicorn 21.2.0
16:32:53 INFO Listening at: http://0.0.0.0:5000
16:32:53 INFO Using worker: sync
16:32:53 INFO Booting worker with pid: 8
```

No deben aparecer errores (`[ERROR]`).

### 2.4 Limpiar

```bash
docker rm -f civicaid-test
```

---

## 3. Deploy en Render

### 3.1 Crear el servicio via Blueprint

1. Hacer push de `render.yaml` a la rama `main` en GitHub.
2. En [dashboard.render.com](https://dashboard.render.com) -> **Blueprints** -> **New Blueprint Instance**.
3. Seleccionar el repositorio `civicaid-voice`.
4. Render leera `render.yaml` y creara el servicio automaticamente.

### 3.2 Configurar secretos

En el dashboard del servicio -> **Environment** -> agregar valores para las variables marcadas `sync: false`:

| Variable | Donde obtenerlo |
|----------|----------------|
| `TWILIO_ACCOUNT_SID` | [Twilio Console](https://console.twilio.com) -> Account Info |
| `TWILIO_AUTH_TOKEN` | [Twilio Console](https://console.twilio.com) -> Account Info |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com) -> API Keys |

### 3.3 Variables de entorno completas (render.yaml)

Las siguientes 16 variables estan pre-configuradas en `render.yaml`:

| Variable | Valor en Render | Notas |
|----------|----------------|-------|
| `TWILIO_ACCOUNT_SID` | (secreto) | `sync: false` — configurar manualmente en el dashboard |
| `TWILIO_AUTH_TOKEN` | (secreto) | `sync: false` — configurar manualmente en el dashboard |
| `TWILIO_SANDBOX_FROM` | `whatsapp:+14155238886` | Numero sandbox de Twilio |
| `GEMINI_API_KEY` | (secreto) | `sync: false` — configurar manualmente en el dashboard |
| `DEMO_MODE` | `true` | Cache-first, LLM como fallback |
| `LLM_LIVE` | `true` | Gemini habilitado |
| `WHISPER_ON` | `false` | Desactivado en free tier (512 MB RAM) |
| `LLM_TIMEOUT` | `6` | Segundos |
| `WHISPER_TIMEOUT` | `12` | Segundos |
| `FLASK_ENV` | `production` | Sin modo debug |
| `LOG_LEVEL` | `INFO` | Nivel de logging |
| `AUDIO_BASE_URL` | `https://civicaid-voice.onrender.com/static/cache` | URL publica de los MP3 |
| `OBSERVABILITY_ON` | `true` | Logs estructurados |
| `STRUCTURED_OUTPUT_ON` | `false` | Outputs Pydantic (stub) |
| `GUARDRAILS_ON` | `true` | Guardrails de contenido |
| `RAG_ENABLED` | `false` | RAG stub desactivado |

### 3.4 Trigger de deploy

- **Automatico:** Cada push a `main` inicia un deploy automatico.
- **Manual:** Dashboard -> servicio -> **Manual Deploy** -> **Deploy latest commit**.

### 3.5 Mapeo de puertos

- Render asigna `PORT=10000` por defecto.
- El Dockerfile expone el puerto 10000 (`EXPOSE 10000`).
- Gunicorn usa `${PORT:-5000}` para flexibilidad entre local (5000) y Render (10000).
- No requiere configuracion manual de puertos.

---

## 4. Verificacion Post-Deploy

### 4.1 Comandos de verificacion

```bash
# 1. Health check
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

**Salida esperada:**

```json
{
  "status": "ok",
  "uptime_s": 120,
  "components": {
    "whisper_loaded": false,
    "whisper_enabled": false,
    "ffmpeg_available": false,
    "gemini_key_set": true,
    "twilio_configured": true,
    "cache_entries": 8,
    "demo_mode": true,
    "llm_live": true
  }
}
```

```bash
# 2. Verificar que los archivos de audio son accesibles
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
# Esperado: HTTP/2 200 con Content-Type: audio/mpeg
```

```bash
# 3. Verificar que el webhook es accesible (devolvera 200 o 403 por signature validation)
curl -s -o /dev/null -w "%{http_code}" \
  -X POST https://civicaid-voice.onrender.com/webhook \
  -d "Body=test" -d "From=whatsapp:+34600000000" -d "NumMedia=0"
# Esperado: 200 o 403
```

### 4.2 Puntos clave a verificar

| Campo | Valor esperado | Significado |
|-------|---------------|-------------|
| `status` | `"ok"` | La aplicacion arranco correctamente |
| `cache_entries` | `8` | El cache de demo se cargo completo |
| `gemini_key_set` | `true` | La GEMINI_API_KEY esta configurada |
| `twilio_configured` | `true` | SID y Auth Token estan configurados |
| `whisper_enabled` | `false` | Correcto para free tier (ahorra RAM) |
| `demo_mode` | `true` | Modo demo activado para la presentacion |

---

## 5. Cron Warm-up (cada 14 minutos)

### 5.1 Por que es necesario

Render free tier apaga el servicio tras **15 minutos de inactividad** (cold start). El cold start tarda ~15-30 segundos, lo cual es inaceptable para una demo. Un ping periodico cada **14 minutos** mantiene el servicio activo, con un margen de seguridad de 1 minuto.

### 5.2 Opcion A: cron-job.org (recomendado)

1. Crear cuenta gratuita en [cron-job.org](https://cron-job.org).
2. Crear un nuevo cron job:
   - **Title:** `CivicAid Health Ping`
   - **URL:** `https://civicaid-voice.onrender.com/health`
   - **Schedule:** Cada **14 minutos** (`*/14 * * * *`)
   - **Request method:** `GET`
   - **Request timeout:** `30` segundos
   - **Enable job:** Si
   - **Notifications:** Opcional (solo si falla)
3. Guardar y activar.
4. Verificar en el historial de ejecuciones que devuelve HTTP 200.

### 5.3 Opcion B: UptimeRobot

1. Crear cuenta en [UptimeRobot](https://uptimerobot.com) (plan gratuito: 50 monitores).
2. Agregar nuevo monitor:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** `CivicAid Voice`
   - **URL:** `https://civicaid-voice.onrender.com/health`
   - **Monitoring Interval:** `5 minutes` (plan gratuito)
3. Guardar.

### 5.4 Opcion C: crontab local (solo para desarrollo o dia de la demo)

```bash
# Agregar a crontab (ejecutar: crontab -e):
*/14 * * * * curl -s https://civicaid-voice.onrender.com/health > /dev/null 2>&1
```

Solo funciona si la maquina esta encendida. No recomendado para produccion.

### 5.5 Verificar que el warm-up funciona

```bash
# Despues de configurar, esperar 15+ minutos y ejecutar:
time curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

**Resultado esperado:** La respuesta debe llegar en **< 2 segundos** (no 15-30 segundos de cold start).

### 5.6 Checklist pre-demo

- [ ] Cron job activo y con historial de ejecuciones exitosas (200 OK)
- [ ] Verificar con `curl /health` al menos 5 minutos antes de la demo
- [ ] Tener video de backup preparado por si hay problemas de red

---

## 6. Troubleshooting

### 6.1 Docker build falla localmente

```
ERROR: could not find requirements.txt
```

**Solucion:** Verificar que se esta en la raiz del repositorio (`ls Dockerfile` debe mostrar el archivo).

### 6.2 El contenedor no arranca

```bash
docker logs civicaid-test
```

Errores comunes:

| Error | Causa | Solucion |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'src'` | Falta `COPY . .` en Dockerfile | Verificar el Dockerfile |
| `Address already in use` | El puerto ya esta ocupado | Cambiar el puerto: `-p 5050:5050 -e PORT=5050` |
| `MemoryError` o `Killed` | Sin suficiente RAM | Desactivar Whisper: `-e WHISPER_ON=false` |

### 6.3 /health devuelve 502 en Render

**Causa:** La aplicacion no arranco correctamente o se quedo sin memoria.

**Diagnostico:**

1. Dashboard -> servicio -> **Logs** -> buscar errores de Python/gunicorn.
2. Dashboard -> servicio -> **Metrics** -> verificar RAM (limite 512 MB en free tier).

**Solucion:**

- Verificar que `WHISPER_ON=false` (Whisper consume mucha RAM).
- Verificar que `--workers 1` en el CMD (no usar mas workers en free tier).
- Si persiste: hacer **Manual Deploy** -> **Clear build cache & deploy**.

### 6.4 Deploy funciona pero el webhook no responde

1. Verificar la URL exacta en Twilio: `https://civicaid-voice.onrender.com/webhook`
2. Verificar que el metodo configurado es `POST`.
3. Render puede tardar hasta 30 segundos en cold start — configurar cron warm-up (seccion 5).
4. Si los logs muestran `403`: es la validacion de firma de Twilio funcionando (normal si se prueba con curl directo).

### 6.5 Cold start demasiado lento

- Configurar cron warm-up cada 14 minutos (seccion 5).
- Antes de la demo: ejecutar `curl /health` al menos 5 minutos antes.
- Si es critico: considerar plan Starter de Render ($7/mes) para always-on.

### 6.6 Los audios no se reproducen

```bash
# Verificar accesibilidad del archivo:
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
```

| Resultado | Causa | Solucion |
|-----------|-------|----------|
| HTTP 404 | Los MP3 no estan en la imagen Docker | Verificar que `data/cache/` contiene los 6 archivos .mp3 |
| HTTP 200 pero no suena | Content-Type incorrecto | Verificar que Content-Type es `audio/mpeg` |
| Funciona en curl pero no en WhatsApp | `AUDIO_BASE_URL` incorrecto | Verificar que coincide con la URL real de Render |

### 6.7 Tests fallan en CI pero pasan localmente

- Verificar que CI usa la misma version de Python (3.11).
- Verificar que las dependencias de `requirements.txt` estan actualizadas.
- Revisar si algun test depende de variables de entorno no configuradas en CI.

---

## Registro de Evidencia

### Docker Build (2026-02-12)

```
$ docker build -t civicaid-voice:test .
#1 [internal] load build definition from Dockerfile
#4 [1/5] FROM docker.io/library/python:3.11-slim
#6 [4/5] RUN pip install --no-cache-dir -r requirements.txt (CACHED)
#9 [5/5] COPY . . (CACHED)
#10 exporting to image — naming to docker.io/library/civicaid-voice:test done
BUILD SUCCESS
```

### Health Check del Contenedor (2026-02-12)

```
$ docker run -d --name civicaid-test -p 5050:5050 -e PORT=5050 -e DEMO_MODE=true civicaid-voice:test
$ curl -s http://localhost:5050/health | python3 -m json.tool
{
    "components": {
        "cache_entries": 8,
        "demo_mode": true,
        "ffmpeg_available": false,
        "gemini_key_set": false,
        "llm_live": true,
        "twilio_configured": false,
        "whisper_enabled": true,
        "whisper_loaded": false
    },
    "status": "ok",
    "uptime_s": 8
}
HEALTH CHECK: PASS (status=ok, cache_entries=8)
```

### Logs del Contenedor (2026-02-12)

```
16:32:53 INFO Loaded 8 cache entries
16:32:53 INFO Whisper model loaded (enabled=True)
16:32:53 INFO Observability enabled (OTEL_ENDPOINT=none)
[2026-02-12 16:32:53 +0000] [7] [INFO] Starting gunicorn 21.2.0
[2026-02-12 16:32:53 +0000] [7] [INFO] Listening at: http://0.0.0.0:5050 (7)
[2026-02-12 16:32:53 +0000] [7] [INFO] Using worker: sync
[2026-02-12 16:32:53 +0000] [8] [INFO] Booting worker with pid: 8
SIN ERRORES
```

### Validacion del Pipeline de CI

Archivo CI (`.github/workflows/ci.yml`) verificado:
- pytest se ejecuta sin hacks de PYTHONPATH (usa imports con prefijo `src.`)
- Paso de Docker build incluido como job separado
- Paso de ruff lint con los flags estandar del proyecto

---

## Como se verifica

1. Ejecutar `docker build` y `docker run` segun las secciones 2.1-2.3 — health check debe devolver `"status": "ok"` y `"cache_entries": 8`.
2. Tras el deploy en Render, ejecutar los 3 comandos de la seccion 4.1 — todos deben devolver los resultados esperados.
3. Tras configurar el cron, esperar 15+ minutos y verificar que `curl /health` responde en menos de 2 segundos (seccion 5.5).

## Referencias

- [Arquitectura](../02-architecture/ARCHITECTURE.md)
- [Deploy en Render](../05-ops/RENDER-DEPLOY.md)
- [Guia de Twilio](../06-integrations/TWILIO-SETUP-GUIDE.md)
- [Runbook de la Demo](./RUNBOOK-DEMO.md)
- [Observabilidad](../05-ops/OBSERVABILITY-QUICKSTART.md)
- [Estado de Fases](../07-evidence/PHASE-STATUS.md)
