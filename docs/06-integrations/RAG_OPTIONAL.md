# Integracion RAG — Ruta de Mejora Opcional

> **Resumen en una linea:** Arquitectura actual de base de conocimiento JSON con keyword matching y ruta de migracion hacia busqueda vectorial con FAISS/Chroma.

## Arquitectura actual

Clara usa una **Base de Conocimiento JSON** con keyword matching para busquedas de tramites:

```
Consulta usuario -> kb_lookup (keyword match) -> tramite.json -> KBContext -> prompt LLM
```

- 3 archivos KB: `data/tramites/{imv,empadronamiento,tarjeta_sanitaria}.json`
- Listas de keywords en `src/core/skills/kb_lookup.py`
- Devuelve un dataclass `KBContext` con nombre del tramite, datos, URL fuente y flag de verificacion

Este enfoque funciona bien para el alcance actual (3 tramites, ~15 keywords cada uno).

## Interfaz del Retriever

`src/core/retriever.py` define una interfaz abstracta `Retriever`:

```python
class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        pass
```

Dos implementaciones:
- **JSONKBRetriever** (actual) — envuelve `kb_lookup`, keyword matching
- **VectorRetriever** (stub) — placeholder para busqueda vectorial FAISS/Chroma

La funcion factory `get_retriever()` devuelve la implementacion activa.

## Feature flag

```
RAG_ENABLED=false   # por defecto — usa JSONKBRetriever
RAG_ENABLED=true    # futuro — usaria VectorRetriever
```

## Ruta de mejora: Anadir busqueda vectorial

Cuando la base de conocimiento crezca mas alla de ~10 tramites o el keyword matching resulte insuficiente:

### Paso 1: Elegir un almacen vectorial

| Opcion | Instalacion | Ventajas | Desventajas |
|--------|-------------|----------|-------------|
| FAISS | `pip install faiss-cpu` | Rapido, sin servidor | Sin persistencia nativa |
| Chroma | `pip install chromadb` | Persistente, API sencilla | Dependencia mas pesada |

### Paso 2: Generar embeddings de documentos

```python
# Al arrancar o como paso de build:
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
for tramite_file in Path("data/tramites").glob("*.json"):
    data = json.loads(tramite_file.read_text())
    text = json.dumps(data, ensure_ascii=False)
    embedding = model.encode(text)
    # Almacenar en indice FAISS o coleccion Chroma
```

### Paso 3: Implementar VectorRetriever

```python
class VectorRetriever(Retriever):
    def __init__(self, index_path: str):
        self.index = faiss.read_index(index_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        query_vec = self.model.encode(query)
        distances, indices = self.index.search(query_vec, k=1)
        if distances[0][0] > THRESHOLD:
            return None
        return self._index_to_kb_context(indices[0][0])
```

### Paso 4: Activar

```bash
RAG_ENABLED=true
```

Actualizar `get_retriever()` en `src/core/retriever.py` para devolver `VectorRetriever` cuando la flag este activada.

## Cuando hacer la mejora

- La base de conocimiento supera 10 documentos de tramites
- Los usuarios hacen preguntas que no coinciden con keywords exactos pero son semanticamente relevantes
- Las consultas multilingue necesitan matching semantico en vez de listas de keywords
- La precision cae por debajo del umbral aceptable en la suite de evals

## Referencias

- [Integracion del Toolkit](../02-architecture/TOOLKIT-INTEGRATION.md)
- [Plan de Testing](../04-testing/TEST-PLAN.md)
