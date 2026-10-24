from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class SalesState(TypedDict):
    question: str

    answer: str


def answer_question(state: SalesState) -> dict[str, str]:

    question = state["question"]

    answer = f"You asked: {question}"

    return {"answer": answer}


builder = StateGraph(SalesState)


builder.add_node("answer", answer_question)


builder.add_edge(START, "answer")


builder.add_edge("answer", END)


graph = builder.compile()


result = graph.invoke({"question": "What is net revenue?"})


print(result)
