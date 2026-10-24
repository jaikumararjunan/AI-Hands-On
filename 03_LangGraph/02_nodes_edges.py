from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str

    cleaned_question: str

    answer: str


def clean_question(state: State):

    cleaned = state["question"].strip().lower()

    return {"cleaned_question": cleaned}


def create_answer(state: State):

    question = state["cleaned_question"]

    return {"answer": f"Processing: {question}"}


builder = StateGraph(State)


builder.add_node("clean", clean_question)

builder.add_node("answer", create_answer)


builder.add_edge(START, "clean")

builder.add_edge("clean", "answer")

builder.add_edge("answer", END)


graph = builder.compile()


result = graph.invoke({"question": "   WHAT IS REVENUE?   "})


print(result)
