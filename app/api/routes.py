from fastapi import APIRouter, HTTPException
from app.api.schemas import IngestMetric, AnalyzeRequest, AnalyzeResponse
from app.services.ingest import IngestService
from app.services.analyze import AnalyzeService
from typing import Any

router = APIRouter()

ingest_service = IngestService()
analyze_service = AnalyzeService()


@router.post("/ingest/metrics", status_code=201)
async def ingest_metrics(payload: IngestMetric) -> Any:
    try:
        ingest_service.save_metrics(payload)
        return {"status": "accepted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest):
    try:
        resp = analyze_service.analyze_vector(payload)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/model/status")
async def model_status():
    status = analyze_service.predictor.status()
    return status
