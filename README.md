# Feedipedia ETL

Airflow DAG that refreshes the **Feedipedia** data set on a weekly schedule:

```
Feedipedia API ──► extract ──► transform ──► load ──► BigQuery / SQLite
```

- **Extract** – Pulls all Feedipedia collections from the public API
   with pagination (`dags/feedipedia_etl/extract.py`,
  `api_client.py`).
- **Transform** – Builds the star-schema staging NDJSON per table
  (dimensions + facts) following the BigQuery design
  (`dags/feedipedia_etl/transform.py`, `schemas.py`).
- **Load** – Loads the transformed rows into a local
  SQLite database (`dags/feedipedia_etl/load.py`).

The pipeline is orchestrated by the `feedipedia_etl` Airflow DAG
(`dags/feedipedia_dag.py`), scheduled weekly on Sundays at 06:00 UTC
(configurable via the `FEEDIPEDIA_DAG_SCHEDULE` env var).

## Project layout

```
├── dags/
│   ├── feedipedia_dag.py        # Airflow DAG definition
│   ├── feedipedia_etl/          # ETL Python package
│   │   ├── api_client.py        # Paginated API client
│   │   ├── config.py            # Endpoints, tables, paths (env-driven)
│   │   ├── extract.py           # Extract tasks (one per collection)
│   │   ├── transform.py         # Staging NDJSON generation
│   │   ├── load.py              # BigQuery / SQLite loaders
│   │   ├── schemas.py           # BigQuery schema definitions
│   │   ├── sqlite_schemas.py    # SQLite table definitions
│   │   ├── seeds/               # Static reference data (countries, params…)
│   │   └── requirements.txt     # Worker/webserver dependencies
├── config/                      # Local Airflow config (not committed)
├── data/                        # Runtime artifacts (raw/staging/DB — gitignored)
├── logs/                        # Airflow logs (gitignored)
└── plugins/                     # Airflow plugins
```

## Data model

Loaded tables are grouped in `dags/feedipedia_etl/config.py`:

- **Dimension tables** – `dim_parameter_class`, `dim_category`, `dim_country`,
  `dim_family`, `dim_license`, `dim_parameter`, `dim_taxon`, `dim_datasheet`, `dim_feed`
- **Entity tables** – 
- **Fact tables** – `fct_feed_values`
