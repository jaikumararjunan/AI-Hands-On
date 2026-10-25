from fastapi import FastAPI, Query

from app.models import FraudRequest, ForecastRequest, AgentRequest, PricingRequest, ChurnRequest, ReturnRiskRequest, ReviewRequest, MarketingDecisionRequest, CampaignSuggestionRequest
from app.services.search import SemanticSearchService
from app.services.recommendation import RecommendationService
from app.services.fraud import FraudService
from app.services.forecast import ForecastService
from app.services.rag import RagService
from app.services.agent import CommerceAgent
from app.services.pricing import PricingService
from app.services.churn import ChurnService
from app.services.returns import ReturnRiskService
from app.services.reviews import ReviewSentimentService
from app.services.marketing import MarketingService
from app.services.vector_rag import VectorRagService
from app.llm.providers import build_llm_provider
from app.observability import configure_prometheus, configure_opentelemetry

app = FastAPI(title="AI Commerce Intelligence Service", version="0.1.0")

search_service = SemanticSearchService()
recommendation_service = RecommendationService()
fraud_service = FraudService()
forecast_service = ForecastService()
rag_service = RagService()
agent_service = CommerceAgent()
pricing_service = PricingService()
churn_service = ChurnService()
return_risk_service = ReturnRiskService()
review_service = ReviewSentimentService()
marketing_service = MarketingService()
vector_rag_service = None
raw_llm = build_llm_provider()


def get_vector_rag_service():
    """Create the external vector-store client lazily.

    This keeps /health and the deterministic APIs available even if Qdrant/pgvector
    are still warming up during Docker startup. Vector/RAG endpoints initialize the
    selected backend only when they are actually called.
    """
    global vector_rag_service
    if vector_rag_service is None:
        vector_rag_service = VectorRagService()
    return vector_rag_service

configure_prometheus(app)
configure_opentelemetry(app)

@app.get("/health")
def health():
    return {"status": "UP", "service": "ai-python"}

@app.get("/ai/search")
def search(q: str = Query(min_length=2), limit: int = 5):
    return {"query": q, "results": search_service.search(q, limit)}

@app.get("/ai/recommendations/{customer_id}")
def recommendations(customer_id: str, limit: int = 4):
    return {"customer_id": customer_id, "recommendations": recommendation_service.recommend(customer_id, limit)}

@app.post("/ai/fraud/score")
def fraud_score(request: FraudRequest):
    return fraud_service.score(request.model_dump())

@app.post("/ai/forecast")
def forecast(request: ForecastRequest):
    return forecast_service.forecast(request.daily_sales, request.horizon_days)

@app.get("/ai/rag/retrieve")
def rag_retrieve(q: str):
    return {"question": q, "documents": rag_service.retrieve(q)}

@app.post("/ai/agent/ask")
def agent_ask(request: AgentRequest):
    return agent_service.ask(request.question)


@app.post("/ai/pricing/recommend")
def pricing_recommend(request: PricingRequest):
    return pricing_service.recommend(**request.model_dump())

@app.post("/ai/churn/score")
def churn_score(request: ChurnRequest):
    return churn_service.score(request.model_dump())

@app.post("/ai/returns/score")
def return_risk(request: ReturnRiskRequest):
    return return_risk_service.score(request.model_dump())

@app.post("/ai/reviews/analyze")
def review_analyze(request: ReviewRequest):
    return review_service.analyze(request.text)

@app.post("/ai/vector/index")
def vector_index():
    return get_vector_rag_service().index_knowledge()

@app.get("/ai/vector/search")
def vector_search(q: str, limit: int = 4):
    return {
        "question": q,
        "results": [
            {"id": hit.id, "text": hit.text, "score": hit.score, "metadata": hit.metadata}
            for hit in get_vector_rag_service().search(q, limit=limit)
        ],
    }

@app.get("/ai/rag/answer")
def vector_rag_answer(q: str, limit: int = 4):
    return get_vector_rag_service().answer(q, limit=limit)

@app.get("/ai/llm/raw")
def raw_llm_chat(q: str):
    try:
        return {"answer": raw_llm.generate(q)}
    except Exception as error:
        return {"error": str(error), "hint": "Start Ollama and ensure OLLAMA_MODEL exists."}



@app.post("/ai/marketing/decision")
def marketing_decision(request: MarketingDecisionRequest):
    return marketing_service.decide(request.model_dump())

@app.post("/ai/marketing/campaign-suggestions")
def campaign_suggestions(request: CampaignSuggestionRequest):
    return marketing_service.campaign_suggestions(request.objective)
