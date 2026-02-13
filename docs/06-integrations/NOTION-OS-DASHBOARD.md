# NOTION OS DASHBOARD -- Estructura Visual del HOME

Documentacion de la estructura de paginas y bloques del workspace de Notion para CivicAid Voice / Clara.

## Para quien

- **Equipo del proyecto** (Robert, Marcos, Lucas, Daniel, Andrea): referencia rapida para mantener y actualizar el workspace.
- **Jueces del hackathon** (OdiseIA4Good -- UDIT, Feb 2026): contexto sobre la organizacion del proyecto en Notion.

## Que incluye

- Sitemap completo del workspace.
- Estructura bloque a bloque de la pagina HOME (dashboard visual).
- Estructura de la pagina "Para Jueces".
- Estructura de la pagina "Recursos y Referencias".
- IDs de Notion de todas las paginas y bases de datos.
- Notas tecnicas de implementacion.

## Que NO incluye

- Contenido completo de las bases de datos (Backlog, KB Tramites, Testing).
- Instrucciones de creacion paso a paso (ver `NOTION-OS-RESTRUCTURA-COMPLETA.md` para eso).
- Configuracion del token o MCP (ver `MCP-TOOLS-REFERENCE.md`).

---

## 1. Sitemap del Workspace

```
CivicAid OS (raiz)
|-- Home -- Panel del Proyecto (dashboard visual)
|-- Para Jueces -- Evaluacion Rapida (2-5 min)
|-- Fases del Proyecto
|   |-- Fase 0 + Fase 1 -- Plan Maestro y MVP
|   |-- Fase 2 -- Hardening y Deploy
|   +-- Fase 3 -- Demo en Vivo
|-- Backlog / Issues (DB -- 43 entradas)
|-- KB Tramites (DB -- 12 entradas)
|-- Demo & Testing (DB -- 26 entradas)
+-- Recursos y Referencias
```

Todas las paginas estan bajo la raiz `CivicAid OS`. Las tres bases de datos (Backlog, KB Tramites, Testing) contienen 81 entradas en total y son accesibles tanto desde el sidebar como desde enlaces inline en las paginas.

---

## 2. HOME Page -- Estructura de Bloques

La pagina HOME funciona como dashboard visual del proyecto. A continuacion se describe cada seccion en orden de aparicion.

### 2.1 Hero

- **Heading 1:** "CivicAid Voice / Clara"
- **Callout azul:** Descripcion de una linea -- "Asistente conversacional WhatsApp-first que ayuda a personas vulnerables en Espana a navegar tramites de servicios sociales."

### 2.2 El Problema

- **Heading 2:** "El Problema"
- **Callout rojo:** Estadisticas clave del contexto social:
  - 3.2 millones de inmigrantes recientes en Espana que enfrentan barreras idiomaticas y burocraticas.
  - 9.5 millones de personas mayores de 65 anios con dificultades de acceso digital.
  - Tramites complejos, presenciales, con documentacion dispersa y tiempos de espera largos.

### 2.3 La Solucion: Clara

- **Heading 2:** "La Solucion: Clara"
- **Callout verde:** Descripcion breve de Clara como asistente WhatsApp con soporte de voz, texto e imagenes.
- **Tabla de 4 diferenciadores:**

| Diferenciador | Descripcion |
|---------------|-------------|
| WhatsApp nativo | Canal que ya usan 33M de personas en Espana, sin apps nuevas |
| Voz primero | Audio transcrito con Whisper, respuesta en audio con gTTS |
| Multilingue | Espanol y frances, con deteccion automatica de idioma |
| Info verificada | Knowledge base curada de 3 tramites con fuentes oficiales |

### 2.4 Stack Tecnologico

- **Heading 2:** "Stack Tecnologico"
- **Layout de 2 columnas** con callouts explicativos:

**Columna 1:**

