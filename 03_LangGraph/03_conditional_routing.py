from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class SalesState(TypedDict, total=False):
    question: str
    route: str
    answer: str


def classify(state: SalesState):
    question = state["question"].lower()

    if "predict" in question or "forecast" in question:
        return {"route": "ml"}

    if (
        "sales" in question
        or "revenue" in question
        or "product" in question
        or "region" in question
    ):
        return {"route": "data"}

    return {"route": "general"}


def choose_route(state: SalesState):
    return state["route"]


def data_answer(state: SalesState):
    return {"answer": "Route selected: Pandas / Data Science"}


def general_answer(state: SalesState):
    return {"answer": "Route selected: General LLM"}


def ml_answer(state: SalesState):
    return {"answer": "Route selected: Machine Learning"}


builder = StateGraph(SalesState)


builder.add_node("classify", classify)

builder.add_node("data", data_answer)

builder.add_node("general", general_answer)

builder.add_node("ml", ml_answer)


builder.add_edge(START, "classify")


builder.add_conditional_edges(
    "classify", choose_route, {"data": "data", "general": "general", "ml": "ml"}
)


builder.add_edge("data", END)

builder.add_edge("general", END)

builder.add_edge("ml", END)


graph = builder.compile()


questions = [
    "Which product has highest revenue?",
    "Predict next month's revenue.",
    "Explain what Python is.",
]


for question in questions:
    result = graph.invoke({"question": question})

    print()
    print("=" * 60)

    print("Question:", question)

    print("Route:", result["route"])

    print("Answer:", result["answer"])
