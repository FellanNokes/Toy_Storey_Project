from fastapi import APIRouter

from backend.db import mart, query
from backend.schemas import Sale

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("", response_model=list[Sale])
def get_sales():
    """One row per transaction with date attributes."""
    sql = f"""
        select day, month, year, day_of_week, date, total_amount,
          payment_method, transaction_type, transaction_timestamp, customer_id
        from {mart('mart_sales')}
        order by transaction_timestamp
    """
    return query(sql)