from app.core.predictor import Predictor
from app.api.schemas import AnalyzeRequest, AnalyzeResponse
from app.core.monitor import log_analysis


class AnalyzeService:
    def __init__(self, predictor: Predictor = None):
        self.predictor = predictor or Predictor()
        # warmup predictor to ensure model exists
        self.predictor.warmup()

    def analyze_vector(self, request: AnalyzeRequest) -> AnalyzeResponse:
        res = self.predictor.predict(request.vector)
        log_analysis(request.source, res["anomaly_score"], res["is_anomaly"])
        return AnalyzeResponse(source=request.source, anomaly_score=res["anomaly_score"], is_anomaly=res["is_anomaly"], threshold=res["threshold"]) 
