from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from sales_tools import get_total_revenue, get_top_products, get_region_revenue


model = ChatOllama(model="llama3.2:3b", temperature=0)


agent = create_agent(
    model=model,
    tools=[get_total_revenue, get_top_products, get_region_revenue],
    system_prompt="""
    You are an enterprise sales
    analytics assistant.

    Use tools whenever the user asks
    about actual sales numbers.

    Never invent business data.

    Explain results in simple English.
    """,
)


questions = [
    "What is our total net revenue?",
    "Which 3 products generate the most revenue?",
    "Which region generates the most revenue?",
    "Explain what net revenue means.",
]


for question in questions:
    print()
    print("=" * 70)

    print("USER:", question)

    result = agent.invoke({"messages": [{"role": "user", "content": question}]})

    answer = result["messages"][-1].content

    print()
    print("ASSISTANT:")

    print(answer)
