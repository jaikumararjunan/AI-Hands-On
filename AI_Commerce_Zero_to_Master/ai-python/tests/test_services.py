from app.services.search import SemanticSearchService
from app.services.recommendation import RecommendationService
from app.services.forecast import ForecastService


def test_search_returns_results():
    assert SemanticSearchService().search("laptop for AI", 2)


def test_recommendation_returns_results():
    assert RecommendationService().recommend("C100", 2)


def test_forecast_size():
    result = ForecastService().forecast([10, 11, 12, 13, 14, 15, 16], 3)
    assert len(result["forecast"]) == 3


def test_in_memory_vector_store_orders_by_cosine():
    from app.vectorstores.base import VectorDocument
    from app.vectorstores.in_memory import InMemoryVectorStore

    store = InMemoryVectorStore()
    store.upsert(
        [VectorDocument(id="a", text="A"), VectorDocument(id="b", text="B")],
        [[1.0, 0.0], [0.0, 1.0]],
    )
    hits = store.search([0.9, 0.1], limit=2)
    assert hits[0].id == "a"
    assert hits[0].score > hits[1].score


def test_chunk_text_has_overlap_and_no_empty_chunks():
    from app.services.vector_rag import chunk_text

    words = " ".join(f"w{i}" for i in range(100))
    chunks = chunk_text(words, chunk_words=30, overlap_words=5)
    assert chunks
    assert all(chunk.strip() for chunk in chunks)
    assert len(chunks) >= 4


def test_agent_returns_deterministic_fallback_when_graph_raises(monkeypatch):
    from app.services.agent import CommerceAgent

    agent = CommerceAgent()

    def fail_graph(_state):
        raise RuntimeError("simulated graph runtime failure")

    monkeypatch.setattr(agent.graph, "invoke", fail_graph)
    result = agent.ask("I need a laptop for local AI development and a monitor")

    assert result["degraded"] is True
    assert result["route"] == "search"
    assert "Product matches" in result["answer"]
    assert result["diagnostic"] == "RuntimeError"
