import logging
import os
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

from app.services.search import SemanticSearchService
from app.services.recommendation import RecommendationService
from app.services.rag import RagService

logger = logging.getLogger(__name__)

search_service = SemanticSearchService()
recommendation_service = RecommendationService()
rag_service = RagService()


class AgentState(TypedDict, total=False):
    question: str
    route: str
    answer: str
    valid: bool
    retry_count: int


class CommerceAgent:
    def __init__(self):
        self.model = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
            temperature=0,
        )
        builder = StateGraph(AgentState)
        builder.add_node("classify", self.classify)
        builder.add_node("search", self.search)
        builder.add_node("support", self.support)
        builder.add_node("general", self.general)
        builder.add_node("validate", self.validate)
        builder.add_node("fallback", self.fallback)
        builder.add_edge(START, "classify")
        builder.add_conditional_edges(
            "classify",
            lambda s: s["route"],
            {"search": "search", "support": "support", "general": "general"},
        )
        for node in ("search", "support", "general"):
            builder.add_edge(node, "validate")
        builder.add_conditional_edges(
            "validate",
            lambda s: "end" if s.get("valid") else "fallback",
            {"end": END, "fallback": "fallback"},
        )
        builder.add_edge("fallback", END)
        self.graph = builder.compile()

    @staticmethod
    def _route_for(question: str) -> str:
        q = question.lower()
        if any(k in q for k in ["find", "search", "laptop", "headphone", "monitor", "product"]):
            return "search"
        if any(k in q for k in ["return", "refund", "shipping", "warranty", "policy"]):
            return "support"
        return "general"

    def classify(self, state: AgentState):
        return {"route": self._route_for(state["question"])}

    def search(self, state: AgentState):
        results = search_service.search(state["question"], limit=4)
        return {
            "answer": "Product matches:\n"
            + "\n".join(f"- {r['name']} (score={r['score']})" for r in results)
        }

    def support(self, state: AgentState):
        docs = rag_service.retrieve(state["question"], limit=2)
        context = "\n\n".join(d["text"] for d in docs)
        prompt = (
            "Use only this policy context to answer briefly.\n"
            f"CONTEXT:\n{context}\nQUESTION:\n{state['question']}"
        )
        try:
            answer = self.model.invoke(prompt).content
        except Exception:
            answer = "Relevant policy excerpts:\n" + context[:1500]
        return {"answer": answer}

    def general(self, state: AgentState):
        try:
            return {"answer": self.model.invoke(state["question"]).content}
        except Exception:
            return {
                "answer": (
                    "Ollama is unavailable. Commerce APIs and deterministic AI services "
                    "are still available."
                )
            }

    def validate(self, state: AgentState):
        answer = state.get("answer", "").strip()
        return {"valid": bool(answer) and "Traceback" not in answer}

    def fallback(self, state: AgentState):
        return {"answer": "I could not complete the AI workflow. Check Ollama and service health."}

    def _safe_fallback(self, question: str, error: Exception):
        """Return a useful answer even if LangGraph execution itself raises.

        The storefront should not receive HTTP 500 just because an optional LLM or
        graph-runtime path fails. Search and policy questions can still be answered
        with deterministic local services; general questions degrade gracefully.
        """
        route = self._route_for(question)
        logger.exception("Commerce agent graph failed; using deterministic fallback")

        try:
            if route == "search":
                results = search_service.search(question, limit=4)
                answer = "Product matches:\n" + "\n".join(
                    f"- {r['name']} (score={r['score']})" for r in results
                )
            elif route == "support":
                docs = rag_service.retrieve(question, limit=2)
                context = "\n\n".join(d["text"] for d in docs)
                answer = "Relevant policy excerpts:\n" + context[:1500]
            else:
                answer = (
                    "The generative model path is temporarily unavailable. "
                    "Search, recommendations, checkout, payments and policy retrieval "
                    "are still available."
                )
        except Exception:
            logger.exception("Deterministic AI fallback also failed")
            answer = (
                "The AI workflow is temporarily unavailable, but the commerce service "
                "is healthy. Check the Python AI logs for the detailed diagnostic."
            )

        return {
            "route": route,
            "answer": answer,
            "degraded": True,
            "diagnostic": type(error).__name__,
        }

    def ask(self, question: str):
        clean_question = (question or "").strip()
        if not clean_question:
            return {
                "route": "validation",
                "answer": "Please enter a question.",
                "degraded": False,
            }

        try:
            result = self.graph.invoke({"question": clean_question, "retry_count": 0})
            return {
                "route": result.get("route"),
                "answer": result.get("answer", ""),
                "degraded": False,
            }
        except Exception as error:
            return self._safe_fallback(clean_question, error)
