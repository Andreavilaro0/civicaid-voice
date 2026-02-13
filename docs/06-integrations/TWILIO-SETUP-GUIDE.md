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

- Integracion con otros canales (SMS, voz).
- Facturacion de Twilio.

---

## 0. Analisis de Opciones Twilio WhatsApp (Fase 3)

### 3 opciones evaluadas

| # | Opcion | Descripcion |
|---|--------|-------------|
| A | **WhatsApp Sandbox** | Entorno de pruebas gratuito de Twilio. Numero compartido `+14155238886`. Cada usuario debe enviar `join <code>` manualmente. |
| B | **Numero propio WhatsApp Business** | Numero dedicado vinculado a un WhatsApp Business Profile aprobado por Meta. Requiere cuenta Twilio pagada + aprobacion Meta. |
| C | **Proxy / Middleware** (ej. ngrok + local) | Servidor local expuesto via tunel (ngrok/cloudflare). Twilio apunta al tunel en vez de a Render. |

### Pros y Contras

| Criterio | A: Sandbox | B: Numero propio | C: Proxy/Middleware |
|----------|-----------|-------------------|---------------------|
| **Coste** | Gratis | $15+/mes + coste por mensaje | Gratis (ngrok free) |
| **Setup** | 5 min | 3-5 dias (aprobacion Meta) | 10 min |
| **Limite usuarios** | Sin limite (pero cada uno hace join) | Sin limite, sin join | Solo devs locales |
| **Persistencia** | Session expira 72h inactivo | Permanente | URL cambia al reiniciar ngrok |
| **Demo hackathon** | Perfecto: rapido, funcional, sin coste | Overkill: demasiado tiempo de aprobacion | Fragil: depende de portatil encendido |
| **Audio soportado** | Si (media URLs autenticadas) | Si | Si |
| **Validacion firma** | Si (X-Twilio-Signature) | Si | Si (pero URL cambia) |
| **Produccion real** | No recomendado | Recomendado | No recomendado |

### Decision: Opcion A — WhatsApp Sandbox

**Justificacion:**

1. **Tiempo:** El hackathon tiene horas, no dias. La aprobacion de Meta para numero propio tarda 3-5 dias habiles.
2. **Coste cero:** No requiere tarjeta de credito ni cuenta pagada.
3. **Funcionalidad completa:** Soporta texto, audio, imagenes — exactamente los 3 tipos de input que Clara maneja.
4. **Seguridad demostrable:** La validacion de firma `X-Twilio-Signature` funciona identicamente en sandbox y produccion.
5. **Escalabilidad futura clara:** Migrar de sandbox a numero propio solo requiere cambiar `TWILIO_SANDBOX_FROM` y el webhook URL en la consola — cero cambios de codigo.

> **Nota de produccion:** Para un despliegue real post-hackathon, se recomienda migrar a Opcion B (numero propio) para eliminar el paso de `join` y tener un perfil WhatsApp Business verificado.

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
        logger.warning("[WEBHOOK] Invalid Twilio signature from %s", request.remote_addr)
        abort(403)
else:
    logger.warning("[WEBHOOK] Twilio signature validation skipped — no auth token configured")
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

## 8. Checklist de Verificacion Fase 3 (paso a paso)

### Pre-requisitos

- [ ] Cuenta Twilio creada (Console > Account Info muestra SID y Auth Token)
- [ ] Sandbox WhatsApp activado (seccion 3.1)
- [ ] Al menos 1 telefono unido al sandbox (`join <code>` enviado y confirmado)
- [ ] Deploy en Render activo (`curl https://civicaid-voice.onrender.com/health` → 200 OK)

### Variables de entorno en Render

