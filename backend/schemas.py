from datetime import date, datetime
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

class Sale(BaseModel):
    day: int
    month: int
    year: int
    day_of_week: int | str
    date: date
    total_amount: float
    payment_method: str
    transaction_typ: str
    transaction_timestamp: datetime
    customer_id: str | None = None