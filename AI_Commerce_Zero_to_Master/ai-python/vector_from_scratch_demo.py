from app.llm.providers import HashEmbeddingProvider
from app.vectorstores.base import VectorDocument
from app.vectorstores.in_memory import InMemoryVectorStore


def main() -> None:
    embedding = HashEmbeddingProvider(dimension=64)
    store = InMemoryVectorStore()
    documents = [
        VectorDocument(id="returns", text="Returns are accepted within 30 days for eligible unused products."),
        VectorDocument(id="shipping", text="Standard shipping normally arrives within 3 to 5 business days."),
        VectorDocument(id="warranty", text="Selected electronics include a one year limited hardware warranty."),
    ]
    store.upsert(documents, embedding.embed([doc.text for doc in documents]))

    question = "How long do I have to send a product back?"
    query_vector = embedding.embed([question])[0]
    print("QUESTION:", question)
    print("EMBEDDING DIMENSION:", len(query_vector))
    print("TOP MATCHES:")
    for hit in store.search(query_vector, limit=3):
        print(f"  score={hit.score:.4f} id={hit.id} text={hit.text}")


if __name__ == "__main__":
    main()
