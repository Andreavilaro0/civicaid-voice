# RUNBOOK — Demo "Clara" WhatsApp Chatbot

> **Duración total:** 3 minutos
> **Momentos WOW:** 2
> **Presentador:** Robert
> **Operador técnico:** Miembro del equipo con móvil listo
>
> **Documentos relacionados:**
> [Arquitectura](../02-architecture/ARCHITECTURE.md) |
> [Implementación MVP (Fase 1)](../01-phases/FASE1-IMPLEMENTACION-MVP.md) |
> [Plan Maestro (Fase 0)](../01-phases/FASE0-PLAN-MAESTRO-FINAL.md)

---

## 1. Checklist Pre-Demo

Verificar **todos** los puntos antes de subir al escenario. Sin excepciones.

| # | Verificación | Comando / Acción | Estado |
|---|---|---|---|
| 1 | Render despierto (no cold start) | `curl https://civicaid-voice.onrender.com/health` → 200 OK | ☐ |
| 2 | WhatsApp Sandbox unido | Enviar "join <código>" al +1 415 523 8886 desde el móvil de demo | ☐ |
| 3 | Móvil cargado >80% | Verificar batería del dispositivo de demo | ☐ |
| 4 | Vídeo de backup cargado | Tener `demo-backup.mp4` en el portátil, listo para reproducir | ☐ |
| 5 | Feature flags configurados | Verificar en Render Dashboard → Environment | ☐ |
| 6 | Audio demo pre-grabado listo | Tener nota de voz en francés grabada en el móvil | ☐ |
| 7 | WiFi estable | Conectar al WiFi del venue, verificar velocidad | ☐ |
| 8 | Pantalla compartida lista | Proyector/TV mostrando WhatsApp Web o mirror del móvil | ☐ |

### Feature Flags Requeridos

Configurar en Render Dashboard → Environment **antes** de la demo:

```env
DEMO_MODE=true
LLM_LIVE=true
WHISPER_ON=true
```

- `DEMO_MODE=true` — Activa respuestas de caché optimizadas para demo, reduce latencia.
- `LLM_LIVE=true` — Permite llamadas al LLM (Gemini) en tiempo real si no hay cache hit.
- `WHISPER_ON=true` — Activa transcripción de audio con Whisper para la demo de Ahmed.

---

## 2. Guión Minuto a Minuto

### t=0:00 — Introducción (30 segundos)

**Robert dice:**

> "Imaginad que sois María, una madre española que acaba de recibir una carta del gobierno sobre una ayuda llamada IMV. No sabe qué es. ¿Qué hace? Abre WhatsApp y le pregunta a Clara."

*Operador: Tener WhatsApp abierto, conversación con Clara visible en pantalla.*

---

### t=0:30 — WOW 1: María (Español, Texto) ⚡

**Acción:** El operador escribe y envía en WhatsApp:

```
Que es el IMV?
```

**Resultado esperado (< 2 segundos):**

1. Clara responde con un mensaje de texto detallado explicando el Ingreso Mínimo Vital:
   - Qué es (prestación económica de la Seguridad Social)
   - Quién puede solicitarlo
   - Cómo solicitarlo
   - Enlace a más información
2. Clara envía un **audio MP3** con la misma respuesta narrada.

**Robert dice (mientras aparece la respuesta):**

> "En menos de dos segundos, María tiene toda la información que necesita: texto claro y un audio que puede escuchar mientras cocina o va en el metro. Sin descargar ninguna app. Sin esperar en una cola telefónica. Solo WhatsApp."

**Ruta técnica:** `POST /webhook` → cache hit (`imv_es`) → respuesta texto + audio pre-generado → Twilio → WhatsApp.

---

### t=1:15 — Transición a WOW 2 (15 segundos)

**Robert dice:**

> "Pero Clara no solo habla español. Ahmed acaba de llegar de Marruecos. Habla francés. Necesita empadronarse pero no sabe cómo. Le envía una nota de voz en francés a Clara."

---

### t=1:30 — WOW 2: Ahmed (Francés, Audio) ⚡

**Acción:** El operador envía una **nota de voz en francés** preguntando:

> "Bonjour, je viens d'arriver en Espagne et j'ai besoin de savoir comment faire le empadronamiento, s'il vous plaît."

**Resultado esperado (~10 segundos):**

1. Whisper transcribe el audio del francés.
2. Clara detecta el idioma (francés).
3. Clara busca información sobre empadronamiento en la KB.
4. Clara responde **en francés** con texto explicando el trámite.
5. Clara envía un **audio MP3 en francés** con la respuesta.

**Robert dice (frases puente mientras Clara procesa):**

Usar estas frases para llenar los ~10 segundos de espera de forma natural:

> "Clara está procesando el audio de Ahmed..."

> "Whisper está transcribiendo del francés..."

> "Lo que está pasando ahora es fascinante: Whisper convierte la voz a texto, detectamos que es francés, buscamos la información sobre empadronamiento en nuestra base de conocimiento, generamos la respuesta en francés y la convertimos de nuevo a audio. Todo automático."

