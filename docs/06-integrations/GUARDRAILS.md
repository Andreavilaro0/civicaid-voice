# Guardrails — Capa de Seguridad de Clara

> **Resumen en una linea:** Sistema de seguridad pre/post que bloquea entradas peligrosas, redacta PII y anade disclaimers legales/medicos a las respuestas.

## Vision general

Clara incluye una capa de seguridad pre/post que protege a los usuarios y asegura un comportamiento responsable de la IA. Los guardrails se ejecutan **antes** de procesar la entrada del usuario (pre-check) y **despues** de generar la salida del LLM (post-check).

## Arquitectura

```
Entrada Usuario -> [PRE-CHECK] -> Pipeline (cache/KB/LLM) -> [POST-CHECK] -> Usuario
                      |                                           |
                      v                                           v
               Bloquear entrada danina                   Anadir disclaimers
               Devolver info de linea de ayuda           Redactar PII
```

## Feature Flag

| Flag | Variable de entorno | Por defecto | Efecto |
|------|---------------------|-------------|--------|
| GUARDRAILS_ON | `GUARDRAILS_ON` | `true` | Activar/desactivar todos los guardrails |

Cuando `GUARDRAILS_ON=false`, todas las verificaciones se omiten y la entrada/salida pasa sin cambios.

## Reglas de Pre-Check

El pre-check se ejecuta sobre la entrada del usuario **antes** de cualquier procesamiento del pipeline. Si se detecta un patron bloqueado, el pipeline retorna inmediatamente con una respuesta segura (numero de linea de ayuda, etc.).

| Categoria | Patrones | Respuesta |
|-----------|----------|-----------|
| self_harm | suicid, matarme, hacerme dano, autolesion | Linea de ayuda 024 / 112 |
| violence | bomba, explosivo, arma, terroris | Emergencias 112 |
| illegal | hackear, robar identidad, falsificar documento | Derivacion a profesional legal |

## Reglas de Post-Check

El post-check se ejecuta sobre la salida del LLM **antes** de enviarla al usuario.

### Disclaimer legal/medico
Si la respuesta menciona terminos legales o medicos (abogado, legal, medico, tratamiento, etc.), se anade un disclaimer:

> IMPORTANTE: Esta informacion es orientativa y no constituye asesoramiento legal ni medico. Consulte con un profesional cualificado o visite las fuentes oficiales para su caso concreto.

### Redaccion de PII
Los patrones de datos sensibles se redactan de la salida del LLM para evitar devolver PII del usuario:

| Patron | Tipo | Reemplazo |
|--------|------|-----------|
| `\b\d{8}[A-Z]\b` | DNI | `[DNI REDACTADO]` |
| `\b[XYZ]\d{7}[A-Z]\b` | NIE | `[NIE REDACTADO]` |
| `\b\d{3}[-.]?\d{3}[-.]?\d{3}\b` | Telefono | `[phone REDACTADO]` |

## Como extender

### Anadir un nuevo patron bloqueado
Editar `BLOCKED_PATTERNS` en `src/core/guardrails.py`:

```python
BLOCKED_PATTERNS = [
    ...
    (r'\bnuevo_patron\b', 'nombre_categoria', 'Mensaje de respuesta al usuario.'),
]
```

### Anadir un nuevo patron de PII
Editar `PII_PATTERNS` en `src/core/guardrails.py`:

```python
PII_PATTERNS = [
    ...
    (r'patron_regex', 'TIPO_PII'),
]
```

## NeMo Guardrails (futuro)

Para produccion, considerar integrar NVIDIA NeMo Guardrails para:
- Rails tematicos (mantener la conversacion en tema)
- Deteccion de jailbreak
- Rails de verificacion de hechos
- Seguridad en conversaciones multi-turno

El enfoque actual basado en regex es un MVP ligero adecuado para la demo del hackathon, disenado para ser reemplazado por NeMo o frameworks similares en produccion.

## Tests

```bash
# Ejecutar tests unitarios de guardrails
pytest tests/unit/test_guardrails.py -v

# Ejecutar script de verificacion completo
bash scripts/verify_guardrails.sh
```

## Archivos

| Archivo | Proposito |
|---------|-----------|
| `src/core/guardrails.py` | Logica de pre-check y post-check |
| `src/core/config.py` | Flag `GUARDRAILS_ON` |
| `src/core/pipeline.py` | Puntos de integracion (pre/post) |
| `tests/unit/test_guardrails.py` | Tests unitarios (16 tests) |
| `scripts/verify_guardrails.sh` | Script de verificacion |

## Referencias

- [Structured Outputs y Guardrails (guia completa)](../05-ops/STRUCTURED-OUTPUTS-GUARDRAILS.md)
- [Integracion del Toolkit](../02-architecture/TOOLKIT-INTEGRATION.md)
