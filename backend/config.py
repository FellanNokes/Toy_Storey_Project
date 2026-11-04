import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_FILE = Path(os.getenv("DUCKDB_PATH", ROOT / "data" / "dev.duckdb"))
MARTS_SCHEMA = os.getenv("MARTS_SCHEMA", "marts")