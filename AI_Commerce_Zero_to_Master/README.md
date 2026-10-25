# AI Commerce Zero to Master — Direct Source Tree v1.4

This folder contains the **actual browsable source files directly in GitHub**. No extraction step, base64 payload, tar archive, or source-payload indirection is required.

## Main source areas

- `backend-java/commerce-core/` — Spring Boot commerce, checkout, payments, Kafka and Java MCP tools
- `ai-python/` — FastAPI ML/DL, search, recommendation, fraud, churn, pricing, RAG, vector stores, LangGraph agent and Python MCP
- `commerce-app/` — actual customer-facing e-commerce application UI
- `learning-site/` — zero-to-master learning portal
- `mock-data/` — cross-service synthetic data generator, validation and streaming events
- `data-platform/` — Bronze → Silver → Gold → warehouse/features learning pipeline
- `infra/` — Docker Compose, PostgreSQL/pgvector, Redis, Kafka, Qdrant, MLflow, OpenTelemetry, Prometheus, Grafana and Kubernetes examples
- `environments/` — Dev, QA, UAT, Pre-Prod and Prod configuration examples
- `contracts/` — event and agent/tool schemas
- `scripts/` — single-click Docker launch, selectable ports, validation, smoke tests and labs

## Local Docker deployment

Recommended full interactive deployment:

```text
START_FULL_LOCAL_DOCKER_INTERACTIVE.bat
```

This lets you select/fallback host ports and starts the actual storefront, Java API, Python AI service, data services and observability stack.

Preferred URLs when ports are free:

- Application: `http://localhost:9200`
- Learning portal: `http://localhost:9100`
- Java health: `http://localhost:8080/actuator/health`
- Python Swagger: `http://localhost:8000/docs`

Use `DOCKER_STATUS.bat` for status/log diagnostics and `OPEN_APPLICATION.bat` to open the selected application URL.

## Important current fixes

- Java `RestClient.Builder` is explicitly configured in `backend-java/commerce-core/src/main/java/com/example/aicommerce/config/HttpClientConfig.java`.
- Python vector/RAG initialization is lazy so API health is not blocked by Qdrant startup timing.
- Docker Java health check uses `/actuator/health`.
- Host ports can be automatic or interactively selected.
- Customer application and learning portal are separate services/URLs.

All data and payment records in this project are synthetic learning data only.
