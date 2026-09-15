"""Configuration for the Feedipedia ETL pipeline."""

import os
from pathlib import Path

# --- Feedipedia API ---
API_BASE_URL = os.getenv(
    "FEEDIPEDIA_API_URL",
    "https://fao-feedipedia-691573242238.europe-west1.run.app/api",
)
API_DEPTH = 1
API_PAGE_SIZE = 100
REQUEST_TIMEOUT_SECONDS = 120
MAX_PAGES = 200

GCS_BUCKET_ENV = os.getenv("FEEDIPEDIA_GCS_BUCKET", "")

# --- BigQuery ---
BQ_PROJECT = os.getenv("GCP_PROJECT", "fao-feedipedia")
BQ_DATASET = os.getenv("BQ_DATASET", "feedipedia")
BQ_LOCATION = os.getenv("BQ_LOCATION", "EU")
BQ_GCS_WRITE_DISPOSITION = "WRITE_TRUNCATE"

# --- Tables loaded by this pipeline (and their load order / group) ---
DIMENSION_TABLES = [
    "dim_parameter_class",
    "dim_category",
    "dim_country",
    "dim_family",
    "dim_license",
    "dim_parameter",
]
ENTITY_TABLES = [
    "dim_dataset",
    "dim_taxon",
    "dim_datasheet",
    "dim_feed",
]
FACT_TABLES = [
    "fct_feed_values",
    "fct_datasheet_feeds",
    "fct_datasheet_fields",
    "fct_datasheet_categories",
    "fct_datasheet_taxa",
    "fct_datasheet_geo",
]
ALL_TABLES = DIMENSION_TABLES + ENTITY_TABLES + FACT_TABLES

SEEDS_DIR = Path(__file__).resolve().parent / "seeds"
SEED_FILES = {
    "countries": "countries.json",
    "parameters": "parameters.json",
    "parameter_classes": "parameter_classes.json",
    "licenses": "licenses.json",
    "region_map": "region_map.json",
}

DAG_SCHEDULE = os.getenv("FEEDIPEDIA_DAG_SCHEDULE", "0 6 * * 0")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_DATA_DIR = Path(
    os.getenv("FEEDIPEDIA_LOCAL_DATA_DIR", str(PROJECT_ROOT / "data"))
)

SQLITE_DB_PATH = Path(
    os.getenv("FEEDIPEDIA_SQLITE_DB", str(LOCAL_DATA_DIR / "feedipedia.db"))
)