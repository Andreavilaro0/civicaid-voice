# Guia de Despliegue en Render — CivicAid Voice / Clara

> **Resumen en una linea:** Guia completa para desplegar Clara en Render con Docker, configurar 16 variables de entorno, verificar el health check y mantener el servicio activo con cron cada 14 minutos.

## Que es

Render es la plataforma de despliegue en la nube donde se ejecuta Clara en produccion. Ofrece un plan gratuito (free tier) con runtime Docker, ideal para prototipos y hackathons. El servicio se despliega automaticamente desde GitHub: cada push a `main` dispara un nuevo build.

## Para quien

- El equipo de DevOps/Infra que gestiona el despliegue.
- Desarrolladores que necesitan verificar que el servicio esta funcionando.
- Cualquier persona que necesite diagnosticar problemas de despliegue o rendimiento.

## Que incluye

- Explicacion del `render.yaml` con las 16 variables de entorno (3 secretas + 13 valores).
- Explicacion del `Dockerfile` linea por linea.
- Pasos de despliegue desde push hasta verificacion.
- Configuracion del health check con 8 componentes.
- Cron warm-up cada 14 minutos para evitar cold starts.
- Diagnostico de problemas comunes.

## Que NO incluye

- Configuracion de dominios personalizados.
- Planes de pago de Render.
- CI/CD con GitHub Actions (ver documentacion de CI por separado).

---

## Datos del servicio

| Clave | Valor |
|---|---|
| **Plataforma** | Render (free tier) |
| **Runtime** | Docker |
| **Region** | Frankfurt (EU) — mas cercano a Espana |
| **URL produccion** | `https://civicaid-voice.onrender.com` |
| **Puerto Render** | 10000 (variable `$PORT`) |
| **Puerto local** | 5000 (fallback) |
| **Tiempo de build** | 3-5 minutos |
| **RAM disponible** | 512 MB (limite del plan gratuito) |
| **Workers Gunicorn** | 1 (por limite de RAM) |
| **Health check** | `GET /health` — 8 componentes |

---

## 1. Que es Render y por que lo usamos

Render es una plataforma de despliegue cloud que permite ejecutar servicios web directamente desde Docker. Se eligio para Clara por las siguientes razones:

- **Plan gratuito:** Sin coste para el hackathon. Incluye Docker runtime, HTTPS automatico y despliegue desde GitHub.
- **Docker runtime:** Clara se despliega como contenedor Docker, garantizando el mismo comportamiento en local y en produccion.
- **Despliegue automatico:** Cada push a la rama `main` dispara un build automatico.
- **HTTPS automatico:** Render proporciona certificado SSL sin configuracion adicional.
- **Region Frankfurt:** Centro de datos mas cercano a Espana para menor latencia.

**Limitaciones del plan gratuito:**
- El servicio se apaga tras 15 minutos de inactividad (cold start).
- 512 MB de RAM — Whisper (modelo base) no cabe con el resto de dependencias.
- Primer arranque tras inactividad puede tardar 15-30 segundos.

---

## 2. Configuracion render.yaml

El archivo `render.yaml` define la infraestructura como codigo (Infrastructure as Code). Contiene 16 variables de entorno: 3 secretas (`sync: false`) y 13 con valores fijos.

### Archivo completo

```yaml
services:
  - type: web
    name: civicaid-voice
    runtime: docker
    region: frankfurt
    plan: free
    dockerfilePath: ./Dockerfile
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
        value: "false"
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
      - key: OBSERVABILITY_ON
        value: "true"
      - key: STRUCTURED_OUTPUT_ON
        value: "false"
      - key: GUARDRAILS_ON
        value: "true"
      - key: RAG_ENABLED
        value: "false"
```

### Explicacion de cada variable

#### Variables secretas (3) — `sync: false`

Estas variables se configuran manualmente en el dashboard de Render. No se suben al repositorio.

| Variable | Descripcion |
|---|---|
| `TWILIO_ACCOUNT_SID` | SID de la cuenta de Twilio (empieza con `AC...`). Necesario para enviar mensajes via API REST. |
| `TWILIO_AUTH_TOKEN` | Token de autenticacion de Twilio. Usado para validar firmas de webhook y para autenticar envios REST. |
| `GEMINI_API_KEY` | Clave API de Google Gemini (empieza con `AIza...`). Necesaria para el LLM y la transcripcion de audio. |

