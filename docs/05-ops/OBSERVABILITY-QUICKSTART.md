# Observabilidad -- Guia rapida de CivicAid Voice / Clara

> **Resumen en una linea:** Todo lo necesario para monitorizar, depurar y alertar sobre Clara en produccion, usando logs estructurados, timings por etapa y el endpoint `/health`.

## Que es

Sistema de observabilidad integrado de Clara: generacion de `request_id` por peticion, cronometrado de cada etapa del pipeline (cache, LLM, Whisper, TTS), lineas de log etiquetadas por componente y un endpoint `/health` que reporta el estado de todos los subsistemas.

No requiere agentes externos ni infraestructura adicional. Todo se emite a stdout y se visualiza desde el dashboard de Render.

## Para quien

- **Operadores** que monitorizan Clara en produccion (dashboard Render, alertas).
- **Desarrolladores** que depuran errores o latencia en el pipeline.
- **QA** que necesita verificar el comportamiento de cada etapa.

## Que incluye

- Referencia completa de tags de log con ejemplos reales.
- Flujo de observabilidad (hooks Flask before/after request).
- Interpretacion del endpoint `/health` y cada componente.
- Recomendaciones de alertas (criticas, advertencia, informativas).
- Comandos de verificacion.

## Que NO incluye

- Exportacion OpenTelemetry (existe stub, no implementado).
- Dashboards Grafana pre-construidos (se dan queries de referencia).

---

## 1. Arquitectura de observabilidad

La pila de observabilidad de Clara es ligera e integrada -- sin agentes externos.

```
Twilio POST /webhook
        |
        v
  Flask before_request
    -> RequestContext(request_id=uuid4)
    -> Almacenado en threading.local()
        |
        v
  Pipeline (hilo de fondo)
    -> Timings por etapa via ctx.add_timing()
    -> Lineas de log etiquetadas: [ACK], [CACHE], [WHISPER], [LLM], [REST], [ERROR], [OBS], [WEBHOOK]
        |
        v
  Flask after_request
    -> Timing http_total registrado
    -> Linea resumen [OBS] emitida
    -> Contexto limpiado
```

**Nota:** El export a OpenTelemetry aun no esta implementado (existe un stub en `src/utils/observability.py`).

---

## 2. Como activar la observabilidad

La observabilidad se controla con la variable de entorno `OBSERVABILITY_ON`:

| Variable | Valor por defecto | Efecto |
|----------|-------------------|--------|
| `OBSERVABILITY_ON` | `true` | Activa generacion de `request_id`, timings por etapa, lineas `[OBS]` |
| `OTEL_ENDPOINT` | `""` (vacio) | Cuando se establece, emite un mensaje stub (export no implementado) |
| `LOG_LEVEL` | `INFO` | Nivel de logging de Python. Cambiar a `DEBUG` para ver lineas `[TIMING]` |

Para desactivar la observabilidad (por ejemplo, en tests):

```bash
OBSERVABILITY_ON=false
```

Para activar timings por skill individual (nivel DEBUG):

```bash
LOG_LEVEL=DEBUG
```

---

## 3. Tags de log -- Referencia completa

Todos los logs usan el logger `clara` de Python y se imprimen a stdout como **JSON estructurado** (una linea JSON por evento):

```json
{"ts": "2026-02-12T14:02:31", "level": "INFO", "logger": "clara", "msg": "[TAG] clave=valor", "tag": "TAG", "campo1": "valor1"}
```

### Tabla de tags

