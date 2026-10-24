from langchain_ollama import ChatOllama

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

response = model.invoke(
    "Explain gross revenue in simple English."
)

print(type(response))
print(type(response.content))
