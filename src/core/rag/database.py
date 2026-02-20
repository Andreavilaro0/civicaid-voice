"""Database engine and session management for Clara RAG."""

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

RAG_DB_URL = os.getenv(
    "RAG_DB_URL",
    "postgresql://clara:clara_dev@localhost:5432/clara_rag",
)

engine = create_engine(RAG_DB_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_session() -> Session:
    """Yield a session; commit on success, rollback on error."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
