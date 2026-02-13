# Structured Outputs y Guardrails -- CivicAid Voice / Clara

> **Resumen en una linea:** Structured Outputs formatea las respuestas de Clara en JSON con campos estandarizados; Guardrails filtra contenido peligroso antes y despues del LLM para proteger a los usuarios.

## Que es

Dos modulos complementarios que mejoran la calidad y seguridad de las respuestas de Clara:

- **Structured Outputs:** Convierte la salida de texto libre del LLM (Gemini Flash) en un objeto JSON con campos definidos (resumen, pasos, documentos, fuentes, disclaimer). Permite un formato de respuesta coherente y parseable.
- **Guardrails:** Sistema de seguridad con dos puntos de chequeo -- `pre_check` (filtra la entrada del usuario antes de procesarla) y `post_check` (modifica la salida del LLM antes de enviarla al usuario). Bloquea temas peligrosos, redacta datos personales (PII) y anade disclaimers legales/medicos.

## Para quien

- **Desarrolladores** que extienden el pipeline de Clara o anaden nuevos tramites.
- **QA** que valida el formato de salida y la seguridad de las respuestas.
- **Operadores** que necesitan entender por que una respuesta fue bloqueada o modificada.

## Que incluye

- Explicacion de ambos sistemas con ejemplos reales.
- Feature flags correspondientes y valores por defecto.
- Schema Pydantic de structured output.
- Patrones de guardrails (blocklist, PII, disclaimers).
- Estado actual de implementacion.

## Que NO incluye

- Guardrails basados en LLM (toda la logica es determinista via regex).
- Validacion semantica de las respuestas (solo validacion estructural).
- Moderacion de imagenes (solo se procesan texto y audio).

---

## 1. Structured Outputs

### Que son y para que sirven

Structured Outputs es un mecanismo opt-in que instruye a Gemini Flash para que responda en formato JSON con un schema predefinido. En lugar de texto libre, Clara recibe un objeto con campos tipados que luego se transforman en texto formateado para WhatsApp.

**Ventajas:**
- Formato de respuesta consistente para todos los tramites.
- Facil de parsear programaticamente (API futura, front-end web).
- Cada campo tiene un proposito claro (pasos, documentos, avisos, fuentes).

### Feature flag

| Variable de entorno | Valor por defecto | Efecto |
|---------------------|-------------------|--------|
| `STRUCTURED_OUTPUT_ON` | `false` | Cuando es `true`, se anade instruccion JSON al prompt de Gemini y se parsea la respuesta |

### Estado actual: STUB (deshabilitado por defecto)

El codigo esta completo e implementado en `src/core/models_structured.py` y `src/core/skills/llm_generate.py`, pero la flag esta en `false` por defecto. Esto significa que en produccion Clara responde con texto libre (comportamiento clasico). Activar con `STRUCTURED_OUTPUT_ON=true` para probar.

### Schema Pydantic

El schema se define en `src/core/models_structured.py` con la clase `ClaraStructuredResponse`:

```python
class ClaraStructuredResponse(BaseModel):
    intent: str          # "informacion", "requisitos", "pasos", "documentos", "otro"
    language: str        # "es", "fr", "en", "ar"
    tramite: str | None  # "imv", "empadronamiento", "tarjeta_sanitaria", o null
    summary: str         # Resumen de 1-2 frases
    steps: list[str]     # Pasos ordenados (si aplica)
    required_docs: list[str]  # Documentos necesarios
    warnings: list[str]  # Avisos importantes
    sources: list[str]   # URLs de fuentes oficiales
    disclaimer: str      # Disclaimer legal
```

### Flujo en el pipeline

```
Usuario -> ... -> llm_generate() -> texto bruto del LLM
                                      |
                        STRUCTURED_OUTPUT_ON=true?
                                      |
                              SI -> parse_structured_response()
                                      |
                              Parseo exitoso? -> display_text formateado
                              Parseo fallo?   -> texto original sin cambios (zero breakage)
```

El parseo es tolerante a fallos: si el JSON no es valido o no cumple el schema, se usa el texto original sin modificar. Esto garantiza que activar la flag nunca rompe las respuestas.

### Ejemplo: Respuesta SIN structured output (por defecto)

