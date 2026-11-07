import os
from typing import Dict, Any
from app.core.model import ModelWrapper, ensure_model_exists


class Predictor:
    def __init__(self, model_file: str = None, default_dim: int = 8, threshold: float = 0.1):
        # threshold: anomaly threshold on reconstruction MSE (domain-specific)
        self.model_file = model_file
        self.default_dim = default_dim
        self.threshold = threshold
        self._model = None

    def warmup(self):
        # ensure model file and load
        p = ensure_model_exists(self.model_file, input_dim=self.default_dim)
        self._model = ModelWrapper(input_dim=self.default_dim)
        self._model.load(p)

    def predict(self, vector: list) -> Dict[str, Any]:
        if self._model is None:
            self.warmup()
        # if client vector size differs, auto-adjust by padding/truncation
        vec = self._normalize_vector(vector)
        score = self._model.score(vec)
        return {
            "anomaly_score": score,
            "is_anomaly": score >= self.threshold,
            "threshold": self.threshold,
        }

    def _normalize_vector(self, vector: list) -> list:
        # simple normalize: pad with zeros or truncate to fit model input
        target = self._model.input_dim
        v = list(vector)
        if len(v) < target:
            v = v + [0.0] * (target - len(v))
        elif len(v) > target:
            v = v[:target]
        return v

    def status(self):
        return {"model_file": self.model_file, "loaded": self._model is not None, "threshold": self.threshold}
