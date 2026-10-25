from __future__ import annotations

import json
import os

from app.vectorstores.base import SearchHit, VectorDocument


class PgVectorStore:
    """Postgres + pgvector implementation using cosine distance (<=>)."""

    def __init__(self, dimension: int) -> None:
        import psycopg

        self.psycopg = psycopg
        self.dimension = int(dimension)
        self.dsn = os.getenv(
            "PGVECTOR_DSN",
            "postgresql://commerce:commerce@127.0.0.1:5432/commerce",
        )
        self._initialize()

    def _connect(self):
        return self.psycopg.connect(self.dsn)

    @staticmethod
    def _vector_literal(vector: list[float]) -> str:
        return "[" + ",".join(f"{value:.9g}" for value in vector) + "]"

    def _initialize(self) -> None:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS commerce_embeddings (
                    id text PRIMARY KEY,
                    text_content text NOT NULL,
                    metadata jsonb NOT NULL DEFAULT '{{}}'::jsonb,
                    embedding vector({self.dimension}) NOT NULL
                )
                """
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS commerce_embeddings_hnsw "
                "ON commerce_embeddings USING hnsw (embedding vector_cosine_ops)"
            )

    def upsert(self, documents: list[VectorDocument], vectors: list[list[float]]) -> None:
        with self._connect() as conn, conn.cursor() as cur:
            for document, vector in zip(documents, vectors):
                cur.execute(
                    """
                    INSERT INTO commerce_embeddings (id, text_content, metadata, embedding)
                    VALUES (%s, %s, %s::jsonb, %s::vector)
                    ON CONFLICT (id) DO UPDATE SET
                        text_content = EXCLUDED.text_content,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding
                    """,
                    (
                        document.id,
                        document.text,
                        json.dumps(document.metadata),
                        self._vector_literal(vector),
                    ),
                )

    def search(self, query_vector: list[float], limit: int = 5) -> list[SearchHit]:
        query = self._vector_literal(query_vector)
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, text_content, metadata,
                       1 - (embedding <=> %s::vector) AS cosine_similarity
                FROM commerce_embeddings
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (query, query, limit),
            )
            return [
                SearchHit(
                    id=row[0],
                    text=row[1],
                    metadata=row[2] or {},
                    score=float(row[3]),
                )
                for row in cur.fetchall()
            ]