| Variable | Donde | Verificacion |
|----------|-------|-------------|
| `TWILIO_ACCOUNT_SID` | Render Dashboard > Environment | `sync: false` en render.yaml — valor real solo en Render |
| `TWILIO_AUTH_TOKEN` | Render Dashboard > Environment | `sync: false` en render.yaml — valor real solo en Render |
| `TWILIO_SANDBOX_FROM` | render.yaml | `whatsapp:+14155238886` (valor por defecto sandbox) |
| `GEMINI_API_KEY` | Render Dashboard > Environment | Necesario para transcripcion de audio |
| `AUDIO_BASE_URL` | render.yaml | `https://civicaid-voice.onrender.com/static/cache` |
| `DEMO_MODE` | render.yaml | `true` (cache-first, fallback generico si miss) |

### Verificacion de firma (seguridad)

```bash
# V1: Sin firma → debe devolver 403
curl -s -o /dev/null -w "%{http_code}" \
  -X POST https://civicaid-voice.onrender.com/webhook \
  -d "Body=test&From=whatsapp:+34600000000&NumMedia=0"
# Esperado: 403

# V2: Con firma invalida → debe devolver 403
curl -s -o /dev/null -w "%{http_code}" \
  -X POST https://civicaid-voice.onrender.com/webhook \
  -d "Body=test&From=whatsapp:+34600000000&NumMedia=0" \
  -H "X-Twilio-Signature: invalida123"
# Esperado: 403
```

### Verificacion E2E desde WhatsApp

| # | Paso | Esperado |
|---|------|----------|
| 1 | Enviar `Hola, necesito ayuda con el IMV` | ACK: "Un momento..." + Respuesta con info IMV |
| 2 | Enviar `Que es el empadronamiento?` | ACK + Respuesta con info empadronamiento |
| 3 | Enviar nota de audio preguntando por IMV | ACK: "Estoy escuchando tu audio..." + Transcripcion + Respuesta |
| 4 | Enviar `Bonjour, j'ai besoin d'aide` | ACK + Respuesta en frances |

### Verificacion de logs en Render

Despues de cada mensaje, los logs de Render deben mostrar:

```
INFO [ACK] from=whatsapp:+34... type=text
INFO [CACHE] HIT id=imv_es_01 XXms       # o MISS si no hay cache match
INFO [REST] Sent to=whatsapp:+34... source=cache total=XXms
```

Para audio:
```
INFO [ACK] from=whatsapp:+34... type=audio
INFO [WHISPER] ok=true XXms text="..."
INFO [CACHE] HIT/MISS ...
INFO [REST] Sent to=whatsapp:+34... source=cache/llm total=XXms
```

---

## Como se verifica (resumen)

| # | Verificacion | Comando / Accion |
|---|---|---|
| 1 | Cuenta Twilio creada | SID y Auth Token visibles en Console > Account Info |
| 2 | Sandbox unido | Enviar join code y recibir confirmacion |
| 3 | Webhook configurado | Twilio Console > Sandbox Configuration apunta a URL correcta |
| 4 | Variables de entorno | `curl /health` muestra `twilio_configured: true` |
| 5 | Validacion de firma (sin firma) | `curl -s -o /dev/null -w "%{http_code}" -X POST .../webhook -d "Body=test"` → 403 |
| 6 | Validacion de firma (firma invalida) | curl con `X-Twilio-Signature: fake` → 403 |
| 7 | Flujo texto E2E | Enviar "Que es el IMV?" por WhatsApp → 2 mensajes (ACK + respuesta) |
| 8 | Flujo audio E2E | Enviar nota de voz por WhatsApp → ACK audio + transcripcion + respuesta |
| 9 | Flujo frances | Enviar "Bonjour" → respuesta en frances |

## Referencias

- Codigo del webhook: `src/routes/webhook.py`
- Cliente Twilio REST: `src/core/twilio_client.py` y `src/core/skills/send_response.py`
- Configuracion: `src/core/config.py`
- Documentacion Twilio WhatsApp: [https://www.twilio.com/docs/whatsapp](https://www.twilio.com/docs/whatsapp)
- RequestValidator: [https://www.twilio.com/docs/usage/security](https://www.twilio.com/docs/usage/security)
- Deploy en Render: `docs/05-ops/RENDER-DEPLOY.md`
