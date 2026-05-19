from __future__ import annotations
import sqlite3
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from src.config import CACHE_DB_PATH


class Cache:
    def __init__(self, db_path: str = CACHE_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS kline_cache (
                    code TEXT, ktype TEXT, date TEXT,
                    data TEXT, cached_at TIMESTAMP,
                    PRIMARY KEY (code, ktype, date)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quote_cache (
                    code TEXT PRIMARY KEY,
                    data TEXT, cached_at TIMESTAMP
                )
            """)

    def get_kline(self, code: str, ktype: str = "1d",
                  max_age_hours: int = 4) -> pd.DataFrame | None:
        with sqlite3.connect(self.db_path) as conn:
            cutoff = datetime.now() - timedelta(hours=max_age_hours)
            row = conn.execute(
                "SELECT data FROM kline_cache WHERE code=? AND ktype=? AND cached_at>? ORDER BY date DESC LIMIT 1",
                (code, ktype, cutoff)
            ).fetchone()
        if row:
            return pd.read_json(row[0])
        return None

    def set_kline(self, code: str, ktype: str, df: pd.DataFrame):
        data_json = df.to_json()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO kline_cache (code, ktype, date, data, cached_at) VALUES (?,?,?,?,?)",
                (code, ktype, datetime.now().strftime("%Y%m%d"), data_json, datetime.now())
            )

    def get_quote(self, code: str, max_age_minutes: int = 5) -> dict | None:
        with sqlite3.connect(self.db_path) as conn:
            cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
            row = conn.execute(
                "SELECT data FROM quote_cache WHERE code=? AND cached_at>?",
                (code, cutoff)
            ).fetchone()
        return json.loads(row[0]) if row else None

    def set_quote(self, code: str, data: dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO quote_cache (code, data, cached_at) VALUES (?,?,?)",
                (code, json.dumps(data), datetime.now())
            )
