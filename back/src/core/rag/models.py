"""SQLAlchemy 2.0 models for Clara RAG knowledge base."""

import uuid
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


# ── procedure_docs ──────────────────────────────────────────────────

class ProcedureDoc(Base):
    __tablename__ = "procedure_docs"

    id = Column(String, primary_key=True)  # slug pattern
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    organismo = Column(String, nullable=False)
    organismo_abrev = Column(String, nullable=True)
    source_url = Column(String, nullable=False)
    source_type = Column(String, nullable=False)  # age/ccaa/local/boe

    territorio_nivel = Column(String, nullable=True)
    territorio_ccaa = Column(String, nullable=True)
    territorio_municipio = Column(String, nullable=True)

    canal = Column(String, nullable=True)
    idioma = Column(String, nullable=False)

    requisitos = Column(JSONB, nullable=True)
    documentos_necesarios = Column(JSONB, nullable=True)
    plazos = Column(JSONB, nullable=True)
    como_solicitar = Column(JSONB, nullable=True)
    donde_solicitar = Column(JSONB, nullable=True)
    tasas = Column(String, nullable=True)

    base_legal = Column(JSONB, nullable=True)
    keywords = Column(JSONB, nullable=False)
    tags = Column(JSONB, nullable=True)

    content_hash = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    completeness_score = Column(Float, nullable=False)

    extracted_at = Column(DateTime, nullable=True)
    verified_at = Column(DateTime, nullable=True)
    verified_by = Column(String, nullable=True)

    last_fetched_at = Column(DateTime(timezone=True), nullable=True)
    fetch_count = Column(Integer, default=0)

    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    chunks = relationship(
        "Chunk", back_populates="procedure", cascade="all, delete-orphan"
    )


# ── chunks ──────────────────────────────────────────────────────────

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    procedure_id = Column(
        String,
        ForeignKey("procedure_docs.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_name = Column(String, nullable=False)
    heading_path = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=False)
    embedding = Column(Vector(768), nullable=True)
    chunk_index = Column(Integer, nullable=False)
    metadata_ = Column("metadata", JSONB, nullable=True)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    procedure = relationship("ProcedureDoc", back_populates="chunks")


# GIN and HNSW indexes are created via raw SQL in scripts/init_db.py
# because SQLAlchemy DDL can't compile REGCONFIG literals or pgvector ops inline.


# ── sources ─────────────────────────────────────────────────────────

class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True)  # slug
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    gov_tier = Column(String, nullable=False)
    priority = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="active")
    last_checked_at = Column(DateTime, nullable=True)
    last_fetched_at = Column(DateTime, nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=True)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )


# ── ingestion_log ──────────────────────────────────────────────────

class IngestionLog(Base):
    __tablename__ = "ingestion_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_id = Column(
        String,
        ForeignKey("procedure_docs.id"),
        nullable=False,
    )
    source_id = Column(
        String,
        ForeignKey("sources.id"),
        nullable=True,
    )
    action = Column(String, nullable=False)  # insert/update/delete
    chunks_created = Column(Integer, nullable=False, default=0)
    chunks_updated = Column(Integer, nullable=False, default=0)
    duration_ms = Column(Integer, nullable=True)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