#### Variables con valor fijo (13)

| Variable | Valor | Descripcion |
|---|---|---|
| `TWILIO_SANDBOX_FROM` | `whatsapp:+14155238886` | Numero del sandbox de WhatsApp de Twilio. |
| `DEMO_MODE` | `true` | Activa el modo demo: responde desde cache sin llamar al LLM en caso de cache hit. |
| `LLM_LIVE` | `true` | Permite llamadas al LLM de Gemini cuando hay cache miss. |
| `WHISPER_ON` | `false` | Desactivado en Render free tier porque el modelo Whisper no cabe en 512 MB de RAM. La transcripcion se delega a Gemini. |
| `LLM_TIMEOUT` | `6` | Timeout maximo en segundos para llamadas al LLM de Gemini. |
| `WHISPER_TIMEOUT` | `12` | Timeout maximo en segundos para transcripcion (cuando esta activa). |
| `FLASK_ENV` | `production` | Entorno de Flask. En produccion desactiva el modo debug. |
| `LOG_LEVEL` | `INFO` | Nivel de logging. Opciones: DEBUG, INFO, WARNING, ERROR. |
| `AUDIO_BASE_URL` | `https://civicaid-voice.onrender.com/static/cache` | URL base publica para servir archivos de audio MP3 cacheados. |
| `OBSERVABILITY_ON` | `true` | Habilita observabilidad: logs estructurados con request_id y trazas. |
| `STRUCTURED_OUTPUT_ON` | `false` | Salidas estructuradas Pydantic. Desactivado por defecto. |
| `GUARDRAILS_ON` | `true` | Habilita guardrails de contenido para filtrar respuestas inapropiadas. |
| `RAG_ENABLED` | `false` | Stub de RAG. Desactivado (no implementado en esta fase). |

### Campos clave del servicio

| Campo | Valor | Significado |
|---|---|---|
| `type` | `web` | Servicio web con URL publica |
| `runtime` | `docker` | Usar Dockerfile para el build |
| `region` | `frankfurt` | Centro de datos mas cercano a Espana |
| `plan` | `free` | Plan gratuito con limitaciones de cold start y 512 MB RAM |
| `dockerfilePath` | `./Dockerfile` | Ruta al Dockerfile en la raiz del repo |
| `healthCheckPath` | `/health` | Render verifica que el servicio responde antes de dirigir trafico |

---

## 3. Dockerfile explicado linea por linea

