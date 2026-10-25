# Single-click local Docker deployment

## Core / lower-memory mode
Double-click `START_LOCAL_DOCKER.bat`.
Starts Java, Python AI, PostgreSQL+pgvector, Redis, Kafka, Qdrant, and the learning site.
Host ports are selected automatically from safe candidate lists and written to `.env.local`.

## Full mode
Double-click `START_FULL_LOCAL_DOCKER.bat`.
Adds Grafana, Prometheus, OpenTelemetry Collector, and MLflow.

## Stop / diagnostics
- `STOP_LOCAL_DOCKER.bat`
- `DOCKER_STATUS.bat`
- destructive reset: `powershell -ExecutionPolicy Bypass -File scripts\reset-local-docker.ps1`

## LLM
The stack works without Ollama for deterministic endpoints and hash embeddings. If Ollama is running on Windows at port 11434, Docker reaches it at `host.docker.internal:11434`.

## v1.2: Auto or interactive host ports

The deployment now has two port modes.

### Automatic (single-click)

Double-click:

- `START_LOCAL_DOCKER.bat`
- `START_FULL_LOCAL_DOCKER.bat`

The launcher tries the preferred port first. If it is occupied, it automatically selects another free port and writes the final value to `.env.local`.

### Interactive (you choose)

Double-click:

- `START_LOCAL_DOCKER_INTERACTIVE.bat`
- `START_FULL_LOCAL_DOCKER_INTERACTIVE.bat`

For every service the launcher shows:

1. preferred port,
2. whether that port is free or occupied,
3. a suggested free port,
4. a prompt where you can type any other free host port.

The launcher also rejects duplicate selections and ports already in use.

Use `SHOW_SELECTED_PORTS.bat` at any time to see the exact ports currently stored in `.env.local`.

### Important Docker concept

Only the **host port** changes. Container ports stay stable. Example:

```text
Windows host 18000 -> ai-python container 8000
Windows host 18080 -> commerce-java container 8080
Windows host 16333 -> qdrant container 6333
```

Internal Docker service-to-service URLs therefore remain stable (`ai-python:8000`, `qdrant:6333`, `postgres:5432`, `kafka:29092`) even when the Windows host ports are changed.

## v1.2 Python startup resilience

The Python API no longer initializes Qdrant/pgvector during module import. The vector backend is created lazily on the first vector/RAG request. This allows `/health`, Swagger, ML and deterministic APIs to come up even while the vector database is still warming up.

If Python is still unhealthy, the launcher now automatically prints `docker compose ps` plus the last Python container log lines rather than only reporting `dependency failed to start`.


ACTUAL APPLICATION UI
---------------------
Preferred application URL: http://localhost:9200
The deployment launcher selects APP_PORT automatically (or interactively) and prints the exact APPLICATION URL.
Use OPEN_APPLICATION.bat to open the selected application port.
The learning portal is separate (preferred http://localhost:9100).
