# Validacion en Produccion — Fase 1

## 1. Verificar DEMO_MODE=false en Runtime

### Metodo 1: Observar logs de Render
1. Ir a Render Dashboard → civicaid-voice → Logs
2. Enviar un mensaje WhatsApp que NO este en demo_cache.json (ej: "como pido el paro")
3. Verificar en logs que aparezca:
   - `[CACHE] MISS` (confirma cache miss)
   - `[LLM] OK XXms source=gemini` (confirma que Gemini respondio)
   - `[PIPELINE_RESULT] ... source=llm` (confirma flujo completo)
4. Si en vez de source=llm aparece source=fallback con fallback_reason=demo_mode, DEMO_MODE sigue activo

### Metodo 2: Verificar render.yaml en el repo
```bash
grep -A1 "DEMO_MODE" render.yaml
# Esperado:
#   - key: DEMO_MODE
#     value: "false"
```

### Metodo 3: Verificar env var en Render Dashboard
1. Ir a Render Dashboard → civicaid-voice → Environment
2. Buscar DEMO_MODE
3. **IMPORTANTE:** Si el valor en el Dashboard difiere de render.yaml, el Dashboard prevalece
   - render.yaml solo se aplica en el primer deploy o si se hace "Update from YAML"
   - Los cambios manuales en el Dashboard sobreescriben render.yaml

## 2. Verificar /health Endpoint

```bash
curl https://civicaid-voice.onrender.com/health | python3 -m json.tool
```

Respuesta esperada:
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

Si el servicio esta dormido (free tier): esperar ~30s a que despierte.

## 3. Checklist de Variables de Entorno

Verificar que todas las env vars criticas estan configuradas en Render Dashboard:

| Variable | Esperado | Riesgo si falta |
|----------|----------|-----------------|
| DEMO_MODE | false | Bot solo responde desde cache |
| LLM_LIVE | true | Gemini deshabilitado, solo fallback |
| GEMINI_API_KEY | (secret) | LLM no funciona |
| TWILIO_ACCOUNT_SID | (secret) | No puede enviar respuestas |
| TWILIO_AUTH_TOKEN | (secret) | No puede enviar respuestas + sin validacion de firma |
| WHISPER_ON | false | Flag legacy, debe estar false en prod |
| GUARDRAILS_ON | true | Sin filtrado de contenido peligroso |
| OBSERVABILITY_ON | true | Sin metricas ni trazas |
| STRUCTURED_OUTPUT_ON | false | No activar sin testing previo |
| RAG_ENABLED | false | Stub no funcional |

## 4. Nota sobre Render YAML vs Dashboard

**Regla critica:** En Render, las variables de entorno configuradas manualmente en el Dashboard **siempre prevalecen** sobre las definidas en render.yaml. El archivo render.yaml solo se usa como template inicial.

Para verificar que no hay override:
1. Comparar valores en Dashboard con los de render.yaml
2. Si hay discrepancia, el Dashboard manda
3. Para sincronizar: actualizar manualmente en Dashboard o hacer "Update from YAML" (esto sobreescribe TODO)

## 5. Test Manual de Flujo Completo

Para validar el flujo real end-to-end:

1. Enviar via WhatsApp: "Hola, como solicito el ingreso minimo vital?"
2. Verificar que la respuesta:
   - Contiene informacion sobre el IMV (no un fallback generico)
   - Incluye fuente oficial (URL o telefono)
   - Esta en espanol
   - No es la respuesta de demo_cache (comparar con data/cache/demo_cache.json)
3. Verificar en logs de Render:
   - source=llm o source=cache (ambos son validos; cache si matchea keyword)
   - latency_ms < 10000 (dentro del timeout)