```
El Ingreso Minimo Vital (IMV) es una prestacion economica de la
Seguridad Social para personas en situacion de vulnerabilidad.

Para solicitarlo necesitas: DNI/NIE, certificado de empadronamiento,
y declaracion de la renta.

Mas informacion: https://www.seg-social.es/imv
```

### Ejemplo: Respuesta CON structured output (`STRUCTURED_OUTPUT_ON=true`)

```
El IMV es una prestacion economica de la Seguridad Social.

Pasos:
  1. Reunir documentos necesarios
  2. Solicitar cita previa en la Seguridad Social
  3. Presentar la solicitud online o presencialmente

Documentos necesarios:
  - DNI/NIE
  - Certificado de empadronamiento

Aviso: El plazo de resolucion puede variar segun comunidad autonoma

Mas info: https://www.seg-social.es/imv

Esta informacion es orientativa. Consulte fuentes oficiales para confirmar.
```

### Tests

96 tests totales en el proyecto (91 passed + 5 xpassed). Los tests especificos de structured outputs estan en `tests/unit/test_structured_outputs.py` y cubren:

- Validacion del modelo Pydantic (campos requeridos y opcionales).
- Parseo de JSON valido, JSON en bloques de codigo markdown.
- Fallback cuando el JSON es invalido o parcial.
- Verificacion de que la flag `STRUCTURED_OUTPUT_ON=false` no tiene impacto.

---

## 2. Guardrails

### Que son y que validan

Guardrails es un sistema de seguridad determinista (basado en regex, sin LLM) que protege a los usuarios en dos puntos del pipeline:

1. **Pre-check (`pre_check`):** Analiza la entrada del usuario ANTES de procesarla. Si detecta temas peligrosos (autolesion, violencia, actividades ilegales), bloquea el mensaje y devuelve una respuesta de seguridad con recursos de emergencia.

2. **Post-check (`post_check`):** Analiza la salida del LLM ANTES de enviarla al usuario. Aplica tres tipos de modificacion:
   - **Disclaimer legal/medico:** Anade un disclaimer cuando detecta temas legales o medicos.
   - **Redaccion de PII:** Sustituye patrones de DNI, NIE y telefonos por `[TIPO REDACTADO]`.
   - **Sin duplicacion:** No anade disclaimer si ya esta presente.

### Feature flag

| Variable de entorno | Valor por defecto | Efecto |
|---------------------|-------------------|--------|
| `GUARDRAILS_ON` | `true` | Cuando es `true`, activa pre_check y post_check en el pipeline |

### Estado actual: ACTIVO por defecto

A diferencia de Structured Outputs, los guardrails estan habilitados por defecto (`GUARDRAILS_ON=true`). Esto es intencional porque Clara atiende a personas vulnerables y la seguridad es prioritaria.

### Flujo en el pipeline

```
Usuario -> pre_check(texto)
              |
        safe=false? -> Respuesta de emergencia (024, 112, etc.) -> FIN
              |
        safe=true -> [cache, KB, LLM, verify]
              |
              v
        post_check(respuesta_llm)
              |
        Anadir disclaimer si es legal/medico
        Redactar PII (DNI, NIE, telefono)
              |
              v
        Enviar al usuario via Twilio REST
```

### Patrones bloqueados (pre-check)

| Patron | Categoria | Respuesta de seguridad |
|--------|-----------|------------------------|
| `suicid*`, `matarme`, `hacerme dano`, `autolesion*` | `self_harm` | "Si necesitas ayuda urgente, llama al 024 (linea de atencion a la conducta suicida) o al 112." |
| `bomba`, `explosivo`, `armas`, `terroris*` | `violence` | "No puedo ayudar con ese tema. Si hay una emergencia, llama al 112." |
| `hackear`, `robar identidad`, `falsificar` | `illegal` | "No puedo asistir con actividades ilegales. Consulte con un profesional legal." |

### Patrones de PII (post-check)

