import os 

import httpx
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")


def get_daily_revenue() -> pd.DataFrame:
    """Fetch revenue per day from the API."""
    response = httpx.get(f"{API_URL}/revenue/daily", timeout=10)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df["date"] = pd.to_datetime(df["date"])
    return df


def get_product_performance() -> pd.DataFrame:
    """Fetch sales per product from the API."""
    response = httpx.get(f"{API_URL}/products/performance", timeout=10)
    response.raise_for_status()
    return pd.DataFrame(response.json())