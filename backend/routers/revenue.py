from datetime import date

from fastapi import APIRouter

from backend.db import mart, query
from backend.schemas import DailyRevenue

router = APIRouter(prefix="/revenue", tags=["revenue"])


@router.get("/daily", response_model=[DailyRevenue])
def get_daily_revenue(start:date | None = None, end: date | None = None):
    """Revenue per day, optionally filtered by date range."""
    sql = f"select date, revenue, transactions, items_sold from {mart('mart_revenue_daily')} where 1=1"
    params = []
    if start:
        sql += " and date >= ?"
        params.append(start)
    if end:
        sql += " and date <= ?"
        params.append(end)
    return query(sql + " order by date", params)