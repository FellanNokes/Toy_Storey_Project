from pathlib import Path

import duckdb

print("--- Files ---")
print("products.csv:", Path("data/products.csv").exists())
print("sales files:", len(list(Path("data/sales").glob("*.jsonl"))))
print("inventory files:", len(list(Path("data/inventory").glob("*.jsonl"))))

print("\n--- Raw (toystore.duckdb) ---")
with duckdb.connect("data/toystore.duckdb", read_only=True) as con:
    for table in ["products", "sales", "sales__items", "inventory", "inventory__items"]:
        try:
            count = con.execute(f"select count(*) from raw.{table}").fetchone()[0]
            print(f"raw.{table}: {count}")
        except duckdb.CatalogException:
            print(f"raw.{table}: MISSING")

print("\n--- dbt (dev.duckdb) ---")
with duckdb.connect("data/dev.duckdb", read_only=True) as con:
    tables = con.execute(
        "select table_schema, table_name from information_schema.tables "
        "where table_catalog = 'dev' order by 1, 2"
    ).fetchall()
    for schema, table in tables:
        count = con.execute(f"select count(*) from {schema}.{table}").fetchone()[0]
        print(f"{schema}.{table}: {count}")