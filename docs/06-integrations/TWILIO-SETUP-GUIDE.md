# Guia de Configuracion de Twilio — CivicAid Voice / Clara

> **Resumen en una linea:** Configuracion completa de Twilio para conectar Clara con WhatsApp, desde la creacion de cuenta hasta la validacion de firma y troubleshooting.

## Que es

Twilio es la plataforma de comunicaciones en la nube que conecta Clara con WhatsApp. Actua como intermediario: recibe los mensajes que los usuarios envian por WhatsApp y los reenvia al webhook de Clara (`POST /webhook`). Clara responde con un ACK inmediato via TwiML y luego envia la respuesta completa por la API REST de Twilio.

## Para quien

- Desarrolladores que necesitan configurar la conexion WhatsApp por primera vez.
- El equipo de operaciones que despliega Clara en Render.
- Cualquier persona que necesite diagnosticar problemas de mensajeria.

## Que incluye

- Creacion de cuenta Twilio paso a paso.
- Configuracion del WhatsApp Sandbox.
- Variables de entorno necesarias.
- Validacion de firma (RequestValidator).
- Comandos curl para pruebas con payloads de texto y audio.
- Diagnostico de errores comunes (401, 403, timeout).

## Que NO incluye

- Configuracion de numeros de telefono de produccion (solo sandbox).
- Integracion con otros canales (SMS, voz).
- Facturacion de Twilio.

---

## 1. Que es Twilio y para que lo usamos

Twilio proporciona la infraestructura para que Clara se comunique con los usuarios a traves de WhatsApp. El flujo completo es:

```
Usuario (WhatsApp)
  |
  v
Twilio Cloud
  |
  v
POST /webhook (Flask)
  |-- Valida firma Twilio (cabecera X-Twilio-Signature)
  |-- Parsea: Body, From, NumMedia, MediaUrl0, MediaContentType0
  |-- Devuelve TwiML XML ACK inmediatamente (<1s, HTTP 200)
  |
  +-- Hilo de fondo:
        |-- Cache match -> HIT -> API REST Twilio -> Usuario
        |-- Cache match -> MISS -> KB + Gemini LLM -> API REST Twilio -> Usuario
```

**Puntos clave del diseno:**

- El webhook devuelve un XML TwiML `<Response><Message>` de forma inmediata para que Twilio reciba su ACK dentro de los 15 segundos permitidos.
- La respuesta real se calcula en un hilo de fondo y se envia mediante la API REST de Twilio (`client.messages.create`).
- El usuario ve dos mensajes: (1) el ACK ("Un momento...") y (2) la respuesta completa.
- El envio REST incluye timeout de 10 segundos y reintento automatico sin media en caso de fallo.

---

## 2. Crear cuenta Twilio (paso a paso)

1. Ir a [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio) y crear una cuenta gratuita.
2. Verificar el numero de telefono durante el registro.
3. Navegar a **Console > Account Info** y anotar:
   - **Account SID** (empieza con `AC...`, 34 caracteres).
   - **Auth Token** (hacer clic para revelarlo).

> **Importante:** La cuenta de prueba es suficiente para el sandbox de WhatsApp. No se necesita tarjeta de credito para las funcionalidades de sandbox.

---

## 3. Configurar WhatsApp Sandbox

### 3.1 Unirse al sandbox

1. En la consola de Twilio, ir a **Messaging > Try it out > Send a WhatsApp message**.
2. Seguir las instrucciones para unirse al sandbox:
   - Enviar el codigo de union (por ejemplo, `join <palabra>-<palabra>`) desde WhatsApp al numero del sandbox de Twilio: `+1 415 523 8886`.
3. Verificar que se recibe un mensaje de confirmacion.

> **Nota:** El numero predeterminado del sandbox es `whatsapp:+14155238886`. Ya esta configurado como valor por defecto en la aplicacion.

### 3.2 Configurar la URL del webhook

1. En la consola de Twilio, ir a **Messaging > Try it out > Send a WhatsApp message**.
2. Bajar hasta la seccion **Sandbox Configuration**.
3. Configurar el campo **"WHEN A MESSAGE COMES IN"** con:
   ```
   https://civicaid-voice.onrender.com/webhook
   ```
   - Metodo: **POST**
4. Dejar el campo **"STATUS CALLBACK URL"** vacio.
5. Hacer clic en **"Save"**.

### 3.3 Desarrollo local con ngrok

Para desarrollo local, exponer el servidor Flask con ngrok:

```bash
ngrok http 5000
```

Usar la URL HTTPS de ngrok (por ejemplo, `https://abc123.ngrok-free.app/webhook`) como URL del webhook en Twilio. Recordar actualizarla cada vez que se reinicie ngrok (las URLs gratuitas cambian).

---

## 4. Variables de entorno

Las siguientes variables de Twilio deben estar configuradas. **Nunca subir valores reales al repositorio.**

