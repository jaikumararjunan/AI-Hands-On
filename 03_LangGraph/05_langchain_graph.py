from langchain_ollama import ChatOllama
from typing import TypedDict

class SalesState(TypedDict):
    question: str

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

def general_llm(
    state: SalesState
):

    response = model.invoke(
        state["question"]
    )

    return {
        "answer":
            response.content
    }