from fastapi import APIRouter

from backend.db import mart, query
from backend.schemas import ProductPerformance

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/performance", response_model=list[ProductPerformance])
def get_product_performance():
    """Units sold and revenue per product, best sellers first."""
    sql = f"""
        select product_id, product_name, category, units_sold, revenue
        from {mart('mart_product_performance')}
        order by revenue desc
    """
    return query(sql)