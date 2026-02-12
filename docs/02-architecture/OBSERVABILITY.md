# Capa de Observabilidad — CivicAid Voice / Clara

> **Resumen en una linea:** Sistema de observabilidad ligero con request_id por peticion, tags de log por etapa, decorador @timed para skills, y endpoint /health con 8 componentes.

## Que es

Clara incluye una capa de observabilidad que asigna un `request_id` unico a cada peticion entrante, registra tiempos por etapa del pipeline, y genera logs estructurados con tags para facilitar el filtrado y la depuracion. Incluye un stub de OpenTelemetry para integracion futura.

## Para quien

- **Desarrolladores** que necesitan depurar el pipeline o medir tiempos de ejecucion.
- **Operadores** que monitorizan Clara en produccion y necesitan filtrar logs.
- **Jurado** que quiere entender las capacidades de observabilidad del sistema.

## Que incluye

- Flujo de request_id (desde Twilio hasta la respuesta final).
- 8 tags de log con sus funciones y niveles.
- Decorador `@timed` para medir tiempos de skills.
- Feature flag `OBSERVABILITY_ON` y variables relacionadas.
- Endpoint `/health` con 8 componentes.
- Modulos: `observability.py`, `logger.py`, `timing.py`.

## Que NO incluye

- Exportacion real a OpenTelemetry (solo stub).
- Logging en formato JSON (los logs son texto plano).
- Alertas o dashboards (requiere integracion con Grafana, Datadog, etc.).

---

## 1. Flujo de request_id

Cada peticion que llega al endpoint `/webhook` recibe un identificador unico (`request_id`) que se propaga a traves de todo el pipeline. Esto permite correlacionar todos los logs de una misma peticion.

```
Twilio POST /webhook
    |
    v
Flask before_request hook
    -> Crea RequestContext(request_id=uuid4)
    -> Almacena en threading.local()
    |
    v
webhook() handler
    -> Lee ctx del thread-local
    -> Asigna msg.request_id = ctx.request_id
    |
    v
pipeline.process(msg) [hilo de fondo]
    -> Lee ctx via get_context()
    -> Registra timings via ctx.add_timing()
    -> Escribe linea [OBS] request_id=... timings=...
    |
    v
Flask after_request hook
    -> Registra timing http_total
    -> Escribe linea [OBS] final
    -> Limpia thread-local context
```

**Nota importante:** El pipeline se ejecuta en un hilo de fondo (lanzado en `webhook.py`). El hook `after_request` se dispara en el hilo HTTP (la respuesta ACK rapida), no en el hilo del pipeline. El pipeline escribe su propia linea `[OBS]` cuando termina via `log_observability(ctx)`.

---

## 2. Tags de Log

Todos los logs usan prefijos con tags entre corchetes para facilitar el filtrado con `grep`. Cada tag tiene una funcion dedicada en `src/utils/logger.py`.

| Tag | Funcion | Nivel | Campos clave |
|-----|---------|-------|-------------|
| `[ACK]` | `log_ack(from_number, input_type)` | INFO | `from`, `type` |
| `[CACHE]` | `log_cache(hit, entry_id, ms)` | INFO | `HIT\|MISS`, `id`, `ms` |
| `[WHISPER]` | `log_whisper(success, duration_ms, text_preview)` | INFO/WARN | `OK\|FAIL`, `ms`, `preview` |
| `[LLM]` | `log_llm(success, duration_ms, source)` | INFO/WARN | `OK\|FAIL`, `ms`, `source` |
| `[REST]` | `log_rest(to_number, source, total_ms)` | INFO | `to`, `source`, `total` |
| `[ERROR]` | `log_error(stage, error)` | ERROR | `stage`, `error` |
| `[OBS]` | `log_observability(ctx)` / `observability.py` | INFO | `request_id`, `timings` |
| `[TIMING]` | `@timed` en `timing.py` | DEBUG | `skill_name`, `OK\|FAIL`, `ms` |

### Ejemplo de salida de logs

```
12:34:56 INFO [ACK] from=whatsapp:+34612345678 type=text
12:34:56 INFO [CACHE] HIT id=maria_imv_es 15ms
12:34:56 INFO [REST] Sent to=whatsapp:+34612345678 source=cache total=18ms
12:34:56 INFO [OBS] request_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890 timings={'cache': 15, 'total': 18}
```

### Ejemplo con audio (cache miss)

