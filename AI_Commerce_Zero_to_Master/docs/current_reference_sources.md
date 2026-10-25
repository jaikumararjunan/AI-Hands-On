# Current reference points (checked 25 Oct 2026)

This file records the public references used to keep the project examples current. The project is intentionally educational: pin versions after you validate them in your own environment.

## Java and Spring

- Spring Boot documentation / stable lines: https://docs.spring.io/spring-boot/
- Spring AI reference documentation: https://docs.spring.io/spring-ai/reference/
- Spring AI MCP documentation and annotations: https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations.html

Project baseline used here:
- Java 21
- Spring Boot 4.1.2
- Spring AI 2.0.1

## Python and API runtime

- FastAPI release notes: https://fastapi.tiangolo.com/release-notes/
- OpenTelemetry Python instrumentation: https://opentelemetry.io/docs/languages/python/instrumentation/
- OpenTelemetry Java: https://opentelemetry.io/docs/languages/java/
- MLflow tracing / GenAI observability: https://mlflow.org/docs/latest/genai/tracing

## Model Context Protocol (MCP)

- MCP official documentation: https://modelcontextprotocol.io/
- Official Python SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP specification: https://modelcontextprotocol.io/specification/

The Python examples in this project use the current MCP v2-style `MCPServer` API and Streamable HTTP. The documentation also explains the older initialize/session and SSE-era concepts so learners can recognize legacy implementations.

## LLMs and embeddings

- Ollama API documentation: https://docs.ollama.com/api
- Ollama embeddings API: https://docs.ollama.com/api/embed
- Ollama model library: https://ollama.com/library

The project keeps the LLM/embedding layer behind small provider interfaces so Ollama can be replaced by hosted providers later without rewriting the RAG/vector logic.

## Vector databases

- Qdrant documentation: https://qdrant.tech/documentation/
- Qdrant concepts: https://qdrant.tech/documentation/concepts/
- pgvector repository / documentation: https://github.com/pgvector/pgvector

The project includes three learning backends:
1. In-memory brute-force cosine similarity (from scratch)
2. Qdrant as a dedicated vector database
3. PostgreSQL + pgvector as relational + vector search

## E-commerce / AI feature references

- Shopify Sidekick: https://help.shopify.com/en/manual/ai-powered-tools/sidekick and https://www.shopify.com/sidekick
- Amazon AI shopping assistant coverage: https://www.aboutamazon.com/news/retail/amazon-rufus-ai-assistant-personalized-shopping-features
- Google shopping / agentic commerce updates: https://blog.google/products-and-platforms/products/shopping/

These public references are used only as inspiration for contemporary capability categories. The source code in this repository is an independent educational reference implementation.


## Release 0.2 commerce/payment/data references (checked 25 Oct 2026)

- Stripe PaymentIntents: https://docs.stripe.com/api/payment_intents
- Stripe idempotent requests: https://docs.stripe.com/api/errors/handling
- Stripe Checkout quickstarts: https://docs.stripe.com/payments/checkout/quickstarts
- Stripe asynchronous payment event guidance: https://docs.stripe.com/payments/save-during-payment
- PCI DSS current document library (v4.0.1 is the published standard at check time): https://www.pcisecuritystandards.org/document_library/
- PCI payment page security/e-skimming guidance: https://blog.pcisecuritystandards.org/new-information-supplement-payment-page-security-and-preventing-e-skimming
- Debezium outbox event router: https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
- Apache Iceberg latest docs: https://iceberg.apache.org/docs/latest/
- Apache Iceberg evolution: https://iceberg.apache.org/docs/latest/evolution/
- OpenTelemetry deployment attributes: https://opentelemetry.io/docs/specs/semconv/registry/attributes/deployment/
- OpenTelemetry resource concepts: https://opentelemetry.io/docs/concepts/resources/