| Herramienta | Funcion |
|-------------|---------|
| Python 3.11 + Flask | Backend ligero, respuesta HTTP en menos de 1 segundo |
| Twilio WhatsApp | Canal de mensajeria bidireccional (texto, audio, imagen) |
| Gemini 1.5 Flash | LLM para generacion de respuestas contextuales |

**Columna 2:**

| Herramienta | Funcion |
|-------------|---------|
| Whisper (base) | Transcripcion de audio a texto |
| gTTS | Sintesis de texto a audio (MP3) |
| Docker + Render | Contenedorizacion y deploy en la nube |
| Notion MCP | Gestion del proyecto, backlog y documentacion |

### 2.5 Arquitectura -- Flujo del Pipeline

- **Heading 2:** "Arquitectura -- Flujo del Pipeline"
- **Bloque de codigo** (code block, lenguaje: text):

```
USUARIO --> TWILIO --> FLASK /webhook --> TwiML ACK (<1s)
                                       --> PIPELINE (11 SKILLS):
  TEXTO: detect_lang --> cache_match --> HIT --> send_response
  AUDIO: fetch_media --> transcribe --> detect_lang --> cache_match
  MISS:  kb_lookup --> llm_generate --> verify --> tts --> send_response
```

Este diagrama muestra el patron TwiML ACK: respuesta HTTP 200 inmediata al webhook de Twilio, procesamiento completo en hilo de fondo, y envio de la respuesta final via Twilio REST API.

### 2.6 KPI Dashboard

- **Heading 2:** "KPI Dashboard"
- **Layout de 3 filas x 3 columnas** con callouts numericos:

**Fila 1:**

| Metrica | Valor | Detalle |
|---------|-------|---------|
| Tests | 96 | 91 passed + 5 xpassed, pytest completo |
| Skills | 11 | Skills atomicas en el pipeline |
| Entradas Notion | 81 | 43 Backlog + 12 KB Tramites + 26 Testing |

**Fila 2:**

| Metrica | Valor | Detalle |
|---------|-------|---------|
| Feature Flags | 9 | Configurables en config.py |
| Tramites | 3 | IMV, Empadronamiento, Tarjeta Sanitaria |
| Idiomas | 2 | Espanol y frances |

**Fila 3:**

| Metrica | Valor | Detalle |
|---------|-------|---------|
| Cache | 8 + 6 MP3 | 8 respuestas pre-calculadas + 6 archivos de audio |
| Health | 8 componentes | Endpoint /health con 8 checks |
| Gates | 22/22 PASS | Todos los gates de todas las fases superados |

### 2.7 Fases del Proyecto

- **Heading 2:** "Fases del Proyecto"
- **Tabla resumen:**

| Fase | Nombre | Estado | Contenido principal |
|------|--------|--------|---------------------|
| F0 | Plan Maestro | COMPLETADA | Arquitectura, tooling, Notion OS, agent teams |
| F1 | MVP | COMPLETADA | Pipeline 11 skills, cache-first, 93 tests, deploy |
| F2 | Hardening y Deploy | COMPLETADA | Audio, guardrails, evals, observabilidad, Render |
| F3 | Demo en Vivo | COMPLETADA | Demo ops, QA audit, verificacion anti-humo |

- **Cards de navegacion** (layout de 3 columnas):
  - Card 1: "Fase 0 + Fase 1 -- Plan Maestro y MVP" (enlace a pagina F0+F1)
  - Card 2: "Fase 2 -- Hardening y Deploy" (enlace a pagina F2)
  - Card 3: "Fase 3 -- Demo en Vivo" (enlace a pagina F3)

### 2.8 Equipo

- **Heading 2:** "Equipo"
- **Tabla de 5 miembros:**

| Nombre | Rol |
|--------|-----|
| Robert | Backend lead, pipeline, demo presenter |
| Marcos | Routes, Twilio, deploy, audio pipeline |
| Lucas | KB research, testing, demo assets |
| Daniel | Web Gradio (backup), video |
| Andrea | Notion, slides, coordination |

