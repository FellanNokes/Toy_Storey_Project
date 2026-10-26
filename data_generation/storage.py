import json
from pathlib import Path

import pandas as pd

#TODO: add this to config file to make it cleaner
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def save_csv(df: pd.DataFrame, filename:str, folder: Path = DATA_DIR) -> None:
    """Save a DataFrame as CSV, creating the folder if needed."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    df.to_csv(folder / filename, index=False)

def save_jsonl(records: list[dict], filename: str, folder: Path = DATA_DIR) -> None:
    """ Save a list of dicts as JSON Lines (one JSON object per line)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / filename, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")