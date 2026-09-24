"""Configuration for the Feedipedia ETL pipeline."""

import os
from datetime import datetime, timezone
from pathlib import Path


def make_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


API_BASE_URL = os.getenv(
    "FEEDIPEDIA_API_URL",
    "https://fao-feedipedia-691573242238.europe-west1.run.app/api",
)
API_DEPTH = 1
API_PAGE_SIZE = 100
REQUEST_TIMEOUT_SECONDS = 120
MAX_PAGES = 200

PROJECT_ID = os.getenv("GCP_PROJECT", "fao-dwh-review")

BQ_PROJECT = os.getenv("GCP_PROJECT", "fao-dwh-review")
BQ_DATASET = os.getenv("BQ_DATASET", "feedipedia")
BQ_LOCATION = os.getenv("BQ_LOCATION", "europe-west1")
BQ_GCS_WRITE_DISPOSITION = "WRITE_TRUNCATE"

GCS_BUCKET = os.getenv("FEEDIPEDIA_GCS_BUCKET", "fao-dwh-review-feedipedia-etl")
# Top-level namespace inside the (shared) bucket, so this pipeline's raw pages
# all sit under one prefix: gs://<bucket>/<GCS_PREFIX>/<collection>/<run_id>/
GCS_PREFIX = os.getenv("FEEDIPEDIA_GCS_PREFIX", "fao_feedipedia")

DIMENSION_TABLES = [
    "dim_parameter_class",
    "dim_category",
    "dim_country",
    "dim_family",
    "dim_license",
    "dim_parameter",
]
ENTITY_TABLES = [
    #"dim_dataset",
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
