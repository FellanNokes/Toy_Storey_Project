from pathlib import Path

import pandas as pd

from sales import generate_month
from storage import DATA_DIR, save_jsonl


def export_year(products: pd.DataFrame, year: int, folder: Path = DATA_DIR / "sales") -> None:
    """Create one JSON Lines file per month, e.g. sales_2025_01.jsonl"""
    for month in range(1, 13):
        transactions = generate_month(products, year, month)
        save_jsonl(transactions, f"sales_{year}_{month:02d}.jsonl", folder)