from __future__ import annotations

import math

from app.vectorstores.base import SearchHit, VectorDocument


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity implemented from first principles."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimension")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class InMemoryVectorStore:
    """Educational brute-force vector database.

    Complexity is O(N * D) per query. Real vector DBs add indexes such as HNSW to avoid scanning every vector.
    """

    def __init__(self) -> None:
        self._rows: dict[str, tuple[VectorDocument, list[float]]] = {}

    def upsert(self, documents: list[VectorDocument], vectors: list[list[float]]) -> None:
        if len(documents) != len(vectors):
            raise ValueError("documents and vectors must have equal lengths")
        for document, vector in zip(documents, vectors):
            self._rows[document.id] = (document, vector)

    def search(self, query_vector: list[float], limit: int = 5) -> list[SearchHit]:
        ranked = []
        for document, vector in self._rows.values():
            ranked.append(
                SearchHit(
                    id=document.id,
                    text=document.text,
                    score=cosine_similarity(query_vector, vector),
                    metadata=document.metadata,
                )
            )
        return sorted(ranked, key=lambda item: item.score, reverse=True)[:limit]
