import json
import time
from app.db.storage import Storage
from app.core.monitor import log_ingest
from app.api.schemas import IngestMetric


class IngestService:
    def __init__(self, storage: Storage = None):
        self.storage = storage or Storage()

    def save_metrics(self, payload: IngestMetric):
        ts = payload.timestamp or int(time.time())
        payload_json = json.dumps(payload.metrics)
        self.storage.save_metric(payload.source, ts, payload_json)
        log_ingest(payload.source, payload.metrics)
