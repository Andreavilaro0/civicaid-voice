"""Retriever interface for Clara — abstracts KB lookup behind a common interface.
Current: JSONKBRetriever (keyword matching). Future: VectorRetriever (FAISS/Chroma).
Controlled by RAG_ENABLED flag — when false, uses existing kb_lookup directly."""

from abc import ABC, abstractmethod
from typing import Optional
from src.core.models import KBContext


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        pass


class JSONKBRetriever(Retriever):
    """Wraps the existing kb_lookup as a Retriever implementation."""
    def retrieve(self, query: str, language: str) -> Optional[KBContext]:
        from src.core.skills.kb_lookup import kb_lookup
        return kb_lookup(query, language)


# --- PLACEHOLDER: Vector Store Retriever ---
# To upgrade to vector search:
# 1. pip install faiss-cpu (or chromadb)
# 2. Implement VectorRetriever below
# 3. Set RAG_ENABLED=true
# 4. Embed tramite JSON documents at startup
#
# class VectorRetriever(Retriever):
#     def __init__(self, index_path: str):
#         self.index = load_faiss_index(index_path)
#     def retrieve(self, query: str, language: str) -> Optional[KBContext]:
#         # embed query, search index, return top match
#         pass


def get_retriever() -> Retriever:
    """Factory — returns the active retriever based on config."""
    # Future: check config.RAG_ENABLED and return VectorRetriever
    return JSONKBRetriever()