| Variable | Obligatoria | Descripcion | Ejemplo |
|----------|-------------|-------------|---------|
| `TWILIO_ACCOUNT_SID` | Si | SID de la cuenta Twilio | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_AUTH_TOKEN` | Si | Token de autenticacion de Twilio | (desde la consola de Twilio) |
| `TWILIO_SANDBOX_FROM` | No | Numero del sandbox de WhatsApp | `whatsapp:+14155238886` (por defecto) |
| `AUDIO_BASE_URL` | No | URL base publica para archivos de audio cacheados | `https://civicaid-voice.onrender.com/static/cache` |

### Configuracion local

```bash
cp .env.example .env
# Editar .env y rellenar TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN
```

### Configuracion en Render

En el dashboard de Render para el servicio `civicaid-voice`, anadir `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN` como variables de entorno secretas (marcadas con `sync: false` en `render.yaml`). Las demas variables ya estan configuradas en el archivo `render.yaml`.

---

## 5. Validacion de firma (RequestValidator)

Clara valida que cada peticion al webhook proviene realmente de Twilio mediante la cabecera `X-Twilio-Signature`. Este mecanismo garantiza que nadie pueda enviar peticiones falsas al webhook.

### Como funciona

1. Twilio firma cada peticion HTTP con el **Auth Token** de la cuenta usando HMAC-SHA1.
2. La firma se incluye en la cabecera `X-Twilio-Signature`.
3. El webhook de Clara usa `twilio.request_validator.RequestValidator` para verificar la firma:

```python
# Extracto de src/routes/webhook.py
from twilio.request_validator import RequestValidator

if config.TWILIO_AUTH_TOKEN:
    validator = RequestValidator(config.TWILIO_AUTH_TOKEN)
    signature = request.headers.get("X-Twilio-Signature", "")
    if not validator.validate(request.url, request.form, signature):
        logger.warning("[WEBHOOK] Firma Twilio invalida desde %s", request.remote_addr)
        abort(403)
else:
    logger.warning("[WEBHOOK] Validacion de firma omitida — no hay auth token configurado")
```

### Comportamiento segun entorno

| Entorno | `TWILIO_AUTH_TOKEN` | Comportamiento |
|---------|---------------------|----------------|
| Produccion (Render) | Configurado | Valida firma. Rechaza con 403 si es invalida. |
| Desarrollo local | No configurado | Omite validacion. Registra advertencia en logs. |

> **Importante:** En produccion, `TWILIO_AUTH_TOKEN` debe estar siempre configurado. Sin el, cualquier atacante podria enviar peticiones falsas al webhook.

---

## 6. Testing con curl

### 6.1 Arrancar la aplicacion en local

```bash
bash scripts/run-local.sh
```

El servidor arranca en `http://localhost:5000`.

### 6.2 Verificar el endpoint de salud

```bash
curl http://localhost:5000/health | python3 -m json.tool
```

Respuesta esperada:
```json
{
    "status": "ok",
    "components": {
        "cache_entries": 8,
        "twilio_configured": true,
        ...
    }
}
```

### 6.3 Payload de texto

```bash
curl -X POST http://localhost:5000/webhook \
  -d "Body=Hola&From=whatsapp:+34612345678&To=whatsapp:+14155238886&NumMedia=0" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

Respuesta TwiML esperada:
```xml
<?xml version="1.0" encoding="UTF-8"?><Response><Message>Un momento, estoy procesando tu mensaje... ⏳</Message></Response>
```

### 6.4 Payload de audio

```bash
curl -X POST http://localhost:5000/webhook \
  -d "Body=&From=whatsapp:+34612345678&To=whatsapp:+14155238886&NumMedia=1&MediaUrl0=https://api.twilio.com/2010-04-01/Accounts/ACxxx/Messages/MMxxx/Media/MExxx&MediaContentType0=audio/ogg" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

Respuesta TwiML esperada:
```xml
<?xml version="1.0" encoding="UTF-8"?><Response><Message>Estoy escuchando tu audio... 🎧</Message></Response>
```

### 6.5 Payload de texto en frances

```bash
curl -X POST http://localhost:5000/webhook \
  -d "Body=Bonjour%2C+j%27ai+besoin+d%27aide+avec+l%27IMV&From=whatsapp:+33600000000&NumMedia=0" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### 6.6 Verificar procesamiento en segundo plano

Despues de enviar una peticion al webhook, revisar la salida de la consola:

```
HH:MM:SS INFO [ACK] from=whatsapp:+34612345678 type=text
HH:MM:SS INFO [CACHE] HIT id=imv_es_01 XXms
HH:MM:SS INFO [REST] Sent to=whatsapp:+34612345678 source=cache total=XXms
```

Si la cache falla y el LLM esta activo:
```
HH:MM:SS INFO [ACK] from=whatsapp:+34612345678 type=text
HH:MM:SS INFO [CACHE] MISS XXms
HH:MM:SS INFO [LLM] OK XXms source=gemini
HH:MM:SS INFO [REST] Sent to=whatsapp:+34612345678 source=llm total=XXms
```

### 6.7 Verificacion en produccion

```bash
curl -X POST https://civicaid-voice.onrender.com/webhook \
  -d "Body=Hola&From=whatsapp:+34612345678&NumMedia=0" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