```
12:35:10 INFO [ACK] from=whatsapp:+33612345678 type=audio
12:35:12 INFO [WHISPER] OK 1800ms "Comment faire pour m'inscrire..."
12:35:12 INFO [CACHE] MISS 1820ms
12:35:16 INFO [LLM] OK 3500ms source=gemini
12:35:16 INFO [REST] Sent to=whatsapp:+33612345678 source=llm total=5800ms
12:35:16 INFO [OBS] request_id=b2c3d4e5-f6a7-8901-bcde-f12345678901 timings={'total': 5800}
```

---

## 3. Decorador @timed

El decorador `@timed(skill_name)` en `src/utils/timing.py` mide automaticamente el tiempo de ejecucion de cualquier funcion y lo registra a nivel DEBUG.

```python
from src.utils.timing import timed

@timed("cache_match")
def match(text: str, language: str, input_type) -> CacheResult:
    # ... logica de matching ...
```

Genera logs como:

```
12:34:56 DEBUG [TIMING] cache_match OK 12ms
12:34:57 DEBUG [TIMING] llm_generate FAIL 6001ms
```

Para ver estos logs, hay que configurar `LOG_LEVEL=DEBUG` en las variables de entorno.

---

## 4. Timings por Etapa

El pipeline registra los siguientes tiempos (en milisegundos) en el `RequestContext`:

| Etapa | Donde se registra | Descripcion |
|-------|-------------------|-------------|
| `cache` | `pipeline.py` | Tiempo hasta la respuesta de cache (solo en cache HIT) |
| `total` | `pipeline.py` | Tiempo total del procesamiento del pipeline |
| `http_total` | `after_request` hook | Tiempo total de la peticion HTTP (solo la ruta ACK) |

---

## 5. Feature Flags de Observabilidad

| Flag | Variable de entorno | Default | Efecto |
|------|-------------------|---------|--------|
| OBSERVABILITY_ON | `OBSERVABILITY_ON` | `true` | Habilita la generacion de request_id, tracking de timings, y lineas [OBS] en logs |
| OTEL_ENDPOINT | `OTEL_ENDPOINT` | `""` (vacio) | Cuando se configura, registra un stub de exportacion OTEL (no implementado aun) |
| LOG_LEVEL | `LOG_LEVEL` | `INFO` | Configurar a `DEBUG` para ver las lineas `[TIMING]` por skill |

### Configuracion

```bash
# Habilitar observabilidad (por defecto)
export OBSERVABILITY_ON=true

# Deshabilitar observabilidad
export OBSERVABILITY_ON=false

# Habilitar stub de exportacion OTEL
export OTEL_ENDPOINT=http://localhost:4317

# Habilitar timing por skill a nivel DEBUG
export LOG_LEVEL=DEBUG
```

---

## 6. Endpoint /health

`GET /health` devuelve un JSON con el estado de 8 componentes del sistema. Render usa `healthCheckPath: /health` para enrutar trafico. El cron de keep-alive hace ping a este endpoint cada 14 minutos.

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

### Componentes reportados

| # | Componente | Tipo | Descripcion |
|---|-----------|------|-------------|
| 1 | `status` | string | Estado general: siempre "ok" si el servidor responde |
| 2 | `uptime_s` | int | Segundos desde el inicio del servidor (se resetea en restart) |
| 3 | `whisper_loaded` | bool | Si el modelo Whisper esta cargado en memoria |
| 4 | `whisper_enabled` | bool | Si la feature flag WHISPER_ON esta activada |
| 5 | `ffmpeg_available` | bool | Si ffmpeg esta disponible en el PATH |
| 6 | `gemini_key_set` | bool | Si la GEMINI_API_KEY esta configurada |
| 7 | `twilio_configured` | bool | Si TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN estan configurados |
| 8 | `cache_entries` | int | Numero de entradas en demo_cache.json (esperado: 8) |
| 9 | `demo_mode` | bool | Si DEMO_MODE esta activado |
| 10 | `llm_live` | bool | Si LLM_LIVE esta activado |

---

## 7. Formato de Logs

Todos los logs se escriben en stdout en formato texto plano:

```
HH:MM:SS LEVEL [TAG] key=value key=value ...
```

Configurado en `src/utils/logger.py`:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
```

---

## 8. Modulo: src/utils/observability.py

### Clase RequestContext

```python
@dataclass
class RequestContext:
    request_id: str    # UUID4 generado automaticamente
    start_time: float  # time.time() al momento de creacion
    timings: dict      # Diccionario de tiempos por etapa

    def add_timing(self, stage: str, ms: int) -> None
    def to_dict(self) -> dict
