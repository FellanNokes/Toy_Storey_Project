import duckdb
from fastapi import HTTPException

from backend.config import DB_FILE, MARTS_SCHEMA


def query(sql: str, params: list | None = None) -> list[dict]:
    """Run a read-only query against DuckDB and return rows as dicts."""
    if not DB_FILE.exists():
        raise HTTPException(status_code=503, detail=f"Database not found: {DB_FILE}")
    try:
        with duckdb.connect(str(DB_FILE), read_only=True) as con:
            df = con.execute(sql, params or []).df()
    except duckdb.CatalogException as e:
        raise HTTPException(status_code=503, detail=f"Mart not built yet, run dbt build. {e}")
    except duckdb.IOException as e:
        raise HTTPException(status_code=503, detail=f"Database is locked, is dbt or dlt running? {e}")
    except (duckdb.ParserException, duckdb.BinderException) as e:
        raise HTTPException(status_code=500, detail=f"SQL error: {e}")

    # Pandas turns NULL into NaN, which Pydantic rejects. Convert to None.
    df = df.astype(object).where(df.notna(), None)
    return df.to_dict("records")


def mart(name: str) -> str:
    """Return the fully qualified name of a mart table."""
    return f"{MARTS_SCHEMA}.{name}"