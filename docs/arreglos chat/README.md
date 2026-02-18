# Arreglos Chat — Registro de Auditorias e Implementaciones

> Carpeta organizada con todos los reportes, evidencia y backlog generados durante las sesiones de trabajo con Claude Code sobre el proyecto Clara / CivicAid Voice.

## Estado Actual

| Fase | Estado | Descripcion |
|------|--------|-------------|
| **Fase 1** | CERRADA | Estabilizacion + salida de demo + calidad percibida |
| **Fase 2** | CERRADA | Memoria + personalizacion por usuario + continuidad multi-turn |
| Fase 3 | Pendiente | RAG vectorial + TTS premium |

## Indice por Fases

### [Fase 1](fase-1/) — Estabilizacion + Salida de Demo

| Documento | Descripcion |
|-----------|-------------|
| [FASE1-CLOSING-REPORT.md](fase-1/FASE1-CLOSING-REPORT.md) | Reporte de cierre: resumen ejecutivo, gates before/after, tickets, cambios, flags, riesgos |
| [AUDIT-REPORT-FASE1-VALIDADO.md](fase-1/AUDIT-REPORT-FASE1-VALIDADO.md) | Auditoria tecnica completa validada contra codigo fuente |
| [backlog.md](fase-1/backlog.md) | Tickets pendientes post-Fase 1 con priorizacion |
| [evidence/gates.md](fase-1/evidence/gates.md) | Gates de calidad con comandos reproducibles |
| [evidence/prod-validation.md](fase-1/evidence/prod-validation.md) | Guia de verificacion en produccion (Render) |
| [evidence/commands-output/](fase-1/evidence/commands-output/) | Salidas capturadas de pytest y ruff |

### [Fase 2](fase-2/) — Memoria + Personalizacion

| Documento | Descripcion |
|-----------|-------------|
| [FASE2-CLOSING-REPORT.md](fase-2/FASE2-CLOSING-REPORT.md) | Reporte de cierre: resumen, gates, abort conditions, cambios |
| [FASE2-DESIGN.md](fase-2/FASE2-DESIGN.md) | Decisiones de arquitectura: backends, hashing, sanitizacion |
| [FASE2-IMPLEMENTATION.md](fase-2/FASE2-IMPLEMENTATION.md) | Log de implementacion por ticket (MEM-01 a MEM-15) |
| [backlog.md](fase-2/backlog.md) | Tickets pendientes post-Fase 2 |
| [evidence/gates.md](fase-2/evidence/gates.md) | Gates de calidad con abort conditions |
| [evidence/prod-validation.md](fase-2/evidence/prod-validation.md) | Guia de verificacion en produccion |
| [evidence/commands-output/](fase-2/evidence/commands-output/) | Salidas capturadas (pytest, ruff — baseline y final) |

### [Fase 3](fase-3/) — Pendiente

## Convenciones

### Estructura por fase
```
fase-N/
  FASE{N}-CLOSING-REPORT.md    # Reporte de cierre (obligatorio)
  AUDIT-REPORT-*.md             # Auditoria si aplica
  backlog.md                    # Tickets pendientes al cerrar
  evidence/
    gates.md                    # Gates de calidad verificados
    prod-validation.md          # Verificacion en produccion
    commands-output/            # Salidas capturadas (pytest, ruff, etc.)
```

### Nombrado
- Reportes: `FASE{N}-CLOSING-REPORT.md` (siempre en mayusculas)
- Evidencia: minusculas con guiones (`gates.md`, `prod-validation.md`)
- Salidas de comandos: nombre del comando + sufijo (`pytest-full.txt`, `ruff-check.txt`)

### Como agregar una nueva fase
1. Crear carpeta `fase-N/` con la estructura de arriba
2. Agregar entrada en la tabla "Estado Actual" de este README
3. Agregar seccion en "Indice por Fases"
4. Al cerrar la fase, asegurarse de que tenga: closing report + gates + backlog

## Contexto del Proyecto

- **Proyecto:** Clara — asistente WhatsApp-first para personas vulnerables en Espana
- **Hackathon:** OdiseIA4Good — UDIT (Feb 2026)
- **Stack:** Python 3.11, Flask, Twilio WhatsApp, Gemini 1.5 Flash, Docker, Render
- **Repo:** civicaid-voice
