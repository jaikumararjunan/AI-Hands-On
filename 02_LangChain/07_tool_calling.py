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

model_with_tools = model.bind_tools([
    get_total_revenue,
    get_top_products,
    get_region_revenue
])

response = model_with_tools.invoke(
    """
    Which three products generate
    the highest revenue?

    Use the appropriate sales tool.
    """
)


print(response)


print(
    response.tool_calls
)

