# Toy_Storey_Project


## Configuring `profiles.yml`

dbt uses a file called `profiles.yml` to know how to connect to the database. These files often contain credentials and are therefore normally not committed to Git. This project uses DuckDB, so no passwords are needed.

### 1. Find or create the file

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

### 2. Add the following content

```yaml
dbt_toy_store:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: './dev.duckdb'
      attach:
        - path: '../data/toystore.duckdb'
          alias: toystore
          read_only: true
```

### 3. Verify

```bash
dbt debug
```

All checks should show `OK`. After that you can run `dbt run`.