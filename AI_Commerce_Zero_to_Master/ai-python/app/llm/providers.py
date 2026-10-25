from __future__ import annotations

import hashlib
import math
import os
import re
from dataclasses import dataclass
from typing import Protocol, Sequence

import httpx


class LlmProvider(Protocol):
    def generate(self, prompt: str, *, system: str | None = None) -> str: ...


class EmbeddingProvider(Protocol):
    @property
    def dimension(self) -> int: ...

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


@dataclass
class OllamaLlmProvider:
    """Minimal raw HTTP LLM client. This intentionally avoids LangChain to show the wire-level idea."""

    model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    timeout_seconds: float = 120.0

    def generate(self, prompt: str, *, system: str | None = None) -> str:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = httpx.post(
            f"{self.base_url.rstrip('/')}/api/chat",
            json={"model": self.model, "messages": messages, "stream": False},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]


@dataclass
class OllamaEmbeddingProvider:
    """Embeddings through Ollama's /api/embed endpoint."""

    model: str = os.getenv("OLLAMA_EMBED_MODEL", "all-minilm")
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    timeout_seconds: float = 120.0
    _dimension: int | None = None

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            self._dimension = len(self.embed(["dimension probe"])[0])
        return self._dimension

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        response = httpx.post(
            f"{self.base_url.rstrip('/')}/api/embed",
            json={"model": self.model, "input": list(texts)},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        vectors = response.json()["embeddings"]
        if vectors and self._dimension is None:
            self._dimension = len(vectors[0])
        return vectors


@dataclass
class HashingEmbeddingProvider:
    """Tiny offline embedding for learning vector math; not a semantic production model.

    Tokens are hashed into a fixed-size vector, term counts are accumulated, then L2-normalized.
    It makes the project runnable without downloading any model and lets you inspect every step.
    """

    dimensions: int = 256

    @property
    def dimension(self) -> int:
        return self.dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            bucket = int.from_bytes(digest, "big") % self.dimensions
            vector[bucket] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def build_embedding_provider() -> EmbeddingProvider:
    provider = os.getenv("EMBEDDING_PROVIDER", "hash").lower()
    if provider == "ollama":
        return OllamaEmbeddingProvider()
    return HashingEmbeddingProvider(dimensions=int(os.getenv("HASH_EMBED_DIM", "256")))


def build_llm_provider() -> LlmProvider:
    return OllamaLlmProvider()