```

### Funciones

| Funcion | Descripcion |
|---------|-------------|
| `set_context(ctx)` | Almacena RequestContext en thread-local storage |
| `get_context()` | Recupera RequestContext (devuelve None si no existe) |
| `clear_context()` | Elimina el contexto del thread-local |
| `init_app(app)` | Registra hooks before/after request en Flask |

### Hooks de Flask

- **before_request:** Si `OBSERVABILITY_ON=true`, crea un `RequestContext` nuevo y lo almacena en `threading.local()`.
- **after_request:** Si `OBSERVABILITY_ON=true`, registra el timing `http_total`, escribe la linea `[OBS]` final, comprueba el stub de OTEL, y limpia el contexto.

---

## 9. Modulo: src/utils/logger.py

Siete funciones de logging estructurado, cada una con su tag:

| Funcion | Tag | Uso |
|---------|-----|-----|
| `log_ack(from_number, input_type)` | `[ACK]` | Se llama al recibir un mensaje en el webhook |
| `log_cache(hit, entry_id, ms)` | `[CACHE]` | Se llama tras la busqueda en cache |
| `log_whisper(success, duration_ms, text_preview)` | `[WHISPER]` | Se llama tras la transcripcion de audio |
| `log_llm(success, duration_ms, source)` | `[LLM]` | Se llama tras la generacion con Gemini |
| `log_rest(to_number, source, total_ms)` | `[REST]` | Se llama al enviar la respuesta final |
| `log_error(stage, error)` | `[ERROR]` | Se llama cuando ocurre un error en cualquier etapa |
| `log_observability(ctx)` | `[OBS]` | Se llama con el RequestContext al finalizar el pipeline |

---

## 10. Modulo: src/utils/timing.py

- **`@timed(skill_name)`**: Decorador que envuelve una funcion y registra `[TIMING] <skill> OK|FAIL <ms>ms` a nivel DEBUG. Captura excepciones, registra el tiempo de fallo, y re-lanza la excepcion.

---

## 11. Tests

Los tests de observabilidad se encuentran en `tests/unit/test_observability.py`:

- `test_request_context_creation` — Generacion de UUID y valores por defecto
- `test_timing_tracking` — add_timing registra correctamente
- `test_to_dict` — Serializacion
- `test_context_thread_local` — Aislamiento entre hilos
- `test_clear_context` — Limpieza
- `test_observability_flag_off` — No falla cuando esta deshabilitado

---

## 12. Futuro: Integracion con OpenTelemetry

Cuando se configure `OTEL_ENDPOINT`, el sistema actualmente registra un mensaje stub. Para implementar la exportacion completa:

1. Instalar `opentelemetry-sdk` y `opentelemetry-exporter-otlp`.
2. Reemplazar el stub en `observability.py` `_obs_after` con creacion real de spans.
3. Mapear `RequestContext.timings` a atributos de span de OTEL.
4. Exportar al `OTEL_ENDPOINT` configurado.

## 13. Futuro: Logging JSON Estructurado

Los logs actuales son texto plano (`HH:MM:SS LEVEL [TAG] key=value`). Para agregacion de logs en produccion (Datadog, Loki, CloudWatch), se deberia reemplazar el formato actual con un formateador JSON. Ver `docs/05-ops/OBSERVABILITY-QUICKSTART.md` para la propuesta de implementacion.

---

## Como se verifica

```bash
# Verificar el endpoint /health (8 componentes)
curl http://localhost:5000/health | python3 -m json.tool

# Verificar en Render
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool

# Ver logs con tags de observabilidad
LOG_LEVEL=DEBUG python -m src.app
# En otra terminal:
curl -X POST http://localhost:5000/webhook -d "Body=Que es el IMV&From=whatsapp:+34000000000"

# Ejecutar tests de observabilidad
pytest tests/unit/test_observability.py -v
```

## Referencias

- [Arquitectura Tecnica](ARCHITECTURE.md) — Pipeline y modelos de datos
- [Observability Quickstart](../05-ops/OBSERVABILITY-QUICKSTART.md) — Guia rapida para operadores
- [Deploy en Render](../05-ops/RENDER-DEPLOY.md) — Configuracion de healthcheck y cron
- [Indice de Documentacion](../00-DOCS-INDEX.md) — Navegacion completa