> "Y ahí está. Ahmed tiene su respuesta en francés. Sin traductor. Sin intermediarios."

**Ruta técnica:** `POST /webhook` → Twilio media → descarga OGG → Whisper STT → detect lang (`fr`) → KB lookup (`empadronamiento`) → Gemini genera respuesta en francés → TTS → audio MP3 → Twilio → WhatsApp.

---

### t=2:30 — Cierre (30 segundos)

**Robert dice:**

> "Esto es Clara. Un asistente de WhatsApp que habla el idioma del usuario, entiende voz y texto, y da información verificada sobre trámites reales. Hoy funciona con IMV y empadronamiento. Mañana puede cubrir cientos de trámites. Y lo más importante: funciona en el canal que ya usan mil millones de personas."

---

## 3. Procedimientos de Fallback

### Fallback A: Render en Cold Start (respuesta > 5 segundos)

| Señal | Acción |
|---|---|
| La primera petición tarda más de 5s | Robert dice: "El servidor se está despertando, esto pasa con el plan gratuito de Render. En producción usaríamos always-on." |
| Si tarda más de 15 segundos | Cambiar a capturas de pantalla pre-preparadas en el portátil |
| Si no responde en 30 segundos | Reproducir `demo-backup.mp4` |

**Prevención:** Hacer `curl /health` **5 minutos antes** de la demo y otra vez **1 minuto antes**.

### Fallback B: Whisper Falla (WOW 2 no transcribe)

| Señal | Acción |
|---|---|
| No hay respuesta tras 15s del audio | Robert dice: "Parece que Whisper está ocupado. Dejadme mostraros lo que normalmente devuelve." |
| Mostrar respuesta pre-grabada | Abrir captura de pantalla con la conversación completa en francés |
| Reproducir audio de backup | Reproducir MP3 pre-grabado con la respuesta en francés |

### Fallback C: Audio No Se Reproduce en WhatsApp

| Señal | Acción |
|---|---|
| El MP3 no carga o no suena | Robert dice: "El audio está ahí pero a veces WhatsApp tarda en cachearlo. Lo importante es el texto." |
| Leer la respuesta en voz alta | Robert lee el texto de la respuesta que sí aparece en pantalla |

### Fallback D: WiFi del Venue Falla

| Señal | Acción |
|---|---|
| Sin conexión WiFi | Cambiar a datos móviles (hotspot) |
| Sin datos móviles | Reproducir `demo-backup.mp4` directamente |

---

## 4. Puntos de Conversación Post-Demo

Después de los 3 minutos, Robert puede expandir sobre estos temas si hay preguntas:

### Tecnología
- **Whisper** (OpenAI) para speech-to-text multilingüe — soporta 99 idiomas.
- **Gemini** (Google) como LLM para generar respuestas contextuales.
- **Twilio** como gateway de WhatsApp — escalable a millones de usuarios.
- **Base de conocimiento verificada** — información oficial de fuentes gubernamentales.

### Impacto Social
- **40% de inmigrantes** en España no completan trámites por barrera idiomática.
- Clara reduce esta barrera a **cero** — responde en el idioma del usuario.
- WhatsApp tiene **penetración del 95%** en España — no hay que instalar nada.
- El audio es clave para personas con **baja alfabetización digital**.

### Escalabilidad
- Hoy: 2 trámites (IMV, empadronamiento). KB extensible a cientos.
- Coste por consulta: ~$0.002 (cache hit) a ~$0.01 (LLM + Whisper).
- Arquitectura stateless — escala horizontalmente.
- Plan: integrar con APIs oficiales de la administración pública.

### Modelo de Negocio
- B2G (Business to Government): ayuntamientos pagan por usuario atendido.
- ONG/cooperación: funding de programas de integración.
- Freemium: consultas básicas gratis, trámites asistidos premium.

---

## 5. Cronograma de Preparación

| Tiempo antes de demo | Acción |
|---|---|
| -30 min | Verificar WiFi, cargar backup video, unir sandbox |
| -15 min | `curl /health` para despertar Render |
| -10 min | Probar WOW 1 (enviar "Que es el IMV?" y verificar respuesta) |
| -5 min | Probar WOW 2 (enviar audio en francés y verificar respuesta) |
| -2 min | Limpiar chat de WhatsApp (borrar mensajes de prueba) |
| -1 min | `curl /health` final, abrir pantalla compartida |
| t=0:00 | **Comenzar demo** |

---

## 6. Contactos de Emergencia

| Rol | Responsabilidad |
|---|---|
| Operador móvil | Enviar mensajes de WhatsApp a tiempo |
| Backup técnico | Monitorizar logs de Render durante la demo |
| Presentador (Robert) | Narrar y cubrir tiempos de espera con frases puente |

---

> **Regla de oro:** Si algo falla, nunca parar. Siempre hay un fallback. La demo debe fluir sin importar qué pase con la tecnología.
