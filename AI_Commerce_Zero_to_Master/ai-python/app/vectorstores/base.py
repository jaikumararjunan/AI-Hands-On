from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class VectorDocument:
    id: str
    text: str
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class SearchHit:
    id: str
    text: str
    score: float
    metadata: dict[str, object] = field(default_factory=dict)


class VectorStore(Protocol):
    def upsert(self, documents: list[VectorDocument], vectors: list[list[float]]) -> None: ...
    def search(self, query_vector: list[float], limit: int = 5) -> list[SearchHit]: ...
