# Observa Core Architecture

Observa Core is intentionally small and modular to make it easy to extend. Below are the main components and responsibilities.

Components

- FastAPI HTTP layer (app/main.py, app/api/*)
  - Exposes ingestion and analysis endpoints
  - Basic health and model status endpoints

- Storage layer (app/db/storage.py)
  - Lightweight SQLite-based persistence for ingested metrics
  - Simple API to persist JSON-encoded metrics and retrieve them

- Model layer (app/core/model.py)
  - PyTorch Autoencoder model definition and convenience wrapper
  - Responsible for saving/loading models

- Predictor wrapper (app/core/predictor.py)
  - Handles model lifecycle for inference and normalizes client vectors
  - Provides an anomaly threshold and returns structured prediction info

- Services (app/services/*)
  - Orchestrate ingestion and analysis logic
  - Keep HTTP layer thin

- Utilities (app/utils/*)
  - Logging and monitoring helpers

Design decisions

- The model included is a lightweight autoencoder. It is a placeholder for a production-trained model.
- The predictor auto-pads or truncates vectors to fit the model. In a real product, vector schema should be stable and versioned.
- Storage is SQLite for simplicity. Replace with time-series DB (InfluxDB/Prometheus/ClickHouse) for scale.
- No authentication is included; add OAuth/MTLS/API keys for production.

Deployment

- The application can be containerized using the provided Dockerfile
- For scaling, run multiple replicas behind a load balancer and use a shared storage and model registry
