from datetime import date
from pydantic import BaseModel

class DailyRevenue(BaseModel):
    date: date
    revenue: float
    transactions: int 
    items_sold: int

class ProductPerformance(BaseModel):
    product_id: str
    product_name: str
    category: str
    units_sold: int
    revenue: float