| Tag | Archivo fuente | Cuando se emite | Campos clave |
|-----|----------------|-----------------|--------------|
| `[ACK]` | `logger.py:log_ack` | Al recibir un mensaje en el webhook | `from=<numero>`, `type=<text\|audio\|image>` |
| `[CACHE]` | `logger.py:log_cache` | Tras la busqueda en cache | `HIT\|MISS`, `id=<entry_id>`, `<ms>ms` |
| `[WHISPER]` | `logger.py:log_whisper` | Tras la transcripcion de audio (Gemini) | `OK\|FAIL`, `<ms>ms`, `"<preview>"` |
| `[LLM]` | `logger.py:log_llm` | Tras la llamada a Gemini Flash | `OK\|FAIL`, `<ms>ms`, `source=gemini` |
| `[REST]` | `logger.py:log_rest` | Tras enviar respuesta via Twilio REST | `to=<numero>`, `source=<cache\|llm\|fallback>`, `total=<ms>ms` |
| `[ERROR]` | `logger.py:log_error` | Cualquier excepcion capturada | `stage=<etapa>`, `error=<mensaje>` |
| `[OBS]` | `observability.py` | Al final de cada peticion (hook after_request) | `request_id=<uuid>`, `timings={...}` |
| `[TIMING]` | `timing.py` | Por cada skill ejecutado (nivel DEBUG) | `<nombre_skill>`, `OK\|FAIL`, `<ms>ms` |

### Ejemplo: PIPELINE -- Cache hit (entrada de texto)

```json
{"ts":"2026-02-12T14:02:31","level":"INFO","logger":"clara","msg":"[ACK] from=whatsapp:+34612345678 type=text","tag":"ACK","from_number":"whatsapp:+34612345678","input_type":"text"}
{"ts":"2026-02-12T14:02:31","level":"INFO","logger":"clara","msg":"[CACHE] HIT id=imv_es_01 12ms","tag":"CACHE","hit":true,"entry_id":"imv_es_01","ms":12}
{"ts":"2026-02-12T14:02:31","level":"INFO","logger":"clara","msg":"[OBS] request_id=a1b2c3d4... timings={...}","tag":"OBS","request_id":"a1b2c3d4-e5f6-7890-abcd-ef1234567890","timings":{"cache":12,"total":12}}
{"ts":"2026-02-12T14:02:31","level":"INFO","logger":"clara","msg":"[REST] Sent to=whatsapp:+34612345678 source=cache total=15ms","tag":"REST","to_number":"whatsapp:+34612345678","source":"cache","total_ms":15}
```

### Ejemplo: PIPELINE -- Cache miss, ruta LLM

```json
{"ts":"2026-02-12T14:03:12","level":"INFO","logger":"clara","msg":"[ACK] from=whatsapp:+34612345678 type=text","tag":"ACK","from_number":"whatsapp:+34612345678","input_type":"text"}
{"ts":"2026-02-12T14:03:12","level":"INFO","logger":"clara","msg":"[CACHE] MISS 5ms","tag":"CACHE","hit":false,"ms":5}
{"ts":"2026-02-12T14:03:15","level":"INFO","logger":"clara","msg":"[LLM] OK 2800ms source=gemini","tag":"LLM","success":true,"duration_ms":2800,"source":"gemini"}
{"ts":"2026-02-12T14:03:15","level":"INFO","logger":"clara","msg":"[OBS] request_id=b2c3d4e5...","tag":"OBS","request_id":"b2c3d4e5-f6a7-8901-bcde-f12345678901","timings":{"total":3100}}
{"ts":"2026-02-12T14:03:15","level":"INFO","logger":"clara","msg":"[REST] Sent to=... source=llm total=3100ms","tag":"REST","to_number":"whatsapp:+34612345678","source":"llm","total_ms":3100}
```

### Ejemplo: AUDIO -- Transcripcion Gemini + LLM

