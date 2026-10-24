import os

from typing import TypedDict

from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, START, END


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")


class SalesState(TypedDict, total=False):
    question: str
    answer: str


model = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)


def general_llm(state: SalesState):
    response = model.invoke(state["question"])

    return {"answer": response.content}


builder = StateGraph(SalesState)


builder.add_node("general_llm", general_llm)


builder.add_edge(START, "general_llm")


builder.add_edge("general_llm", END)


graph = builder.compile()


result = graph.invoke(
    {"question": "Explain the difference between Pandas and NumPy in simple English."}
)


print("Ollama:", OLLAMA_BASE_URL)

print("Model:", OLLAMA_MODEL)

print()

print(result["answer"])
