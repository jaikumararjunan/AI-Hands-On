from __future__ import annotations

import os

from app.vectorstores.in_memory import InMemoryVectorStore


def build_vector_store(dimension: int):
    backend = os.getenv("VECTOR_BACKEND", "memory").lower()
    if backend == "qdrant":
        from app.vectorstores.qdrant_store import QdrantVectorStore
        return QdrantVectorStore(dimension)
    if backend == "pgvector":
        from app.vectorstores.pgvector_store import PgVectorStore
        return PgVectorStore(dimension)
    return InMemoryVectorStore()
