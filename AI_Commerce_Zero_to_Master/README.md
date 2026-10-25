# AI Commerce Zero to Master — Complete Source Bundle v1.4

This repository folder contains the complete v1.4 AI Commerce source payload created in the learning project: Java Spring Boot commerce services, Python FastAPI AI/ML/RAG/MCP services, Docker single-click deployment, customer storefront, learning portal, mock-data generator, data-lake/warehouse pipelines, observability, Kubernetes/environment examples, and tests.

## Why is the source stored as a payload here?

The ChatGPT GitHub connector used for this push can write repository objects but blocked creation of an auto-expanding GitHub Actions workflow. To preserve the **entire source tree losslessly in one atomic push**, the 178 text source/config files are compressed as `tar.xz`, base64-split under `source-payload/`, and accompanied by one-command extractors.

The payload SHA-256 is:

`f41aabe4384d3975d3f98ef76ee503946e2830104975edb0c0295ada1051bbc2`

## Windows — extract all source

Double-click:

`EXTRACT_SOURCE.bat`

or run:

```powershell
powershell -ExecutionPolicy Bypass -File .\EXTRACT_SOURCE.ps1
```

The complete normal source tree will be created at:

`expanded\AI_Commerce_Zero_to_Master\`

## Linux/macOS — extract all source

```bash
chmod +x EXTRACT_SOURCE.sh
./EXTRACT_SOURCE.sh
```

## What is included

- Java Spring Boot commerce core, checkout, payment mock gateway, Kafka publisher and MCP tools
- Python FastAPI ML/DL, recommendation, fraud, churn, pricing, returns, review, RAG, vector stores and MCP
- Customer-facing commerce application UI
- Zero-to-master learning portal
- Docker single-click local stack with selectable ports
- PostgreSQL/pgvector, Redis, Kafka, Qdrant, MLflow, Prometheus, Grafana and OpenTelemetry configs
- Bronze → Silver → Gold historical data pipeline and warehouse examples
- Mock-data generator and service exercise scripts
- Kubernetes overlays for Dev, QA, UAT, Pre-Prod and Prod
- Validation and smoke-test scripts

See `SOURCE_MANIFEST.txt` for the exact 178 files in the payload.
