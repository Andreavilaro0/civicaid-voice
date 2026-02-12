# Framework de Evaluacion

> **Resumen en una linea:** Suite de evaluacion automatizada para medir la calidad de las respuestas de Clara contra patrones de contenido esperados.

## Vision general

Suite de evaluacion automatizada para la calidad de respuestas de Clara. Testea respuestas de cache y busquedas de KB contra patrones de contenido esperados.

## Estructura

```
data/evals/
  imv_evals.json              # 5 casos — consultas sobre IMV
  empadronamiento_evals.json  # 5 casos — consultas sobre empadronamiento
  tarjeta_evals.json          # 3 casos — consultas sobre tarjeta sanitaria
  safety_evals.json           # 3 casos — consultas de seguridad/fuera de tema

src/utils/eval_runner.py      # Motor de evaluacion (cargar, ejecutar, reportar)
scripts/run_evals.py          # Ejecutor CLI
tests/unit/test_evals.py      # Tests unitarios del framework de evals
```

## Formato de caso de evaluacion

```json
{
  "id": "imv_01",
  "query": "Que es el IMV?",
  "language": "es",
  "expected_contains": ["IMV", "Ingreso Minimo"],
  "expected_not_contains": ["empadronamiento"],
  "expected_tramite": "imv"
}
```

- `expected_contains`: subcadenas (sin distincion de mayusculas) que DEBEN aparecer en la respuesta
- `expected_not_contains`: subcadenas que NO DEBEN aparecer
- `expected_tramite`: metadato para clasificacion (no verificado por el runner)

## Ejecucion de evals

```bash
# Ejecutar suite de evaluacion
python3 scripts/run_evals.py

# Ejecutar tests unitarios del framework de evals
pytest tests/unit/test_evals.py -v
```

## Puntuacion

- Cada caso recibe una puntuacion de 0.0 a 1.0 basada en verificaciones pasadas / total de verificaciones
- Un caso aprueba solo si TODAS las verificaciones pasan (puntuacion = 1.0)
- Los reportes muestran tasas de aprobacion por conjunto y globales

## Referencias

- [Plan de Testing](TEST-PLAN.md)
- [Integracion del Toolkit](../02-architecture/TOOLKIT-INTEGRATION.md)
