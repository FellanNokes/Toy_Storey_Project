import json
from pathlib import Path

import dlt 
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SALES_DIR = DATA_DIR / "sales"
PRODUCTS_FILE = DATA_DIR / "products.csv"
DB_FILE = DATA_DIR / "toystore.duckdb"

@dlt.resource(name="sales", write_disposition="merge", primary_key="transaction_id")
def sales():
    for file in sorted(SALES_DIR.glob("sales_*.jsonl")):
        with open(file, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)

@dlt.resource(name="products", write_disposition="replace")
def products():
    yield pd.read_csv(PRODUCTS_FILE).to_dict("records")


def main():
    pipeline = dlt.pipeline(
        pipeline_name="toystore",
        destination=dlt.destinations.duckdb(str(DB_FILE)),
        dataset_name="raw",
    )
    load_info = pipeline.run([products(), sales()])
    print(load_info)

if __name__ == "__main__":
    main()