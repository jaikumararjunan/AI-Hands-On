from __future__ import annotations

import os

from app.vectorstores.base import SearchHit, VectorDocument


class QdrantVectorStore:
    def __init__(self, dimension: int) -> None:
        from qdrant_client import QdrantClient, models

        self.models = models
        self.collection = os.getenv("QDRANT_COLLECTION", "commerce_knowledge")
        self.client = QdrantClient(url=os.getenv("QDRANT_URL", "http://127.0.0.1:6333"))
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE),
            )

    def upsert(self, documents: list[VectorDocument], vectors: list[list[float]]) -> None:
        points = [
            self.models.PointStruct(
                id=document.id,
                vector=vector,
                payload={"text": document.text, "metadata": document.metadata},
            )
            for document, vector in zip(documents, vectors)
        ]
        self.client.upsert(collection_name=self.collection, points=points, wait=True)

    def search(self, query_vector: list[float], limit: int = 5) -> list[SearchHit]:
        response = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )
        hits: list[SearchHit] = []
        for point in response.points:
            payload = point.payload or {}
            hits.append(
                SearchHit(
                    id=str(point.id),
                    text=str(payload.get("text", "")),
                    score=float(point.score),
                    metadata=dict(payload.get("metadata", {})),
                )
            )
        return hits
