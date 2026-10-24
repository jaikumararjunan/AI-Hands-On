from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from sales_tools import (
    get_total_revenue,
    get_top_products,
    get_region_revenue
)


model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


agent = create_agent(
    model=model,

    tools=[
        get_total_revenue,
        get_top_products,
        get_region_revenue
    ],

    system_prompt="""
    You are a senior sales data analyst.

    When a question requires information
    from the sales dataset, use the
    appropriate tool.

    Never invent sales numbers.

    Explain the final answer in simple
    business English.
    """
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content":
                "Which 3 products have the highest revenue?"
        }
    ]
})

final_message = (
    result["messages"][-1]
)


print(
    final_message.content
)