from __future__ import annotations

import hashlib
from pathlib import Path

from app.llm.providers import build_embedding_provider, build_llm_provider
from app.vectorstores.base import VectorDocument
from app.vectorstores.factory import build_vector_store


def chunk_text(text: str, *, chunk_words: int = 160, overlap_words: int = 30) -> list[str]:
    """Simple sliding-window chunker built from scratch."""
    words = text.split()
    if chunk_words <= overlap_words:
        raise ValueError("chunk_words must be greater than overlap_words")
    chunks: list[str] = []
    step = chunk_words - overlap_words
    for start in range(0, len(words), step):
        part = words[start : start + chunk_words]
        if not part:
            break
        chunks.append(" ".join(part))
        if start + chunk_words >= len(words):
            break
    return chunks


class VectorRagService:
    def __init__(self) -> None:
        self.embedding = build_embedding_provider()
        self.vector_store = build_vector_store(self.embedding.dimension)
        self.llm = build_llm_provider()
        self._indexed = False

    def index_knowledge(self) -> dict[str, int | str]:
        knowledge_dir = Path(__file__).resolve().parent.parent / "knowledge"
        documents: list[VectorDocument] = []
        for path in sorted(knowledge_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for chunk_no, chunk in enumerate(chunk_text(text)):
                stable_id = hashlib.sha1(f"{path.name}:{chunk_no}".encode()).hexdigest()
                documents.append(
                    VectorDocument(
                        id=stable_id,
                        text=chunk,
                        metadata={"source": path.name, "chunk": chunk_no},
                    )
                )
        vectors = self.embedding.embed([document.text for document in documents])
        self.vector_store.upsert(documents, vectors)
        self._indexed = True
        return {"documents": len(documents), "backend": type(self.vector_store).__name__}

    def search(self, question: str, limit: int = 4):
        if not self._indexed:
            self.index_knowledge()
        query_vector = self.embedding.embed([question])[0]
        return self.vector_store.search(query_vector, limit=limit)

    def answer(self, question: str, limit: int = 4) -> dict[str, object]:
        hits = self.search(question, limit=limit)
        context = "\n\n".join(
            f"SOURCE={hit.metadata.get('source')} SCORE={hit.score:.4f}\n{hit.text}"
            for hit in hits
        )
        prompt = (
            "Answer the e-commerce support question using only the supplied context. "
            "If the context is insufficient, say so. Cite the source file names.\n\n"
            f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
        )
        try:
            answer = self.llm.generate(prompt, system="You are a grounded e-commerce support assistant.")
        except Exception:
            answer = "LLM unavailable. Retrieved context:\n" + context
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {"id": hit.id, "source": hit.metadata.get("source"), "score": round(hit.score, 4)}
                for hit in hits
            ],
        }
