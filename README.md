# Toy_Storey_Project

End-to-end data pipeline for a fictional toy store: generated sales and inventory data is loaded with dlt, transformed with dbt and served through a FastAPI backend to a Streamlit dashboard.

```
data_generation  →  data/*.jsonl  →  dlt  →  toystore.duckdb (raw)  →  dbt  →  dev.duckdb (marts)  →  FastAPI  →  Streamlit
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.13 (installed automatically by uv)

Install all dependencies from the project root:

```bash
uv sync
```

All commands below are run from the project root unless stated otherwise.

## 1. Generate data

The generator acts as the store's register and inventory system. It writes one year of sales and daily inventory snapshots as JSON Lines, plus the product catalogue as CSV.

```bash
cd data_generation
uv run create_data.py
cd ..
```

Check that these exist:

- `data/products.csv`
- `data/sales/sales_YYYY_MM.jsonl` (12 files)
- `data/inventory/inventory_YYYY_MM.jsonl` (12 files)

The same seed is used every time, so the output is identical on every run.

## 2. Load raw data with dlt

dlt reads the files and loads them as-is into `data/toystore.duckdb`, in the schema `raw`.

### 2.1 Run the pipeline

```bash
uv run python ingestion/pipeline.py
```

The first run creates `data/toystore.duckdb`. dlt prints a summary ending with `LOADED and contains no failed jobs`.

### 2.2 Verify the tables

```bash
uv run python -c "import duckdb; con = duckdb.connect('data/toystore.duckdb', read_only=True); con.sql('show all tables').show()"
```

You should see these tables in the `raw` schema:

| Table | Content |
|---|---|
| `products` | Product catalogue |
| `sales` | One row per receipt |
| `sales__items` | One row per receipt line, linked to `sales` via `_dlt_parent_id` → `_dlt_id` |
| `inventory` | One row per daily snapshot, store details flattened to `store__*` |
| `inventory__items` | One row per product and snapshot, linked to `inventory` via `_dlt_parent_id` → `_dlt_id` |
| `_dlt_*` | dlt's internal bookkeeping, leave as is |

### 2.3 Re-running

`sales` and `inventory` use `merge` on `transaction_id` and `snapshot_id`, and `products` uses `replace`. Running the pipeline again does not create duplicates.

To start from scratch, delete `data/toystore.duckdb` and run steps 1 and 2 again.

## 3. Transform with dbt

dbt reads the raw tables from `toystore.duckdb` (attached read-only) and writes staging, warehouse and mart models to `data/dev.duckdb`.

### 3.1 Configure `profiles.yml`

dbt uses a file called `profiles.yml` to know how to connect to the database. These files often contain credentials and are therefore normally not committed to Git. This project uses DuckDB, so no passwords are needed.

#### Find or create the file

By default, dbt looks for `profiles.yml` in `~/.dbt/` (your home directory). If a `profiles.yml` exists in the project folder, dbt uses that one first.

Open the file in your editor of choice, for example:

```bash
code ~/.dbt/profiles.yml
```

If the file or folder doesn't exist, create them:

```bash
mkdir -p ~/.dbt
touch ~/.dbt/profiles.yml
```

#### Add the following content

```yaml
dbt_toy_store:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: '../data/dev.duckdb'
      attach:
        - path: '../data/toystore.duckdb'
          alias: toystore
          read_only: true
```

The paths are relative to the folder dbt is run from, so **always run dbt from `dbt_core/`**.

#### Verify

```bash
cd dbt_core
uv run dbt debug
```

All checks should show `OK`.

### 3.2 Build the models

From `dbt_core/`:

```bash
uv run dbt build
cd ..
```

`dbt build` runs all models and tests. The result ends up in `data/dev.duckdb`:

| Schema | Content |
|---|---|
| `staging` | Cleaned source models (`src_*`) |
| `warehouse` | Facts and dimensions (`fct_*`, `dim_*`) |
| `marts` | Models used by the API (`mart_*`) |

## 4. Start the backend (FastAPI)

The API reads the marts from `data/dev.duckdb` in read-only mode.

```bash
uv run uvicorn backend.main:app --reload
```

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Optional environment variables:

| Variable | Default | Description |
|---|---|---|
| `DUCKDB_PATH` | `data/dev.duckdb` | Database the API reads from |
| `MARTS_SCHEMA` | `marts` | Schema where the marts are |

If an endpoint returns `503`, the response's `detail` explains why: the database or mart doesn't exist yet (run `dbt build`), or the database is locked by another process.

## 5. Start the dashboard (Streamlit)

Keep the backend running and open a second terminal:

```bash
uv run streamlit run dashboard/Toy_Storey.py
```

The dashboard opens at http://localhost:8501. It only talks to the API, never directly to the database.

To point the dashboard to another API, set `API_URL` (default `http://localhost:8000`).

## Run everything from scratch

```bash
uv sync
cd data_generation && uv run create_data.py && cd ..
uv run python ingestion/pipeline.py
cd dbt_core && uv run dbt build && cd ..
uv run uvicorn backend.main:app --reload            # terminal 1
uv run streamlit run dashboard/Toy_Storey.py        # terminal 2
```

## Troubleshooting

- **`Database is locked`**: DuckDB allows only one process to write at a time. Close notebooks or tools that have a `.duckdb` file open without `read_only=True`, and don't run dlt or dbt while the API is reading.
- **Changes in `dashboard/` don't show up**: stop Streamlit (Ctrl+C) and start it again. Imported modules are not always reloaded automatically.
- **Old data in the dashboard**: clear Streamlit's cache with **C** or from the menu in the top right corner.