from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class IngestMetric(BaseModel):
    source: str = Field(..., description="Source identifier, e.g., host or service")
    timestamp: Optional[int] = Field(None, description="UNIX epoch seconds")
    metrics: Dict[str, float] = Field(..., description="Key-value metrics")


class AnalyzeRequest(BaseModel):
    source: str
    vector: List[float]


class AnalyzeResponse(BaseModel):
    source: str
    anomaly_score: float
    is_anomaly: bool
    threshold: float
