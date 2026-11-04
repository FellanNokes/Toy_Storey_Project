import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STEPS = [
    ("Generate data", ["uv", "run", "create_data.py"], ROOT / "data_generation"),
    ("Load raw data with dlt", ["uv", "run", "python", "ingestion/pipeline.py"], ROOT),
    ("Install dbt packages", ["uv", "run", "dbt", "deps"], ROOT / "dbt_core"),
    ("Build dbt models", ["uv", "run", "dbt", "build"], ROOT / "dbt_core"),
]

for name, command, cwd in STEPS:
    print(f"\n=== {name} ===")
    if subprocess.run(command, cwd=cwd).returncode != 0:
        sys.exit(f"Step failed: {name}")

print("\nPipeline done. Start the API and dashboard to see the result.")