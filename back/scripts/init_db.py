"""Initialize the Clara RAG database: create pgvector extension and all tables."""

import sys
import os

# Allow running from project root: python scripts/init_db.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import text
from src.core.rag.database import engine
from src.core.rag.models import Base


def init_db() -> None:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    Base.metadata.create_all(engine)

    # Create special indexes that SQLAlchemy DDL can't compile
    with engine.connect() as conn:
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_chunks_content_fts "
            "ON chunks USING gin (to_tsvector('spanish', content))"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_chunks_embedding_hnsw "
            "ON chunks USING hnsw (embedding vector_cosine_ops) "
            "WITH (m = 16, ef_construction = 64)"
        ))
        conn.commit()

    table_names = list(Base.metadata.tables.keys())
    print(f"Database initialized — {len(table_names)} tables created: {table_names}")
    print("Indexes created: ix_chunks_content_fts (GIN), ix_chunks_embedding_hnsw (HNSW)")


if __name__ == "__main__":
    init_db()
