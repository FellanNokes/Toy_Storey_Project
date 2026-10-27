from pathlib import Path

import pandas as pd

from sales import generate_month
from storage import DATA_DIR, save_jsonl
from inventory import simulate_inventory


def export_year(products: pd.DataFrame, year: int, folder: Path = DATA_DIR / "sales") -> None:
    """Create one JSON Lines file per month for sales, plus daily inventory snapshots."""
    all_transactions = []
    for month in range(1, 13):
        transactions = generate_month(products, year, month)
        save_jsonl(transactions, f"sales_{year}_{month:02d}.jsonl", folder)
        all_transactions.extend(transactions)

    snapshots = simulate_inventory(products, all_transactions, year)
    for month in range(1, 13):
        month_snapshots = [s for s in snapshots if s["snapshot_timestamp"][5:7] == f"{month:02d}"]
        save_jsonl(month_snapshots, f"inventory_{year}_{month:02d}.jsonl", DATA_DIR / "inventory")