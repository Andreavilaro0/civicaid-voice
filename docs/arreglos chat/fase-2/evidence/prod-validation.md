# Fase 2 — Production Validation Guide

## Prerequisites
- Render deploy with env vars set (see render.yaml)
- Redis instance provisioned (Render Redis or external)
- MEMORY_SECRET_SALT set to a strong random value
- FORGET_TOKEN set to a strong random value

## Validation Steps

### 1. Health Check
```bash
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool
```
Expected: `components.memory.status` = "ok" (if MEMORY_ENABLED=true) or "disabled"

### 2. Memory Opt-In Flow
1. Send WhatsApp message: "hola, necesito ayuda"
2. Clara should ask: "¿Quieres que recuerde tu trámite? (Sí/No)"
3. Reply "si" → Clara confirms memory enabled
4. Ask about a tramite → Clara responds normally
5. Ask follow-up → Clara should reference previous context

### 3. Forget Flow
1. Send "olvida mis datos"
2. Clara should respond: "Tus datos han sido eliminados..."
3. Next message should trigger opt-in again

### 4. Admin Forget Endpoint
```bash
curl -X POST https://civicaid-voice.onrender.com/forget \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FORGET_TOKEN" \
  -d '{"phone": "+34600111222"}'
```
Expected: `{"status": "forgotten", "user_id_hash": "..."}`

### 5. Memory Disabled (safe default)
With MEMORY_ENABLED=false (default), no memory operations should occur. Pipeline works exactly as Fase 1.

## Render Environment Variables (new for Fase 2)
| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| MEMORY_ENABLED | No | false | Set to true to enable memory |
| MEMORY_BACKEND | No | dev | Use "redis" for production |
| MEMORY_TTL_DAYS | No | 30 | Days before memory expires |
| MEMORY_SECRET_SALT | Yes (if memory on) | "" | Random secret for user hashing |
| MEMORY_OPTIN_DEFAULT | No | false | If true, memory on by default |
| FORGET_TOKEN | Yes (if memory on) | "" | Token for /forget endpoint |
| REDIS_URL | Yes (if redis) | - | Redis connection URL |
