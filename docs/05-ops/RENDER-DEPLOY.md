# RENDER DEPLOY — Guía de Despliegue en Render

> **Servicio:** Web Service (Docker)
> **Plan:** Free (con limitaciones de cold start)
> **URL producción:** https://civicaid-voice.onrender.com
> **Tiempo de build estimado:** 3–5 minutos

---

## 1. Prerequisitos

Antes de comenzar el despliegue, verificar:

| Requisito | Detalle |
|---|---|
| Repositorio en GitHub | Repo `civicaid-voice` con `Dockerfile` en la raíz |
| Cuenta en Render | Registrarse en [render.com](https://render.com) (plan gratuito) |
| Cuenta en Twilio | Con acceso al Sandbox de WhatsApp |
| API Key de Gemini | Obtenida desde [Google AI Studio](https://aistudio.google.com) |
| Dockerfile funcional | Verificar que `docker build .` funciona localmente |

### Estructura esperada del repositorio

```
civicaid-voice/
├── Dockerfile
├── render.yaml
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── webhook.py
│   └── ...
├── tests/
└── ...
```

---

## 2. Despliegue Paso a Paso

### Paso 2.1 — Crear Web Service en Render

1. Iniciar sesión en [dashboard.render.com](https://dashboard.render.com).
2. Hacer clic en **"New +"** → **"Web Service"**.
3. Seleccionar **"Build and deploy from a Git repository"**.
4. Conectar la cuenta de GitHub si no está conectada.
5. Buscar y seleccionar el repositorio `civicaid-voice`.
6. Configurar:
   - **Name:** `civicaid-voice`
   - **Region:** `Frankfurt (EU)` (más cercano a España)
   - **Branch:** `main`
   - **Runtime:** `Docker`
   - **Instance Type:** `Free`

### Paso 2.2 — Configurar Variables de Entorno

En la sección **"Environment Variables"**, agregar **todas** las siguientes variables:

| Variable | Valor | Descripción |
|---|---|---|
| `TWILIO_ACCOUNT_SID` | `AC...` | SID de la cuenta de Twilio |
| `TWILIO_AUTH_TOKEN` | `...` | Token de autenticación de Twilio |
| `TWILIO_SANDBOX_FROM` | `whatsapp:+14155238886` | Número del sandbox de WhatsApp |
| `GEMINI_API_KEY` | `AIza...` | API key de Google Gemini |
| `DEMO_MODE` | `true` | Activa el modo demo con respuestas de caché |
| `LLM_LIVE` | `true` | Permite llamadas en tiempo real al LLM |
| `WHISPER_ON` | `true` | Activa la transcripción con Whisper |
| `LLM_TIMEOUT` | `6` | Timeout en segundos para llamadas al LLM |
| `WHISPER_TIMEOUT` | `12` | Timeout en segundos para transcripción Whisper |
| `FLASK_ENV` | `production` | Entorno de Flask |
| `LOG_LEVEL` | `INFO` | Nivel de logging |
| `AUDIO_BASE_URL` | `https://civicaid-voice.onrender.com/static/cache` | URL base para servir archivos de audio |

**IMPORTANTE:** No usar comillas alrededor de los valores en Render. El dashboard las añade automáticamente.

### Paso 2.3 — Desplegar

1. Hacer clic en **"Create Web Service"**.
2. Render clonará el repositorio y ejecutará el `Dockerfile`.
3. Esperar a que el build termine (barra de progreso verde).
4. El log de build mostrará cada paso del Dockerfile.
5. Cuando termine, el estado cambiará a **"Live"**.

**Tiempo estimado de build:** 3–5 minutos en la primera vez (descarga de dependencias + modelo Whisper base).

---

## 3. Verificar el Despliegue

### Health Check

Ejecutar desde la terminal:

```bash
curl https://civicaid-voice.onrender.com/health
```

**Respuesta esperada (JSON):**

```json
{
  "status": "healthy",
  "components": {
    "cache": "ok",
    "kb": "ok",
    "whisper": "ok",
    "llm": "ok",
    "twilio": "ok"
  },
  "version": "1.0.0",
  "demo_mode": true,
  "uptime_seconds": 42
}
```

Verificar que **todos los componentes** devuelven `"ok"`. Si alguno falla, revisar la sección de Troubleshooting.

### Verificar que los audios se sirven correctamente

```bash
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
```

**Respuesta esperada:** `HTTP/1.1 200 OK` con `Content-Type: audio/mpeg`.

---

## 4. Configurar Webhook de Twilio

Para que WhatsApp envíe mensajes a Clara, configurar el webhook en Twilio:

1. Ir a la [consola de Twilio](https://console.twilio.com).
2. Navegar a **Messaging** → **Try it out** → **Send a WhatsApp message**.
3. En la sección **Sandbox Configuration**, configurar:
   - **When a message comes in:** `https://civicaid-voice.onrender.com/webhook`
   - **Method:** `POST`
   - **Status callback URL:** _(dejar vacío)_
4. Hacer clic en **"Save"**.

### Verificar la conexión

1. Enviar un mensaje desde WhatsApp al número del sandbox.
2. En el dashboard de Render, ir a **"Logs"** y verificar que aparece el POST entrante.
3. Verificar que la respuesta llega a WhatsApp.

---

## 5. Configurar Cron-Job para Evitar Cold Starts

El plan gratuito de Render apaga el servicio tras 15 minutos de inactividad. Para mantenerlo activo, configurar un ping periódico:

1. Ir a [cron-job.org](https://cron-job.org) y crear una cuenta gratuita.
2. Crear un nuevo cron job:
   - **Title:** `CivicAid Health Ping`
   - **URL:** `https://civicaid-voice.onrender.com/health`
   - **Schedule:** Cada **8 minutos** (dentro del límite de 15 min de Render)
   - **Method:** `GET`
   - **Timeout:** `30` segundos
3. Activar el cron job.

**Alternativa con crontab local (solo para desarrollo):**

```bash
# Añadir al crontab: crontab -e
*/8 * * * * curl -s https://civicaid-voice.onrender.com/health > /dev/null 2>&1
```

**Nota:** El cron-job.org es preferible porque funciona 24/7 sin depender de un ordenador encendido.

---

## 6. Blueprint render.yaml

El archivo `render.yaml` permite despliegue declarativo con Infrastructure as Code:

```yaml
services:
  - type: web
    name: civicaid-voice
    runtime: docker
    repo: https://github.com/<org>/civicaid-voice
    branch: main
    region: frankfurt
    plan: free
    healthCheckPath: /health
    envVars:
      - key: TWILIO_ACCOUNT_SID
        sync: false
      - key: TWILIO_AUTH_TOKEN
        sync: false
      - key: TWILIO_SANDBOX_FROM
        value: "whatsapp:+14155238886"
      - key: GEMINI_API_KEY
        sync: false
      - key: DEMO_MODE
        value: "true"
      - key: LLM_LIVE
        value: "true"
      - key: WHISPER_ON
        value: "true"
      - key: LLM_TIMEOUT
        value: "6"
      - key: WHISPER_TIMEOUT
        value: "12"
      - key: FLASK_ENV
        value: "production"
      - key: LOG_LEVEL
        value: "INFO"
      - key: AUDIO_BASE_URL
        value: "https://civicaid-voice.onrender.com/static/cache"
```

**Campos clave:**

- `sync: false` — Indica que el valor se configura manualmente en el dashboard (secretos). No se sube al repositorio.
- `healthCheckPath: /health` — Render verifica automáticamente que el servicio responde antes de dirigir tráfico.
- `region: frankfurt` — Centro de datos más cercano a España para menor latencia.
- `plan: free` — Plan gratuito con las limitaciones de cold start.

### Desplegar con Blueprint

1. Subir `render.yaml` a la raíz del repositorio.
2. En Render Dashboard → **"Blueprints"** → **"New Blueprint Instance"**.
3. Seleccionar el repositorio.
4. Render leerá el `render.yaml` y creará el servicio automáticamente.
5. Rellenar los valores de las variables marcadas con `sync: false`.

---

## 7. Troubleshooting

### Problema: Cold Start (latencia de 15–30 segundos en primera petición)

**Causa:** El plan gratuito de Render apaga los servicios inactivos tras 15 minutos.

**Solución:**
- Configurar el cron job de la sección 5.
- Antes de la demo, hacer `curl /health` al menos 5 minutos antes.
- Para producción, considerar el plan Starter ($7/mes) que mantiene el servicio siempre activo.

### Problema: Build Falla — Out of Memory

**Causa:** Whisper base requiere ~150MB de RAM para cargar el modelo. El plan gratuito tiene 512MB.

**Solución:**
- Usar el modelo `whisper-base` (no `whisper-small` ni `whisper-medium`).
- Verificar que el Dockerfile no instala dependencias innecesarias.
- Usar multi-stage build para reducir el tamaño de la imagen.

```dockerfile
# Ejemplo de multi-stage build
FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:10000"]
```

### Problema: Build Falla — Dockerfile Error

**Causa:** Error de sintaxis o dependencia faltante en el Dockerfile.

**Solución:**
- Verificar que el build funciona localmente: `docker build -t civicaid-test .`
- Revisar los logs de build en Render Dashboard → servicio → **"Events"**.
- Errores comunes:
  - `requirements.txt` faltante → Verificar que está en la raíz.
  - Puerto incorrecto → Render espera que la app escuche en `$PORT` (default 10000).

### Problema: Twilio No Envía al Webhook

**Causa:** URL del webhook mal configurada o el servicio no responde.

**Solución:**
1. Verificar que la URL en Twilio es exactamente: `https://civicaid-voice.onrender.com/webhook`
2. Verificar que el método es `POST` (no GET).
3. Probar manualmente con curl:

```bash
curl -X POST https://civicaid-voice.onrender.com/webhook \
  -d "Body=Hola" \
  -d "From=whatsapp:+34600000000" \
  -d "NumMedia=0"
```

4. Revisar los logs de Render para ver si llega el POST.

### Problema: Audios No Se Reproducen en WhatsApp

**Causa:** Twilio no puede acceder a la URL del audio o el formato es incorrecto.

**Solución:**
- Verificar que `AUDIO_BASE_URL` apunta a la URL correcta de Render.
- Verificar que los archivos MP3 están en `static/cache/` dentro del contenedor.
- Los archivos deben ser MP3 válidos (no OGG ni WAV).
- Verificar con: `curl -I https://civicaid-voice.onrender.com/static/cache/<archivo>.mp3`

### Problema: Whisper No Transcribe

**Causa:** Modelo no descargado o memoria insuficiente.

**Solución:**
- Verificar que el Dockerfile descarga el modelo durante el build.
- Revisar logs: buscar errores de `torch` o `whisper`.
- Verificar que `WHISPER_ON=true` está configurado.
- El modelo base ocupa ~150MB en RAM. Verificar uso de memoria en Render Dashboard → **"Metrics"**.

---

## 8. Checklist de Despliegue Completo

| # | Paso | Estado |
|---|---|---|
| 1 | Crear Web Service en Render | ☐ |
| 2 | Configurar todas las variables de entorno (12 vars) | ☐ |
| 3 | Build completado sin errores | ☐ |
| 4 | `curl /health` devuelve 200 con todos los componentes OK | ☐ |
| 5 | Webhook configurado en Twilio Console | ☐ |
| 6 | Cron job activo en cron-job.org (cada 8 min) | ☐ |
| 7 | Enviar "Que es el IMV?" por WhatsApp y recibir respuesta | ☐ |
| 8 | Verificar que el audio MP3 se reproduce en WhatsApp | ☐ |

---

> **Nota:** Para la demo del hackathon, despertar Render al menos 5 minutos antes y verificar con `curl /health`. Tener siempre preparado el video de backup por si hay problemas de red.
