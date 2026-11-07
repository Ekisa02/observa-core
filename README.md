# Observa Core

Observa Core is a modular DevOps observability platform built with FastAPI and PyTorch. It provides a simple ingestion API for metrics/events, lightweight storage, and a PyTorch-based anomaly detection predictor (autoencoder) for metric streams.

Key features:
- FastAPI endpoints for ingestion, analysis, and health checks
- Lightweight persistent storage (SQLite) for ingested events
- PyTorch autoencoder-based anomaly scoring for metric vectors
- Modular structure to extend with new detectors, storages, or ingress
- Dockerfile for containerized runs and simple local development

Architecture overview

- app/main.py: FastAPI app entrypoint
- app/api: HTTP routes and request/response schemas
- app/core: Model logic, predictor wrapper, monitoring utilities
- app/services: Ingestion and analysis orchestration
- app/db: Small SQLite persistence for ingested events
- tests: Unit tests for API and model behavior

Flow (high-level):
1. Client POSTs metrics to /ingest/metrics. Metrics are persisted to SQLite.
2. Client POSTs to /analyze with metric vectors. Predictor loads a PyTorch autoencoder and computes reconstruction error (anomaly score).
3. The API returns anomaly score and boolean flag if score exceeds configured threshold.

Installation

Prerequisites:
- Python 3.10+ (recommended)
- pip

Local (venv) quickstart:

1. Clone the repository

   git clone <repo-url>
   cd observa-core

2. Create venv and install dependencies

   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install --upgrade pip
   pip install -r requirements.txt

3. Start the app

   # Start with uvicorn
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. API documentation

   Interactive docs: http://localhost:8000/docs
   Redoc: http://localhost:8000/redoc

Docker

Build and run via Docker:

   docker build -t observa-core:latest .
   docker run -p 8000:8000 --rm observa-core:latest

 or use docker-compose up (see docker-compose.yml)

Usage examples

1) Ingest metrics

   curl -X POST "http://localhost:8000/ingest/metrics" \
     -H "Content-Type: application/json" \
     -d '{"source":"web-server-1","timestamp": 1670000000, "metrics": {"cpu": 0.42, "latency_ms": 120}}'

2) Analyze vector for anomalies

   curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"source":"web-server-1","vector": [0.42, 120]}'

Responses include anomaly_score (reconstruction error) and is_anomaly boolean.

Testing

Run unit tests with pytest:

   pytest -q

Extending the system

- Add additional detectors by creating new classes under app/core and exposing them through app/services/analyze.py
- Replace storage with a more scalable backend by adapting app/db/storage.py
- Add streaming ingestion (Kafka, NATS) by adding a new service in app/services

Security & production notes

- This repository includes a simple CPU PyTorch model and no authentication. Add authentication, rate limiting, and secure model lifecycle before production use.
- For production deployments, prepare models via an offline training pipeline, version models, and use GPU-enabled containers where necessary.

License

MIT (placeholder)
