"""Transform tasks: flatten raw Feedipedia NDJSON into per-table staging NDJSON.

Each staging file is NDJSON (one JSON row per line) under
``<LOCAL_DATA_DIR>/staging/<run_id>/{table}.ndjson``. Column names follow the
BigQuery design doc (snake_case). The BigQuery and SQLite loaders both consume
these files.
"""

from __future__ import annotations

import json
from pathlib import Path
from .doc_to_model import ( 
        transform_datasheet_docs, 
        transform_family_docs, 
        transform_feed_docs, 
        transform_taxon_docs, 
        transform_parameter_class_docs, 
        transform_parameter_docs, 
        transform_country_docs, 
        transform_category_docs , 
        transform_license_docs
    )


from .config import LOCAL_DATA_DIR, SEEDS_DIR, SEED_FILES
from .extract import _run_id
from .utils import (
    as_list,
    extract_lexical_plain_text,
    to_float,
    to_int,
)

def _read_dim_dr(path: str) -> list[dict]:
    """Read every NDJSON page under ``<LOCAL_DATA_DIR>/<path>`` into one doc list."""
    dir = Path(LOCAL_DATA_DIR) / path
    docs: list[dict] = []
    for file_path in sorted(dir.glob("*.ndjson")):
        with open(file_path, "r", encoding="utf-8") as f:
            docs.extend(json.loads(line) for line in f if line.strip())
    return docs


def transform_all(**context) -> dict[str, int]:
    """Read raw prefixes, flatten every table, write per-table staging NDJSON."""
    ti = context["ti"]
    log = ti.log
    gcp_conn_id = context.get("gcp_conn_id", "google_cloud_default")
    # GCS bucket is only needed when the original BigQuery loader is used; a local
    # (SQLite) pipeline may run without any GCS configuration.
    try:
        #bucket = _resolve_bucket()
        bucket = None
    except RuntimeError:
        bucket = None
        log.info("No GCS bucket configured; running in local/SQLite mode")
    run_id = _run_id(context)

    datasheets_prefix = ti.xcom_pull(task_ids="extract_datasheets")
    feeds_prefix = ti.xcom_pull(task_ids="extract_feeds")
    taxon_prefix = ti.xcom_pull(task_ids="extract_taxon")
    family_prefix = ti.xcom_pull(task_ids="extract_family")
    categories_prefix = ti.xcom_pull(task_ids="extract_categories")
    licenses_prefix = ti.xcom_pull(task_ids="extract_licenses")
    countries_prefix = ti.xcom_pull(task_ids="extract_countries")
    parameter_classes_prefix = ti.xcom_pull(task_ids="extract_parameter_classes")
    parameters_prefix = ti.xcom_pull(task_ids="extract_parameters")

    if not (datasheets_prefix and taxon_prefix and family_prefix and categories_prefix and licenses_prefix and countries_prefix and feeds_prefix):
        raise RuntimeError(
            "Missing XCom prefixes from extract tasks "
            f"(datasheets={datasheets_prefix!r}, taxon={taxon_prefix!r}, "
            f"family={family_prefix!r})"
        )


    family_docs = _read_dim_dr(family_prefix)
    dim_family = transform_family_docs(family_docs)

    taxon_docs = _read_dim_dr(taxon_prefix)
    dim_taxon = transform_taxon_docs(taxon_docs=taxon_docs)
    
    category_docs = _read_dim_dr(categories_prefix)
    dim_category = transform_category_docs(category_docs=category_docs)
    
    parameter_class_docs = _read_dim_dr(parameter_classes_prefix)
    dim_parameter_class = transform_parameter_class_docs(parameter_class_docs=parameter_class_docs)
    
    parameter_docs = _read_dim_dr(parameters_prefix)
    dim_parameter = transform_parameter_docs(parameter_docs=parameter_docs)
    
    country_docs = _read_dim_dr(countries_prefix)
    dim_country = transform_country_docs(country_docs=country_docs)
    
    license_docs = _read_dim_dr(licenses_prefix)
    dim_license = transform_license_docs(license_docs=license_docs)

    datasheet_docs = _read_dim_dr(datasheets_prefix)
    dim_datasheet = transform_datasheet_docs(datasheet_docs=datasheet_docs)
    
    feed_docs = _read_dim_dr(feeds_prefix)
    dim_feed = transform_feed_docs(feed_docs=feed_docs)

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
        # Fact tables (fct_*) are added here once their transforms exist.
    }

    staging_dir = Path(LOCAL_DATA_DIR) / "staging" / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for table_name, rows in tables.items():
        out_path = staging_dir / f"{table_name}.ndjson"
        with open(out_path, "w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        counts[table_name] = len(rows)
        log.info("Wrote %s: %d rows -> %s", table_name, len(rows), out_path)

    log.info(
        "Transform complete: %d tables staged under %s",
        len(counts),
        staging_dir,
    )
    return counts
    

    