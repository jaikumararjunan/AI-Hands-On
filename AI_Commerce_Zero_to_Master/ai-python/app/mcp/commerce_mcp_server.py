from __future__ import annotations

from mcp.server import MCPServer

from app.services.search import SemanticSearchService
from app.services.vector_rag import VectorRagService

mcp = MCPServer("ai-commerce-python")
search_service = SemanticSearchService()
rag_service = VectorRagService()


@mcp.tool()
def search_products(query: str, limit: int = 5) -> list[dict]:
    """Search the demo product catalog."""
    return search_service.search(query, limit=limit)


@mcp.tool()
def retrieve_policy(question: str, limit: int = 3) -> list[dict]:
    """Retrieve the most relevant policy chunks from the configured vector store."""
    return [
        {
            "text": hit.text,
            "score": hit.score,
            "metadata": hit.metadata,
        }
        for hit in rag_service.search(question, limit=limit)
    ]


@mcp.tool()
def answer_policy_question(question: str) -> dict:
    """Run the complete retrieval-augmented generation flow for a support question."""
    return rag_service.answer(question)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8100)
