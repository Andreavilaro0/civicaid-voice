# RAG Integration — Optional Upgrade Path

## Current Architecture

Clara uses a **JSON Knowledge Base** with keyword matching for tramite lookups:

```
User query -> kb_lookup (keyword match) -> tramite.json -> KBContext -> LLM prompt
```

- 3 KB files: `data/tramites/{imv,empadronamiento,tarjeta_sanitaria}.json`
- Keyword lists in `src/core/skills/kb_lookup.py`
- Returns `KBContext` dataclass with tramite name, data, source URL, and verification flag

This approach works well for the current scope (3 tramites, ~15 keywords each).

## Retriever Interface

`src/core/retriever.py` defines an abstract `Retriever` interface:

```python
class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        pass
```

Two implementations:
- **JSONKBRetriever** (current) -- wraps `kb_lookup`, keyword matching
- **VectorRetriever** (stub) -- placeholder for FAISS/Chroma vector search

Factory function `get_retriever()` returns the active implementation.

## Feature Flag

```
RAG_ENABLED=false   # default — uses JSONKBRetriever
RAG_ENABLED=true    # future — would use VectorRetriever
```

## Upgrade Path: Adding Vector Search

When the knowledge base grows beyond ~10 tramites or keyword matching becomes insufficient:

### Step 1: Choose a vector store

| Option | Install | Pros | Cons |
|--------|---------|------|------|
| FAISS | `pip install faiss-cpu` | Fast, no server needed | No persistence built-in |
| Chroma | `pip install chromadb` | Persistent, easy API | Heavier dependency |

### Step 2: Embed documents

```python
# At startup or as a build step:
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
for tramite_file in Path("data/tramites").glob("*.json"):
    data = json.loads(tramite_file.read_text())
    text = json.dumps(data, ensure_ascii=False)
    embedding = model.encode(text)
    # Store in FAISS index or Chroma collection
```

### Step 3: Implement VectorRetriever

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

### Step 4: Enable

```bash
RAG_ENABLED=true
```

Update `get_retriever()` in `src/core/retriever.py` to return `VectorRetriever` when the flag is set.

## When to Upgrade

- Knowledge base exceeds 10 tramite documents
- Users ask questions that don't match exact keywords but are semantically relevant
- Multi-language queries need semantic matching instead of keyword lists
- Accuracy drops below acceptable threshold on eval suite