```dockerfile
FROM python:3.11-slim
```
Imagen base de Python 3.11 en su variante slim (minima). Reduce el tamano de la imagen.

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```
`PYTHONDONTWRITEBYTECODE=1`: No genera archivos `.pyc` (innecesarios en contenedor).
`PYTHONUNBUFFERED=1`: Los logs de Python se muestran inmediatamente sin buffering.

```dockerfile
# ffmpeg skipped — Whisper disabled on free tier to stay under 512MB RAM
```
Comentario: No se instala ffmpeg porque Whisper esta desactivado en el plan gratuito para respetar el limite de 512 MB de RAM.

```dockerfile
WORKDIR /app
```
Establece `/app` como directorio de trabajo dentro del contenedor.

```dockerfile
COPY requirements.txt ./
```
Copia solo `requirements.txt` primero para aprovechar la cache de capas de Docker. Si las dependencias no cambian, Docker reutiliza esta capa.

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
Instala las dependencias de Python sin cache de pip (reduce tamano de imagen). No instala `requirements-audio.txt` (que contiene openai-whisper + PyTorch) para respetar el limite de RAM.

```dockerfile
COPY . .
```
Copia todo el codigo fuente de la aplicacion al contenedor.

```dockerfile
EXPOSE 10000
```
Documenta que el contenedor escucha en el puerto 10000 (el puerto que Render asigna por defecto via `$PORT`).

```dockerfile
CMD gunicorn --bind "0.0.0.0:${PORT:-5000}" --timeout 120 --workers 1 --preload "src.app:create_app()"
```
Comando de arranque con Gunicorn:
- `--bind "0.0.0.0:${PORT:-5000}"`: Escucha en el puerto de la variable `$PORT` (10000 en Render) o 5000 como fallback local.
- `--timeout 120`: Timeout de 120 segundos por worker (Whisper puede tardar hasta 12s + LLM 6s + overhead).
- `--workers 1`: Un solo worker por el limite de RAM de 512 MB.
- `--preload`: Carga la aplicacion al arranque (no por peticion).
- `"src.app:create_app()"`: Punto de entrada de la aplicacion Flask.

---

## 4. Pasos de despliegue

### Paso 4.1 — Crear Web Service en Render

1. Iniciar sesion en [dashboard.render.com](https://dashboard.render.com).
2. Hacer clic en **"New +"** > **"Web Service"**.
3. Seleccionar **"Build and deploy from a Git repository"**.
4. Conectar la cuenta de GitHub si no esta conectada.
5. Buscar y seleccionar el repositorio `civicaid-voice`.
6. Configurar:
   - **Name:** `civicaid-voice`
   - **Region:** `Frankfurt (EU)`
   - **Branch:** `main`
   - **Runtime:** `Docker`
   - **Instance Type:** `Free`

### Paso 4.2 — Configurar variables de entorno

En la seccion **"Environment Variables"**, agregar las 3 variables secretas:

| Variable | Donde obtenerla |
|---|---|
| `TWILIO_ACCOUNT_SID` | Consola Twilio > Account Info |
| `TWILIO_AUTH_TOKEN` | Consola Twilio > Account Info (clic para revelar) |
| `GEMINI_API_KEY` | Google AI Studio > API Keys |

**Importante:** No poner comillas alrededor de los valores en el dashboard de Render. Las anade automaticamente.

Las demas 13 variables ya estan definidas en `render.yaml` y se aplican automaticamente.

### Paso 4.3 — Desplegar

1. Hacer clic en **"Create Web Service"**.
2. Render clonara el repositorio y ejecutara el `Dockerfile`.
3. Esperar a que el build termine (barra de progreso verde).
4. El log de build mostrara cada paso del Dockerfile.
5. Cuando termine, el estado cambiara a **"Live"**.

**Tiempo estimado de build:** 3-5 minutos en la primera vez (descarga de dependencias).

### Paso 4.4 — Verificar con /health

```bash
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

Si el health check devuelve 200 con `"status": "ok"`, el despliegue fue exitoso.

### Despliegue con Blueprint (alternativa)

1. Subir `render.yaml` a la raiz del repositorio.
2. En Render Dashboard > **"Blueprints"** > **"New Blueprint Instance"**.
3. Seleccionar el repositorio.
4. Render leera el `render.yaml` y creara el servicio automaticamente.
5. Rellenar los valores de las 3 variables secretas (`sync: false`).

---

## 5. Puerto: EXPOSE 10000 (Render) / fallback 5000 (local)

Render asigna el puerto `10000` mediante la variable de entorno `$PORT`. El Dockerfile y Gunicorn estan configurados para respetar esta variable:

| Entorno | Puerto | Mecanismo |
|---|---|---|
| **Render (produccion)** | 10000 | `$PORT=10000` (configurado por Render automaticamente) |
| **Local (desarrollo)** | 5000 | Fallback `${PORT:-5000}` cuando `$PORT` no esta definida |
| **Docker local** | 5000 o custom | `docker run -p 5000:5000 -e PORT=5000 ...` |

> **Importante:** Si se cambia el puerto manualmente, asegurarse de que `EXPOSE` en el Dockerfile y el `--bind` de Gunicorn coincidan. Si no, Render no detectara que el servicio esta escuchando y lo marcara como fallido.

---

## 6. Health check: GET /health

Render utiliza el endpoint `GET /health` para verificar que el servicio esta operativo antes de dirigir trafico. La respuesta incluye 8 componentes que resumen el estado del sistema.

### Comando

