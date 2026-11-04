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


def get_sales() -> pd.DataFrame:
    """Fetch all transactions from the API."""
    response = httpx.get(f"{API_URL}/sales", timeout=30)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df["date"] = pd.to_datetime(df["date"])
    df["transaction_timestamp"] = (
        pd.to_datetime(df["transaction_timestamp"], utc=True)
        .dt.tz_convert("Europe/Stockholm")
    )
    return df