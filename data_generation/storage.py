import json
from pathlib import Path

import pandas as pd

def save_csv(df: pd.DataFrame, filename:str, folder: str = "data") -> None:
    """Save a DataFrame as CSV, creating the folder if needed."""
    Path(folder).mkdir(parents=True, exist_ok=True)
    df.to_csv(Path(folder) / filename, index=False)

def save_jsonl(records: list[dict], filename: str, folder str = "data") -> None:
    """ Save a list of dicts as JSON Lines (one JSON object per line)."""
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(Path(folder) / filename, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")