```bash
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

### Respuesta esperada

```json
{
    "status": "ok",
    "uptime_s": 42,
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

### Explicacion de los 8 componentes

| Componente | Valor esperado (Render) | Descripcion |
|---|---|---|
| `whisper_loaded` | `false` | Modelo Whisper cargado en memoria. False en Render (desactivado). |
| `whisper_enabled` | `false` | Flag `WHISPER_ON`. False en Render free tier (512 MB RAM). |
| `ffmpeg_available` | `false` | ffmpeg instalado. False en Render (no se instala sin Whisper). |
| `gemini_key_set` | `true` | `GEMINI_API_KEY` configurada. Debe ser true. |
| `twilio_configured` | `true` | `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN` configurados. Debe ser true. |
| `cache_entries` | `8` | Numero de entradas en `demo_cache.json`. Siempre 8. |
| `demo_mode` | `true` | `DEMO_MODE` activo. Respuestas cache-first. |
| `llm_live` | `true` | `LLM_LIVE` activo. Permite Gemini en cache miss. |

### Verificacion de archivos de audio

```bash
curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3
```

Respuesta esperada: `HTTP/1.1 200 OK` con `Content-Type: audio/mpeg`.

---

## 7. Cron warm-up: cada 14 minutos

El plan gratuito de Render apaga el servicio tras 15 minutos de inactividad. Para mantenerlo activo durante la demo, se configura un ping periodico cada 14 minutos (dentro del margen de 15 minutos).

### Configuracion con cron-job.org (recomendado)

1. Ir a [cron-job.org](https://cron-job.org) y crear una cuenta gratuita.
2. Crear un nuevo cron job:
   - **Titulo:** `CivicAid Health Ping`
   - **URL:** `https://civicaid-voice.onrender.com/health`
   - **Intervalo:** Cada **14 minutos**
   - **Metodo:** `GET`
   - **Timeout:** `30` segundos
3. Activar el cron job.

### Alternativa con crontab local (solo desarrollo)

```bash
# Anadir al crontab: crontab -e
*/14 * * * * curl -s https://civicaid-voice.onrender.com/health > /dev/null 2>&1
```

> **Nota:** cron-job.org es preferible porque funciona 24/7 sin depender de un ordenador encendido.

### Antes de la demo

Independientemente del cron, ejecutar manualmente al menos 5 minutos antes de la demo:

```bash
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

Esto garantiza que el servicio esta despierto y caliente.

---

## 8. Troubleshooting

### Build falla — Out of Memory

| Aspecto | Detalle |
|---------|---------|
| **Causa** | Las dependencias superan el limite de 512 MB de RAM del plan gratuito. |
| **Sintoma** | El build falla con error de memoria o el servicio se reinicia constantemente (OOM kill). |
| **Solucion** | Verificar que `WHISPER_ON=false` y que no se instala `requirements-audio.txt` (contiene PyTorch + Whisper). Usar solo `requirements.txt` base. Verificar que el Dockerfile no instala ffmpeg ni dependencias innecesarias. |

### Build falla — Error en Dockerfile

| Aspecto | Detalle |
|---------|---------|
| **Causa** | Error de sintaxis, dependencia faltante o archivo no copiado. |
| **Sintoma** | El build se detiene en un paso especifico con mensaje de error. |
| **Solucion** | 1. Verificar que el build funciona localmente: `docker build -t civicaid-test .` 2. Revisar los logs de build en Render Dashboard > servicio > **"Events"**. 3. Verificar que `requirements.txt` esta en la raiz del repositorio. |

### Port mismatch — El servicio no responde

| Aspecto | Detalle |
|---------|---------|
| **Causa** | La aplicacion no escucha en el puerto que Render espera (`$PORT`, por defecto 10000). |
| **Sintoma** | El servicio aparece como "Live" pero `/health` no responde o devuelve timeout. |
| **Solucion** | Verificar que el CMD de Gunicorn usa `${PORT:-5000}` y que el `EXPOSE` del Dockerfile es 10000. Render configura `$PORT=10000` automaticamente. No hardcodear el puerto. |

### Limite de 512 MB — Servicio se reinicia

| Aspecto | Detalle |
|---------|---------|
| **Causa** | El uso de memoria excede los 512 MB disponibles en el plan gratuito. |
| **Sintoma** | El servicio arranca pero se reinicia periodicamente (visible en "Events"). |
| **Solucion** | 1. Verificar que `WHISPER_ON=false`. 2. Usar `--workers 1` en Gunicorn (ya configurado). 3. Revisar Render Dashboard > **"Metrics"** para ver el uso de memoria. 4. Si es necesario, considerar el plan Starter ($7/mes) con mas recursos. |

### Cold start — Latencia de 15-30 segundos

| Aspecto | Detalle |
|---------|---------|
| **Causa** | El servicio estaba dormido por inactividad (>15 min sin peticiones). |
| **Sintoma** | La primera peticion tarda entre 15 y 30 segundos en responder. |
| **Solucion** | 1. Configurar el cron job de la seccion 7 (cada 14 minutos). 2. Antes de la demo, hacer `curl /health` al menos 5 minutos antes. 3. Para produccion, el plan Starter mantiene el servicio siempre activo. |

### Twilio no envia al webhook

| Aspecto | Detalle |
|---------|---------|
| **Causa** | URL del webhook mal configurada o el servicio no responde. |
| **Sintoma** | Los mensajes de WhatsApp no llegan a Clara. |
| **Solucion** | 1. Verificar que la URL en Twilio es exactamente: `https://civicaid-voice.onrender.com/webhook`. 2. Verificar que el metodo es `POST`. 3. Probar con: `curl -X POST https://civicaid-voice.onrender.com/webhook -d "Body=Hola&From=whatsapp:+34600000000&NumMedia=0"` 4. Revisar logs de Render para ver si llega el POST. |

### Audios no se reproducen en WhatsApp

| Aspecto | Detalle |
|---------|---------|
| **Causa** | Twilio no puede acceder a la URL del audio o el formato es incorrecto. |
| **Sintoma** | El mensaje de texto llega pero el audio no se reproduce. |
| **Solucion** | 1. Verificar que `AUDIO_BASE_URL` apunta a la URL correcta de Render. 2. Verificar los archivos MP3 con: `curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3` 3. Los archivos deben ser MP3 validos (no OGG ni WAV). |

---

## Checklist de despliegue completo

| # | Paso | Verificacion |
|---|---|---|
| 1 | Crear Web Service en Render | Servicio visible en dashboard |
| 2 | Configurar 16 variables de entorno (3 secretas + 13 valores) | Todas las variables presentes |
| 3 | Build completado sin errores | Estado "Live" en dashboard |
| 4 | `curl /health` devuelve 200 con 8 componentes OK | `cache_entries: 8`, `twilio_configured: true` |
| 5 | Webhook configurado en Twilio Console | URL: `/webhook`, metodo: POST |
| 6 | Cron job activo en cron-job.org (cada 14 min) | Job en estado activo |
| 7 | Enviar "Que es el IMV?" por WhatsApp y recibir respuesta | 2 mensajes recibidos (ACK + respuesta) |
| 8 | Audio MP3 accesible y reproducible | `curl -I .../imv_es.mp3` devuelve 200 |

---

## Como se verifica

| # | Verificacion | Comando |
|---|---|---|
| 1 | Servicio desplegado | Dashboard Render muestra "Live" |
| 2 | Health check OK | `curl https://civicaid-voice.onrender.com/health` devuelve 200 |
| 3 | 8 componentes correctos | JSON con `cache_entries: 8`, `twilio_configured: true`, `gemini_key_set: true` |
| 4 | Audio accesible | `curl -I https://civicaid-voice.onrender.com/static/cache/imv_es.mp3` devuelve 200 |
| 5 | Cron activo | cron-job.org muestra ejecuciones exitosas cada 14 min |
| 6 | Flujo WhatsApp completo | Enviar mensaje y recibir ACK + respuesta |

## Referencias

- Archivo de infraestructura: `render.yaml`
- Dockerfile: `Dockerfile`
- Configuracion de la app: `src/core/config.py`
- Health check: `src/routes/health.py`
- Guia de Twilio: `docs/06-integrations/TWILIO-SETUP-GUIDE.md`
- Render Docs: [https://render.com/docs](https://render.com/docs)
- Render Blueprint Spec: [https://render.com/docs/blueprint-spec](https://render.com/docs/blueprint-spec)
