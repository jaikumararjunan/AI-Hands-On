from pydantic import BaseModel, Field

from langchain_ollama import ChatOllama


class BusinessAnalysis(BaseModel):

    metric: str = Field(
        description="Business metric being discussed"
    )

    explanation: str = Field(
        description="Simple explanation of the metric"
    )

    importance: str = Field(
        description="low, medium, or high"
    )


model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


structured_model = model.with_structured_output(
    BusinessAnalysis
)


result = BusinessAnalysis.model_validate(
    structured_model.invoke(
        """
        Analyze net revenue.
        Explain why management should monitor it.
        """
    )
)


print(result)

print(type(result))

print(result.metric)

print(result.explanation)

print(result.importance)