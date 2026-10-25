#!/bin/sh
set -eu

# The API health endpoint must be able to start independently of Qdrant/pgvector.
# VectorRagService now initializes lazily on the first vector/RAG request.
# This avoids a container-wide startup failure when an external vector backend is
# accepting TCP but is not yet fully ready to serve collection APIs.

echo "Starting AI Python service. VECTOR_BACKEND=${VECTOR_BACKEND:-memory}"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
