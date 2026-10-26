from pathlib import Path
import duckdb


ROOT_PATH = Path(__file__).parents[1]
DB_PATH = ROOT_PATH / "ingestion" / "toystore.duckdb"


def load_data(query: str = "SELECT * FROM table"):
    if not DB_PATH.exists():
        raise FileNotFoundError(f"No database found in {DB_PATH}")
    with duckdb.connect(str(DB_PATH), read_only=True) as conn:
        return conn.execute(query).fetchdf()