```json
{"ts":"2026-02-12T14:05:00","level":"INFO","logger":"clara","msg":"[ACK] from=whatsapp:+34612345678 type=audio","tag":"ACK","from_number":"whatsapp:+34612345678","input_type":"audio"}
{"ts":"2026-02-12T14:05:04","level":"INFO","logger":"clara","msg":"[WHISPER] OK 3500ms","tag":"WHISPER","success":true,"duration_ms":3500,"preview":"Necesito ayuda con el ingreso minimo vital..."}
{"ts":"2026-02-12T14:05:04","level":"INFO","logger":"clara","msg":"[CACHE] MISS 3ms","tag":"CACHE","hit":false,"ms":3}
{"ts":"2026-02-12T14:05:07","level":"INFO","logger":"clara","msg":"[LLM] OK 2600ms source=gemini","tag":"LLM","success":true,"duration_ms":2600,"source":"gemini"}
{"ts":"2026-02-12T14:05:07","level":"INFO","logger":"clara","msg":"[OBS] request_id=c3d4e5f6...","tag":"OBS","request_id":"c3d4e5f6-a7b8-9012-cdef-123456789012","timings":{"total":6500}}
{"ts":"2026-02-12T14:05:07","level":"INFO","logger":"clara","msg":"[REST] Sent to=... source=llm total=6500ms","tag":"REST","to_number":"whatsapp:+34612345678","source":"llm","total_ms":6500}
```

### Ejemplo: SKILL timing (nivel DEBUG)

```
14:05:00 DEBUG [TIMING] detect_lang OK 2ms
14:05:00 DEBUG [TIMING] cache_match OK 8ms
14:05:03 DEBUG [TIMING] kb_lookup OK 15ms
14:05:06 DEBUG [TIMING] llm_generate OK 2800ms
14:05:06 DEBUG [TIMING] tts OK 450ms
14:05:06 DEBUG [TIMING] send_response OK 320ms
```

### Ejemplo: HEALTH -- Peticion al endpoint

```
14:10:00 INFO [ACK] health_check
```

---

## 4. Campos clave para triaje

Al investigar problemas en produccion, concentrarse en estos campos:

| Campo | Por que importa | Que buscar |
|-------|----------------|------------|
| `request_id` | Correlaciona todas las lineas de log de una misma peticion | Usar para trazar una peticion de principio a fin |
| `total=<ms>ms` en `[REST]` | Latencia total visible por el usuario | > 6000ms indica experiencia degradada |
| `FAIL` en cualquier tag | Algo fallo | `[WHISPER] FAIL`, `[LLM] FAIL` |
| `stage=` en `[ERROR]` | Que etapa del pipeline fallo | `pipeline`, `tts`, `pipeline_fallback` |
| `source=fallback` en `[REST]` | El usuario recibio una respuesta generica en vez de una real | Indica fallo de LLM o transcripcion |
| Ratio `[CACHE] HIT` vs `MISS` | Efectividad del cache | Tasa baja = usuarios haciendo preguntas inesperadas |

---

## 5. Como leer logs en Render

### Streaming de logs en tiempo real