> **Nota:** En produccion con `TWILIO_AUTH_TOKEN` configurado, este curl devolvera **403 Forbidden** porque no incluye una cabecera `X-Twilio-Signature` valida. Este comportamiento es correcto y significa que la validacion de firma funciona.

### 6.8 Test end-to-end por WhatsApp

1. Verificar que se ha unido al sandbox de Twilio (ver seccion 3).
2. Enviar un mensaje de WhatsApp al numero del sandbox: `Hola, necesito ayuda con el IMV`
3. Se deben recibir dos mensajes:
   - **Mensaje 1 (ACK):** "Un momento, estoy procesando tu mensaje..."
   - **Mensaje 2 (Respuesta):** La informacion sobre el IMV

---

## 7. Troubleshooting: errores comunes

### Error 401 — Credenciales invalidas

| Aspecto | Detalle |
|---------|---------|
| **Causa** | `TWILIO_ACCOUNT_SID` o `TWILIO_AUTH_TOKEN` son incorrectos o estan vacios. |
| **Sintoma** | El envio REST falla al intentar `client.messages.create`. El ACK llega pero no la respuesta. |
| **Solucion** | Verificar que los valores coinciden con los de la consola de Twilio (Console > Account Info). Regenerar el token si es necesario. |

### Error 403 — Firma invalida

| Aspecto | Detalle |
|---------|---------|
| **Causa** | La cabecera `X-Twilio-Signature` no coincide o falta. Ocurre al hacer curl directo en produccion. |
| **Sintoma** | El webhook devuelve 403 Forbidden. |
| **Solucion** | Verificar que `TWILIO_AUTH_TOKEN` en el entorno coincide con el de la consola de Twilio. Para pruebas locales sin firma, dejar `TWILIO_AUTH_TOKEN` sin configurar. |

### Timeout — El ACK llega pero no la respuesta

| Aspecto | Detalle |
|---------|---------|
| **Causa** | El hilo de fondo fallo silenciosamente, o las credenciales REST de Twilio son incorrectas. |
| **Sintoma** | El usuario recibe "Un momento..." pero nunca la respuesta completa. |
| **Solucion** | 1. Revisar logs buscando entradas `[ERROR]`. 2. Verificar que `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN` son correctos. 3. Verificar que `TWILIO_SANDBOX_FROM` coincide con el numero del sandbox. 4. Verificar que `DEMO_MODE=true` (solo cache) o `GEMINI_API_KEY` esta configurada (para modo LLM). |

### "No pude entender tu audio" en mensajes de audio

| Aspecto | Detalle |
|---------|---------|
| **Causa** | La transcripcion fallo (problema con Gemini API o fallo al descargar el media). |
| **Sintoma** | El usuario envia audio y recibe un mensaje de error generico. |
| **Solucion** | 1. Revisar logs buscando `[ERROR] stage=transcribe`. 2. Verificar que `GEMINI_API_KEY` es valida. 3. Verificar que las URLs de media de Twilio son accesibles (requieren autenticacion). |

### Sandbox expirado — "Your message could not be delivered"

| Aspecto | Detalle |
|---------|---------|
| **Causa** | Las sesiones del sandbox de WhatsApp expiran tras 72 horas de inactividad. |
| **Sintoma** | WhatsApp muestra error de entrega. |
| **Solucion** | Reenviar el codigo de union al sandbox (ver seccion 3). |

### Render: /webhook no responde

| Aspecto | Detalle |
|---------|---------|
| **Causa** | El servicio puede estar dormido (free tier) o el deploy fallo. |
| **Sintoma** | Timeout o sin respuesta al enviar mensajes. |
| **Solucion** | 1. Probar primero `/health`: `curl https://civicaid-voice.onrender.com/health`. 2. Si falla, revisar el dashboard de Render. 3. El free tier duerme tras 15 minutos de inactividad — la primera peticion puede tardar ~30s en despertar. |

---

## Como se verifica

| # | Verificacion | Comando / Accion |
|---|---|---|
| 1 | Cuenta Twilio creada | SID y Auth Token visibles en Console > Account Info |
| 2 | Sandbox unido | Enviar join code y recibir confirmacion |
| 3 | Webhook configurado | Twilio Console > Sandbox Configuration apunta a URL correcta |
| 4 | Variables de entorno | `curl /health` muestra `twilio_configured: true` |
| 5 | Validacion de firma | curl directo a produccion devuelve 403 |
| 6 | Flujo completo | Enviar "Que es el IMV?" por WhatsApp y recibir 2 mensajes |

## Referencias

- Codigo del webhook: `src/routes/webhook.py`
- Cliente Twilio REST: `src/core/twilio_client.py` y `src/core/skills/send_response.py`
- Configuracion: `src/core/config.py`
- Documentacion Twilio WhatsApp: [https://www.twilio.com/docs/whatsapp](https://www.twilio.com/docs/whatsapp)
- RequestValidator: [https://www.twilio.com/docs/usage/security](https://www.twilio.com/docs/usage/security)
- Deploy en Render: `docs/05-ops/RENDER-DEPLOY.md`
