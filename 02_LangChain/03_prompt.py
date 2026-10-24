from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


model = ChatOllama(model="llama3.2:3b", temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        You are a senior data analyst.

        Explain answers in simple English.

        Focus on business meaning.
        """,
        ),
        ("human", "{question}"),
    ]
)


chain = prompt | model


response = chain.invoke(
    {"question": "What is the difference between gross revenue and net revenue?"}
)


print(response.content)