| Patron | Tipo | Ejemplo de redaccion |
|--------|------|---------------------|
| `\b\d{8}[A-Z]\b` | DNI | `12345678A` -> `[DNI REDACTADO]` |
| `\b[XYZ]\d{7}[A-Z]\b` | NIE | `X1234567B` -> `[NIE REDACTADO]` |
| `\b\d{3}[-.]?\d{3}[-.]?\d{3}\b` | Telefono | `612345678` -> `[phone REDACTADO]` |

### Disclaimer legal/medico

Cuando se detectan palabras como `abogado`, `legal`, `juridic`, `demanda`, `medic`, `diagnostic`, `receta` o `tratamiento` en la respuesta del LLM, se anade automaticamente:

```
IMPORTANTE: Esta informacion es orientativa y no constituye
asesoramiento legal ni medico. Consulte con un profesional cualificado
o visite las fuentes oficiales para su caso concreto.
```

### Ejemplo: Entrada bloqueada por guardrail

**Entrada del usuario:**
```
quiero hacerme dano
```

**Respuesta de Clara (guardrail pre-check):**
```
Si necesitas ayuda urgente, llama al 024 (linea de atencion a
la conducta suicida) o al 112.
```

El pipeline se detiene inmediatamente -- no se llama al cache, KB ni LLM.

### Ejemplo: Salida modificada por post-check

**Respuesta original del LLM:**
```
Tu DNI es 12345678A. Deberias consultar un abogado para revisar tu caso.
```

**Respuesta modificada por guardrail:**
```
Tu DNI es [DNI REDACTADO]. Deberias consultar un abogado para revisar tu caso.

IMPORTANTE: Esta informacion es orientativa y no constituye
asesoramiento legal ni medico. Consulte con un profesional cualificado
o visite las fuentes oficiales para su caso concreto.
```

### Tests

Los tests de guardrails estan en `tests/unit/test_guardrails.py` (18 tests) y `tests/unit/test_redteam.py`. Cubren:

- Bloqueo de autolesion, violencia, actividades ilegales.
- Redaccion de DNI, NIE, telefono.
- Disclaimer para temas legales y medicos.
- No duplicacion de disclaimers.
- Paso correcto de entradas seguras (tramites normales).
- Configurabilidad de la flag `GUARDRAILS_ON`.
- Red team: variantes de frases peligrosas.

---

## 3. Resumen de feature flags

Clara cuenta con 10 feature flags en total. Las dos relevantes para este documento son:

| Flag | Variable | Valor por defecto | Estado |
|------|----------|-------------------|--------|
| Structured Outputs | `STRUCTURED_OUTPUT_ON` | `false` | Stub -- deshabilitado, codigo completo |
| Guardrails | `GUARDRAILS_ON` | `true` | Activo -- habilitado por defecto |

Para activar ambos en un entorno de prueba:

```bash
export STRUCTURED_OUTPUT_ON=true
export GUARDRAILS_ON=true
```

Para desactivar ambos (solo para tests aislados):

```bash
export STRUCTURED_OUTPUT_ON=false
export GUARDRAILS_ON=false
```

---

## Como se verifica

```bash
# Ejecutar tests de structured outputs
pytest tests/unit/test_structured_outputs.py -v

# Ejecutar tests de guardrails
pytest tests/unit/test_guardrails.py -v

# Ejecutar tests de red team
pytest tests/unit/test_redteam.py -v

# Ejecutar todos los tests del proyecto (93 total)
pytest tests/ -v --tb=short

# Verificar valor por defecto de las flags
python3 -c "from src.core.config import Config; c=Config(); print(f'STRUCTURED_OUTPUT_ON={c.STRUCTURED_OUTPUT_ON}, GUARDRAILS_ON={c.GUARDRAILS_ON}')"
```

---

## Referencias

| Recurso | Ubicacion |
|---------|-----------|
| Modelo structured output (Pydantic) | `src/core/models_structured.py` |
| Generacion LLM (instruccion JSON) | `src/core/skills/llm_generate.py` |
| Modulo guardrails | `src/core/guardrails.py` |
| Pipeline (orquestador) | `src/core/pipeline.py` |
| Configuracion (flags) | `src/core/config.py` |
| Tests structured outputs | `tests/unit/test_structured_outputs.py` |
| Tests guardrails | `tests/unit/test_guardrails.py` |
| Tests red team | `tests/unit/test_redteam.py` |
