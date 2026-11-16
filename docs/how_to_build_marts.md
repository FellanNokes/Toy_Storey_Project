# Adding a mart to the backend
 
How to make a new dbt mart available through the API and the dashboard.
 
## 1. Build the mart
 
Create `dbt_core/models/marts/mart_<name>.sql`. Read only from `fct_*` and `dim_*`, and select columns explicitly. Then:
 
```bash
cd dbt_core && uv run dbt build && cd ..
```
 
## 2. Add a Pydantic model
 
In `backend/schemas.py`. Field names must match the mart's columns. Nullable columns get `| None = None`.
 
```python
class ReorderItem(BaseModel):
    product_id: str
    product_name: str | None = None
    quantity_available: int
    reorder_point: int
```
 
## 3. Add an endpoint
 
In `backend/routers/<area>.py`:
 
```python
from fastapi import APIRouter
 
from backend.db import mart, query
from backend.schemas import ReorderItem
 
router = APIRouter(prefix="/inventory", tags=["inventory"])
 
 
@router.get("/reorder", response_model=list[ReorderItem])
def get_reorder():
    sql = f"""
        select product_id, product_name, quantity_available, reorder_point
        from {mart('mart_reorder')}
    """
    return query(sql)
```
 
Register it in `backend/main.py`:
 
```python
from backend.routers import inventory
 
app.include_router(inventory.router)
```
 
User input (dates, filters) always goes in as `?` parameters, never in the f-string.
 
## 4. Add a client function
 
In `dashboard/api_client.py`:
 
```python
def get_reorder() -> pd.DataFrame:
    response = httpx.get(f"{API_URL}/inventory/reorder", timeout=10)
    response.raise_for_status()
    return pd.DataFrame(response.json())
```
 
Timestamps with time zone: `pd.to_datetime(df["col"], utc=True).dt.tz_convert("Europe/Stockholm")`.
 
## 5. Test
 
```bash
uv run uvicorn backend.main:app --reload
```
 
Open http://localhost:8000/docs and try the endpoint. A `503` or `500` response explains the problem in `detail`.