### 2.9 Footer

- **Divider**
- **Texto en italica:** "Ultima actualizacion: 2026-02-13 | Hackathon OdiseIA4Good -- UDIT"

---

## 3. Para Jueces -- Estructura

Pagina disenada para que los jueces evaluen el proyecto en 2 a 5 minutos.

### 3.1 Hero

- **Callout azul:** "Esta pagina resume Clara en 2 minutos. Todo lo que necesitan para evaluar el proyecto esta aqui."

### 3.2 Que es Clara

- **Heading 2:** "Que es Clara"
- Tres frases descriptivas:
  1. Clara es un asistente WhatsApp que guia a personas vulnerables por tramites de servicios sociales en Espana.
  2. Soporta texto, audio (transcripcion con Whisper) e imagenes, respondiendo en espanol y frances.
  3. Funciona con un pipeline de 11 skills orquestadas, cache-first para latencia minima, y deploy en Render.

### 3.3 Datos Clave

- **Heading 2:** "Datos Clave"
- **Tabla de 10 metricas:**

| Metrica | Valor |
|---------|-------|
| Tests totales | 96 (91 passed + 5 xpassed) |
| Skills del pipeline | 11 |
| Tramites cubiertos | 3 (IMV, Empadronamiento, Tarjeta Sanitaria) |
| Idiomas | 2 (espanol, frances) |
| Feature flags | 9 |
| Entradas en Notion | 81 (43 Backlog + 12 KB + 26 Testing) |
| Cache pre-calculado | 8 respuestas + 6 MP3 |
| Health checks | 8 componentes |
| Gates superados | 22/22 |
| Deploy | Render (Docker, healthcheck activo) |

### 3.4 Progreso por Fases

- **Heading 2:** "Progreso por Fases"
- **Tabla semaforo:**

| Fase | Estado | Gates |
|------|--------|-------|
| F0 -- Plan Maestro | VERDE | G0 Tooling PASS |
| F1 -- MVP | VERDE | G1 Texto PASS |
| F2 -- Hardening | VERDE | G2 Audio PASS |
| F3 -- Demo | VERDE | G3 Demo PASS |

### 3.5 Demo en Vivo

- **Heading 2:** "Demo en Vivo"
- Descripcion de los WOW moments:
  - **WOW 1 -- Texto:** Usuario pregunta por IMV en WhatsApp, Clara responde con pasos verificados en menos de 2 segundos.
  - **WOW 2 -- Audio:** Usuario envia nota de voz en frances, Clara transcribe, detecta idioma, y responde en frances con audio.

### 3.6 Donde Verificar

- **Heading 2:** "Donde Verificar"
- Comandos para verificacion independiente:

```bash
# Tests completos
pytest tests/ -v --tb=short

# Linter limpio
ruff check src/ tests/ --select E,F,W --ignore E501

# Health check del deploy
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

---

## 4. Recursos y Referencias -- Estructura

### 4.1 Feature Flags

- **Heading 2:** "Feature Flags"
- **Tabla de 9 flags:**

| Flag | Default | Efecto |
|------|---------|--------|
| DEMO_MODE | false | Cache-only, skip LLM tras cache miss |
| LLM_LIVE | true | Habilita Gemini |
| WHISPER_ON | true | Habilita transcripcion de audio |
| LLM_TIMEOUT | 6 | Segundos max para Gemini |
| WHISPER_TIMEOUT | 12 | Segundos max para Whisper |
| GUARDRAILS_ON | true | Habilita guardrails de contenido |
| STRUCTURED_OUTPUT_ON | false | Habilita salida estructurada JSON |
| OBSERVABILITY_ON | true | Habilita metricas y trazas |
| RAG_ENABLED | false | Habilita RAG (stub, pendiente implementacion) |

Nota: TWILIO_TIMEOUT (10s) esta hardcodeado en `src/core/skills/send_response.py`, no es un flag en config.py.

### 4.2 Endpoints

- **Heading 2:** "Endpoints"
- **Tabla de 3 endpoints:**

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| /webhook | POST | Recibe mensajes de Twilio WhatsApp |
| /health | GET | Healthcheck con 8 componentes |
| /static/cache/* | GET | Sirve archivos MP3 de cache |

### 4.3 Configuracion MCP

- **Heading 2:** "Configuracion MCP"
- Referencia a `~/.mcp.json` para el token de Notion.
- Nota: requiere reinicio de Claude Code tras cambiar el token.
- IDs de las 3 bases de datos para scripts de poblado.

---

## 5. IDs de Notion (referencia)

### Paginas

| Pagina | ID |
|--------|----|
| CivicAid OS (raiz) | 304c5a0f-372a-801f-995f-ce24036350ad |
| HOME -- Panel del Proyecto | 306c5a0f-372a-81a9-8990-feeadddb8da0 |
| Para Jueces | 306c5a0f-372a-8189-9571-cc90fc4f871f |
| Fases del Proyecto | 306c5a0f-372a-81cb-9baa-e960b5f83aa7 |
| Recursos y Referencias | 306c5a0f-372a-813b-aae5-d0a337faf44a |
| Fase 0 + Fase 1 | 305c5a0f-372a-81c8-b609-cc5fe793bfe4 |
| Fase 2 | 305c5a0f-372a-813b-8915-f7e6c21fd055 |
| Fase 3 | 305c5a0f-372a-818d-91a7-f59c22551350 |

### Bases de Datos

| Base de Datos | ID | Entradas |
|---------------|----|----------|
| Backlog / Issues | 304c5a0f-372a-81de-92a8-f54c03b391c0 | 43 |
| KB Tramites | 304c5a0f-372a-81ff-9d45-c785e69f7335 | 12 |
| Demo & Testing | 304c5a0f-372a-810d-8767-d77efbd46bb2 | 26 |

---

## 6. Notas de Implementacion

### Limitaciones de la API de Notion

1. **Vistas de base de datos:** Las vistas (Board por Fase, Calendar, etc.) no se pueden crear por API. Requieren configuracion manual desde la interfaz web de Notion.

2. **Bloques column_list:** Los bloques de tipo `column_list` deben crearse con sus `column` hijos incluidos inline en la misma llamada. No es posible crear un `column_list` vacio y luego agregarle columnas.

3. **Limite de bloques por llamada:** La API de Notion acepta un maximo de 100 bloques hijos por llamada a `PATCH /blocks/{id}/children`. Para paginas con mas de 100 bloques, es necesario dividir en multiples llamadas.

4. **Code blocks:** Los bloques de codigo soportan resaltado de sintaxis (python, bash, text, etc.) pero no soportan diagramas Mermaid. Para diagramas de arquitectura se usa ASCII art dentro de bloques de codigo con lenguaje `text`.

### Orden de creacion

Para reconstruir el HOME desde cero:

1. Crear la pagina bajo la raiz del workspace.
2. Agregar bloques secuencialmente en el orden descrito en la seccion 2.
3. Para secciones con columnas (Stack Tecnologico, KPI Dashboard, Cards de navegacion), crear el `column_list` con todas las columnas y su contenido en una sola llamada.
4. Las tablas se crean como bloques `table` con `table_row` hijos.

### Actualizacion de metricas

Cuando cambian las metricas del proyecto (tests, entries, etc.), actualizar en:

- Seccion 2.6 (KPI Dashboard del HOME).
- Seccion 3.3 (Datos Clave de Para Jueces).
- Este documento.

---

*Documento generado para el proyecto CivicAid Voice / Clara -- Hackathon OdiseIA4Good, UDIT, Feb 2026.*
