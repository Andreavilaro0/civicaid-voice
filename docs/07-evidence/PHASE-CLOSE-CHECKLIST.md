# Checklist de Cierre de Fase — Template

> Copiar este archivo como `PHASE-N-CLOSE.md` al cerrar cada fase.

## Fase: ___
## Fecha cierre: ___
## Owner: ___

### 1. Codigo
- [ ] Todos los archivos del plan estan creados
- [ ] Todos los tests pasan (`pytest tests/ -v`)
- [ ] Lint pasa (`ruff check src/ tests/`)
- [ ] Sin secretos en el codigo (no .env commiteado)

### 2. Deploy
- [ ] Docker build exitoso
- [ ] Deploy en Render exitoso
- [ ] /health retorna JSON OK
- [ ] Twilio webhook configurado
- [ ] Cron-job.org activo (cada 8 min)

### 3. Documentacion
- [ ] PHASE-STATUS.md actualizado
- [ ] PHASE-N-EVIDENCE.md escrito con logs reales
- [ ] Architecture docs actualizados si hubo cambios
- [ ] README.md refleja estado actual

### 4. Notion
- [ ] Phase Releases DB actualizada (estado, commit SHA, URL)
- [ ] Backlog: tareas movidas a "Hecho"
- [ ] Demo & Testing: resultados actualizados con "Pasa"/"Falla"
- [ ] Metricas de latencia registradas

### 5. GitHub
- [ ] Commit con mensaje descriptivo
- [ ] Push a main
- [ ] Tag release: `phase-N-vX.Y`
- [ ] Issues cerrados

### 6. Demo/QA
- [ ] Demo rehearsal completado
- [ ] Video backup grabado
- [ ] Screenshots fallback listos

### 7. Comunicacion
- [ ] Equipo notificado del cierre
- [ ] Siguiente fase planificada
