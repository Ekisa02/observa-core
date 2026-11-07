import sqlite3
import os
from typing import Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "observa.sqlite3")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


class Storage:
    def __init__(self, path: str = None):
        self.path = path or DB_PATH
        self._ensure()

    def _conn(self):
        return sqlite3.connect(self.path)

    def _ensure(self):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                timestamp INTEGER,
                metrics_json TEXT
            )
        """
        )
        conn.commit()
        conn.close()

    def save_metric(self, source: str, timestamp: int, metrics_json: str):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO metrics (source, timestamp, metrics_json) VALUES (?, ?, ?)", (source, timestamp, metrics_json))
        conn.commit()
        conn.close()

    def list_metrics(self, limit: int = 100):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id, source, timestamp, metrics_json FROM metrics ORDER BY id DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return rows