1. Ir a [dashboard.render.com](https://dashboard.render.com).
2. Seleccionar el servicio **civicaid-voice**.
3. Hacer clic en **"Logs"** en la barra lateral izquierda.
4. Los logs se muestran en tiempo real. Usar Ctrl+F / Cmd+F del navegador para buscar.

### Filtrado por tag de log

El visor de logs de Render soporta busqueda de texto basica. Usar estas busquedas:

| Termino de busqueda | Que se encuentra |
|---------------------|------------------|
| `[ERROR]` | Todos los errores en todas las etapas del pipeline |
| `[WHISPER] FAIL` | Transcripciones de audio fallidas |
| `[LLM] FAIL` | Llamadas fallidas a Gemini |
| `source=fallback` | Peticiones donde el usuario recibio una respuesta generica |
| `[OBS]` | Resumenes por peticion con request_id y timings |
| Un valor especifico de `request_id` | Todas las lineas de log de una peticion |

### Descarga de logs

Render no soporta exportacion de logs en el plan gratuito. Para logging persistente, considerar reenviar stdout a un servicio externo (ver Seccion 8).

---

## 6. Endpoint de salud `/health`

### Endpoint

```
GET /health
```

Puerto en Render: **10000** | Puerto local: **5000**

### Formato de respuesta

```json
{
  "status": "ok",
  "uptime_s": 1234,
  "components": {
    "whisper_loaded": true,
    "whisper_enabled": true,
    "ffmpeg_available": true,
    "gemini_key_set": true,
    "twilio_configured": true,
    "cache_entries": 8,
    "demo_mode": false,
    "llm_live": true
  }
}
```

### Interpretacion de componentes

| Componente | Valor saludable | Si no es saludable |
|------------|----------------|-------------------|
| `status` | `"ok"` | El servicio no responde; Render mostrara "Unavailable" |
| `whisper_loaded` | `true` | El modelo no cargo (se usa Gemini API, no modelo local) -- verificar `GEMINI_API_KEY` |
| `whisper_enabled` | `true` (cuando se necesita audio) | `WHISPER_ON=false` -- intencional o mal configurado? |
| `ffmpeg_available` | `true` | Falta en la imagen Docker -- revisar Dockerfile |
| `gemini_key_set` | `true` | `GEMINI_API_KEY` no establecida o vacia -- revisar variables de entorno en Render |
| `twilio_configured` | `true` | Falta `TWILIO_ACCOUNT_SID` o `TWILIO_AUTH_TOKEN` |
| `cache_entries` | `>= 8` | `demo_cache.json` no cargado o malformado |
| `demo_mode` | depende de la intencion | `true` = solo cache (sin LLM), `false` = pipeline completo |
| `llm_live` | depende de la intencion | `false` significa que las llamadas a Gemini estan deshabilitadas |

### Health checks automatizados

Render usa `healthCheckPath: /health` (configurado en `render.yaml`) para determinar si el servicio esta listo para recibir trafico. Si `/health` falla, Render no enrutara trafico a esa instancia.

Para monitorizacion proactiva, configurar un ping cron (ver `docs/05-ops/RENDER-DEPLOY.md`):

```bash
# cron-job.org: GET https://civicaid-voice.onrender.com/health cada 14 minutos
```

---

## 7. Alertas recomendadas

Clara no incluye alertas integradas. Estas son las recomendaciones de umbrales para monitorizacion externa (UptimeRobot, notificaciones de Render, o cron-job.org):

### Alertas criticas (accion inmediata necesaria)

| Condicion | Metodo de deteccion | Umbral |
|-----------|--------------------|---------
| Servicio caido | `/health` devuelve non-200 | Cualquier fallo durante > 2 checks consecutivos |
| Clave de Gemini expirada | `/health` -> `gemini_key_set: false` | Inmediato |
| Twilio mal configurado | `/health` -> `twilio_configured: false` | Inmediato |

### Alertas de advertencia (investigar en 1 hora)

| Condicion | Metodo de deteccion | Umbral |
|-----------|--------------------|---------
| Latencia alta | Lineas `[REST]` con `total=` > 8000ms | > 3 ocurrencias en 5 minutos |
| Fallos de LLM | `[LLM] FAIL` en logs | > 2 fallos en 10 minutos |
| Fallos de transcripcion | `[WHISPER] FAIL` en logs | > 2 fallos en 10 minutos |
| Tasa baja de cache hit | Ratio de `[CACHE] HIT` a `[CACHE] MISS` | < 30% hits en 1 hora |
| Respuestas fallback | `source=fallback` en lineas `[REST]` | > 5 en 30 minutos |

### Informativas (revisar semanalmente)

| Metrica | Que revisar |
|---------|-------------|
| `uptime_s` de `/health` | Detectar reinicios inesperados (el valor se reinicia a 0) |
| Conteo de entradas cache | Asegurar `cache_entries >= 8` (set de demo esperado) |
| Volumen total de peticiones | Linea base para planificacion de capacidad |

---

## 8. Feature flags relacionadas con observabilidad

Clara cuenta con 9 feature flags en total. Las que afectan a la observabilidad son:

| Flag | Variable de entorno | Valor por defecto | Efecto |
|------|---------------------|-------------------|--------|
| Observabilidad | `OBSERVABILITY_ON` | `true` | Activa `request_id`, timings por etapa, lineas `[OBS]` |
| OTEL endpoint | `OTEL_ENDPOINT` | `""` (vacio) | Cuando se establece, emite mensaje stub (no implementado) |
| Nivel de log | `LOG_LEVEL` | `INFO` | Controla nivel de logging Python. `DEBUG` para ver `[TIMING]` |

---

## 9. Mejoras futuras

### 9.1 Logging JSON estructurado — IMPLEMENTADO (Fase 3)

Los logs ahora usan formato JSON estructurado. Cada linea es un JSON object con campos `ts`, `level`, `logger`, `msg`, `tag`, y campos especificos por tag. Implementado en `src/utils/logger.py` con la clase `JSONFormatter`.

### 9.2 Integracion OpenTelemetry

El stub en `src/utils/observability.py` (lineas 71-75) emite un placeholder cuando `OTEL_ENDPOINT` esta configurado. Para implementar trazado completo:

1. Instalar `opentelemetry-sdk` y `opentelemetry-exporter-otlp`.
2. Reemplazar el stub con creacion y exportacion de spans.
3. Mapear las claves de `RequestContext.timings` a atributos de span.
4. Apuntar `OTEL_ENDPOINT` a una instancia de Grafana Tempo o Jaeger.

### 9.3 Receta de dashboard Grafana

Si hay una instancia de Grafana disponible y los logs se reenvian a Loki, usar estas queries:

```
# Tasa de errores
count_over_time({app="clara"} |= "[ERROR]" [5m])

# Latencia de LLM (extraer ms de la linea de log)
{app="clara"} |= "[LLM] OK" | regexp `(?P<latency>\d+)ms` | unwrap latency

# Ratio de cache hit
count_over_time({app="clara"} |= "[CACHE] HIT" [1h])
/
(count_over_time({app="clara"} |= "[CACHE] HIT" [1h]) + count_over_time({app="clara"} |= "[CACHE] MISS" [1h]))

# Tasa de fallback
count_over_time({app="clara"} |= "source=fallback" [30m])
```

---

## 10. Como se verifica

### Lista de triaje rapida

1. **Servicio inaccesible?** -> Revisar el estado en el dashboard de Render y `/health`.
2. **Respuestas lentas?** -> Buscar en logs lineas `[REST]` con valores altos de `total=`. Verificar si `[LLM]` o `[WHISPER]` es el cuello de botella.
3. **Usuario recibio fallback?** -> Encontrar el `request_id` de la linea `[REST]`, buscar todas las lineas con ese ID.
4. **Audio no funciona?** -> Revisar lineas `[WHISPER]`. Verificar `whisper_loaded: true` en `/health`.
5. **Errores de LLM?** -> Revisar `[LLM] FAIL` y `[ERROR] stage=pipeline`. Verificar `gemini_key_set: true` en `/health`.

### Comandos curl utiles

```bash
# Health check (JSON, produccion en Render, puerto 10000)
curl -s https://civicaid-voice.onrender.com/health | python3 -m json.tool

# Health check (solo codigo de estado)
curl -s -o /dev/null -w "%{http_code}" https://civicaid-voice.onrender.com/health

# Health check (local, puerto 5000)
curl -s http://localhost:5000/health | python3 -m json.tool

# Test del webhook local
curl -X POST http://localhost:5000/webhook \
  -d "Body=Que es el IMV?" \
  -d "From=whatsapp:+34600000000" \
  -d "NumMedia=0"
```

---

## Referencias

| Recurso | Ubicacion |
|---------|-----------|
| Logger estructurado | `src/utils/logger.py` |
| Decorador de timing | `src/utils/timing.py` |
| Modulo de observabilidad | `src/utils/observability.py` |
| Endpoint health | `src/routes/health.py` |
| Configuracion (flags) | `src/core/config.py` |
| Pipeline (orquestador) | `src/core/pipeline.py` |
| Tests de observabilidad | `tests/unit/test_observability.py` |
| Deploy en Render | `docs/05-ops/RENDER-DEPLOY.md` |
