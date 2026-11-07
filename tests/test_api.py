import os
import json
import tempfile
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_ingest_and_analyze_roundtrip():
    # ingest a small metric payload
    payload = {"source": "test-host", "metrics": {"cpu": 0.1, "mem": 0.2}}
    r = client.post("/ingest/metrics", json=payload)
    assert r.status_code == 201
    assert r.json().get("status") == "accepted"

    # analyze a vector (will be auto-padded to model input size)
    r2 = client.post("/analyze", json={"source": "test-host", "vector": [0.1, 0.2]})
    assert r2.status_code == 200
    body = r2.json()
    assert "anomaly_score" in body
    assert "is_anomaly" in body


def test_model_status():
    r = client.get("/model/status")
    assert r.status_code == 200
    body = r.json()
    assert "loaded" in body
    # loaded may be True depending on startup warmup
