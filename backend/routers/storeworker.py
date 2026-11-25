from fastapi import APIRouter
 
from backend.db import mart, query
from backend.schemas import Storeworker
 
router = APIRouter(prefix="/storeworker", tags=["storeworker"])
 
 
@router.get("/", response_model=list[Storeworker])
def get_storeworker_inventory(category: str | None = None, brand: str | None = None,):
    sql = f"""
        select
            product_name,
            category,
            brand,
            age_group,
            age_min,
            age_max,
            unit_price,
            shelf_location,
            quantity_available
        from {mart('mart_storeworker')}
        where 1=1
    """
    params = []

    if category:
        sql += " and category = ?"
        params.append(category)

    if brand:
        sql += " and brand = ?"
        params.append(brand)

    return query(sql, params)