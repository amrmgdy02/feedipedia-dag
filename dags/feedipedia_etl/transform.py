from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from .config import GCS_BUCKET
from .doc_to_model import (
    transform_category_docs,
    transform_country_docs,
    transform_datasheet_docs,
    transform_family_docs,
    transform_feed_docs,
    transform_license_docs,
    transform_parameter_class_docs,
    transform_parameter_docs,
    transform_taxon_docs,
)
from .extract import prefix_for
from .gcp_clients import storage_client
from .schemas import SCHEMAS
from .utils import fill_referenced_by, resolve_bridge_ref_ids

log = logging.getLogger(__name__)

INGESTION_ID_COLUMN = "_data_ingestion_id"
INGESTION_TIME_COLUMN = "_ingestion_time"


RESOURCES = [
    "datasheets",
    "feeds",
    "taxon",
    "family",
    "categories",
    "licenses",
    "countries",
    "parameter_classes",
    "parameters",
]


def _read_dim_dir(path: str) -> list[dict]:
    """Read every NDJSON page under ``gs://<bucket>/<path>/`` into one doc list."""
    bucket = storage_client().bucket(GCS_BUCKET)
    blobs = sorted(bucket.list_blobs(prefix=f"{path}/"), key=lambda b: b.name)
    docs: list[dict] = []
    for blob in blobs:
        content = blob.download_as_bytes().decode("utf-8")
        docs.extend(json.loads(line) for line in content.splitlines() if line.strip())
    return docs


def _stamp_ingestion_audit(tables: dict[str, list[dict]], run_id: str) -> None:
    ingestion_time = datetime.now(timezone.utc).isoformat()

    for table_name, rows in tables.items():
        schema = SCHEMAS.get(table_name)
        if schema is None:
            continue
        columns = {field.name for field in schema}
        if INGESTION_ID_COLUMN not in columns and INGESTION_TIME_COLUMN not in columns:
            continue
        for row in rows:
            if INGESTION_ID_COLUMN in columns:
                row[INGESTION_ID_COLUMN] = run_id
            if INGESTION_TIME_COLUMN in columns:
                row[INGESTION_TIME_COLUMN] = ingestion_time


def transform_all(
    run_id: str,
    prefixes: dict[str, str] | None = None,
) -> dict[str, list[dict]]:
    
    if prefixes is None:
        prefixes = {resource: prefix_for(resource, run_id) for resource in RESOURCES}

    family_docs = _read_dim_dir(prefixes["family"])
    dim_family = transform_family_docs(family_docs)

    taxon_docs = _read_dim_dir(prefixes["taxon"])
    dim_taxon = transform_taxon_docs(taxon_docs=taxon_docs)
    
    dim_taxon = resolve_bridge_ref_ids(dim_taxon, dim_family, "family_id")

    category_docs = _read_dim_dir(prefixes["categories"])
    dim_category = transform_category_docs(category_docs=category_docs)

    parameter_class_docs = _read_dim_dir(prefixes["parameter_classes"])
    dim_parameter_class = transform_parameter_class_docs(
        parameter_class_docs=parameter_class_docs
    )

    parameter_docs = _read_dim_dir(prefixes["parameters"])
    dim_parameter = transform_parameter_docs(parameter_docs=parameter_docs)
    
    dim_parameter = resolve_bridge_ref_ids(dim_parameter, dim_parameter_class, "parameter_class_id")

    country_docs = _read_dim_dir(prefixes["countries"])
    dim_country = transform_country_docs(country_docs=country_docs)

    license_docs = _read_dim_dir(prefixes["licenses"])
    dim_license = transform_license_docs(license_docs=license_docs)

    feed_docs = _read_dim_dir(prefixes["feeds"])
    feed_data = transform_feed_docs(feed_docs=feed_docs)
    
    dim_feed = [fd["feed"] for fd in feed_data]
    
    fct_feed_values = [row for fd in feed_data for row in fd["feed_values"]]
    fct_feed_values = resolve_bridge_ref_ids(fct_feed_values, dim_feed, "feed")
    fct_feed_values = resolve_bridge_ref_ids(fct_feed_values, dim_parameter, "parameter")

    datasheet_docs = _read_dim_dir(prefixes["datasheets"])
    datasheet_data = transform_datasheet_docs(datasheet_docs=datasheet_docs)
    
    dim_datasheet = [ds["datasheet"] for ds in datasheet_data]

    fct_datasheet_geo = [row for ds in datasheet_data for row in ds["datasheet_geo"]]
    fct_datasheet_taxa = [row for ds in datasheet_data for row in ds["datasheet_taxa"]]
    fct_datasheet_categories = [row for ds in datasheet_data for row in ds["datasheet_categories"]]
    fct_datasheet_feeds = [row for ds in datasheet_data for row in ds["datasheet_feeds"]]
    fct_datasheet_fields = [row for ds in datasheet_data for row in ds["datasheet_fields"]]

    fct_datasheet_geo = resolve_bridge_ref_ids(fct_datasheet_geo, dim_country, "country")
    fct_datasheet_taxa = resolve_bridge_ref_ids(fct_datasheet_taxa, dim_taxon, "taxon")
    fct_datasheet_categories = resolve_bridge_ref_ids(fct_datasheet_categories, dim_category, "category")
    fct_datasheet_feeds = resolve_bridge_ref_ids(fct_datasheet_feeds, dim_feed, "feed")

    tables: dict[str, list[dict]] = {
        "dim_parameter_class": dim_parameter_class,
        "dim_category": dim_category,
        "dim_country": dim_country,
        "dim_family": dim_family,
        "dim_license": dim_license,
        "dim_parameter": dim_parameter,
        "dim_taxon": dim_taxon,
        "dim_datasheet": dim_datasheet,
        "dim_feed": dim_feed,
        "fct_datasheet_geo": fct_datasheet_geo,
        "fct_datasheet_taxa": fct_datasheet_taxa,
        "fct_datasheet_categories": fct_datasheet_categories,
        "fct_datasheet_feeds": fct_datasheet_feeds,
        "fct_datasheet_fields": fct_datasheet_fields,
        "fct_feed_values": fct_feed_values,
    }

    fill_referenced_by(tables)
    _stamp_ingestion_audit(tables, run_id=run_id)

    log.info("Transform complete: %d table(s) ready to load", len(tables))
    return tables
