import time
import logging

logger = logging.getLogger(__name__)


def log_ingest(source: str, metrics: dict):
    logger.info("Ingested metrics from %s: %s", source, metrics)


def log_analysis(source: str, score: float, is_anomaly: bool):
    logger.info("Analysis for %s => score=%.6f anomaly=%s", source, score, is_anomaly)
