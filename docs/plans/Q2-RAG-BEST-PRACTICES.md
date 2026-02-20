# Mejores Practicas RAG 2026 — Resumen Ejecutivo para Q2

> Extraido del reporte completo de mejores practicas modernas para RAG con documentos oficiales y pocas alucinaciones (2026). Basado en documentacion oficial de Microsoft Azure AI Search, Azure AI Foundry, OpenAI, y trabajos academicos recientes.

---

## Principios de Alto Nivel

1. **Grounding obligatorio**: el modelo basa respuestas SOLO en contenido recuperado, no en conocimiento implicito
2. **Fuentes curadas y actualizadas**: la calidad del corpus es el factor #1 para precision
3. **Retrieval robusto**: indices hibridos (BM25 + vectorial) + ranking semantico
4. **Prompts anti-alucinacion**: instrucciones que fuercen uso exclusivo del contexto
5. **Observabilidad**: medir precision, faithfulness y frecuencia de "no answer"

## Chunking (Seccion 4 del reporte)

- Chunking a nivel de **seccion/subseccion/parrafo**, conservando titulo y ruta de encabezados
- Rango: **300-800 tokens** con solapamiento 10-20%
- Metadatos jerarquicos en cada chunk: `doc_title`, `section`, `heading_path`, `page_range`
- NO cortar por longitud fija — respetar estructura del documento
- Indices separados por dominio cuando los contenidos son muy diferentes

## Embeddings y Vector Stores (Seccion 5)

- Mismo modelo para indexar y para queries (coherencia obligatoria)
- Metrica: cosine similarity o dot product segun el motor
- Filtrar por metadatos ANTES de similitud vectorial
- **Busqueda hibrida**: BM25 para terminos exactos + vectorial para semantica
- **Semantic reranking**: cross-encoder cuando sea posible
- **top_k moderado**: 4-8 chunks para equilibrar recall sin diluir contexto
- **Score threshold**: si ningun chunk supera umbral, tratar como "sin contexto"

## Prompting Anti-Alucinacion (Seccion 7)

- Instrucciones explicitas: responder SOLO basado en grounding data
- Reconocer y declarar lagunas: "no puedo responder con la documentacion disponible"
- Requisito de citas: tras cada afirmacion, indicar fuente y seccion
- Respuestas estructuradas: Contexto > Pasos > Referencias
- Limitar verbosidad para no sobrecargar grounding

## Minimizar Alucinaciones (Seccion 8)

- Curar y auditar datos regularmente
- Separar dominios en indices diferentes
- Temperatura baja + sampling conservador
- Score thresholds con fallback (FAQ predefinida o busqueda clasica)
- Human-in-the-loop en primeras fases
- Preferir fuentes estructuradas (DB, knowledge graphs) sobre texto libre

## Manejo de Errores (Seccion 9)

- Modo estricto: "no se encuentra en la documentacion" cuando scores son bajos
- Mensajes utiles: sugerir como reformular o que tipo de info SI esta cubierta
- Registrar queries sin respuesta para mejorar corpus
- Fallbacks: busqueda tradicional > ticketing > soporte humano

## Evaluacion (Seccion 10)

- **Retrieval**: Precision@k, Recall@k, MRR, nDCG
- **Generacion**: faithfulness (todas las afirmaciones trazables a documentos)
- Conjunto de evaluacion: preguntas reales + respuesta esperada + fragmentos de soporte
- Monitorizar: % respuestas con citas, % "no answer", feedback de usuarios
- Logging por turno: query, chunks recuperados (con scores), prompt final, respuesta

## Aplicacion a Clara Q2

Para el modelo de datos + storage de Clara:
- PostgreSQL + pgvector permite busqueda hibrida (tsvector BM25 + vector cosine)
- ProcedureDoc v1 schema ya tiene los metadatos necesarios para filtrado
- Chunking por secciones del ProcedureDoc (descripcion, requisitos, documentos, etc.)
- Embeddings con Gemini text-embedding-004 (768 dims, ya tienen API key)
- Score threshold configurable via feature flag
- Fallback chain: vector → keyword (kb_lookup actual) → "no tengo info"
