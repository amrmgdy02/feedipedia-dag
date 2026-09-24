from __future__ import annotations

import io
import json
import logging

from google.api_core.exceptions import NotFound
from google.cloud import bigquery

from .config import (
    BQ_DATASET,
    BQ_GCS_WRITE_DISPOSITION,
    BQ_LOCATION,
    BQ_PROJECT,
)
from .gcp_clients import bigquery_client
from .schemas import SCHEMAS

log = logging.getLogger(__name__)


def _ensure_table(client: bigquery.Client, table_name: str) -> bigquery.TableReference:
    """Return the table ref, creating the table from its schema if missing."""
    if table_name not in SCHEMAS:
        raise ValueError(f"No BigQuery schema defined for table {table_name!r}")
    table_ref = client.dataset(BQ_DATASET, project=BQ_PROJECT).table(table_name)
    try:
        client.get_table(table_ref)
    except NotFound:
        table = bigquery.Table(table_ref, schema=SCHEMAS[table_name])
        client.create_table(table)
        log.info("Created BigQuery table %s", table_name)
    return table_ref


def _rows_to_ndjson(rows: list[dict]) -> bytes:
    """Serialize rows to an in-memory NDJSON blob for a BigQuery load job."""
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


def _check_not_empty(
    tables: dict[str, list[dict]],
    write_disposition: str,
    allow_empty: frozenset[str] | set[str],
) -> None:
    """Refuse to truncate a table down to nothing.
    Empty tables are checked for the whole batch 
    up front so the run fails before any load job has truncated anything.

    Raises:
        RuntimeError: If any table would be truncated to zero rows.
    """
    if write_disposition != "WRITE_TRUNCATE":
        return

    empty = sorted(
        name
        for name, rows in tables.items()
        if name in SCHEMAS and not rows and name not in allow_empty
    )
    if empty:
        raise RuntimeError(
            "Refusing to load: "
            + ", ".join(empty)
            + f" produced 0 rows, and {write_disposition} would replace the "
            "existing BigQuery data with an empty table. Investigate upstream, "
            "or pass allow_empty={...} if a table is legitimately empty."
        )


def load_bigquery_tables(
    tables: dict[str, list[dict]],
    write_disposition: str = BQ_GCS_WRITE_DISPOSITION,
    allow_empty: frozenset[str] | set[str] = frozenset(),
) -> dict[str, int]:
    """Load each table's rows straight into BigQuery (full refresh).

    Args:
        tables: Mapping ``table name -> list of rows`` produced by the transform
            step. There is no staging buffer — rows are loaded from memory.
        write_disposition: BigQuery write disposition (default ``WRITE_TRUNCATE``).
        allow_empty: Table names permitted to load zero rows under
            ``WRITE_TRUNCATE``. Any other empty table fails the run.

    Returns:
        ``table name -> rows loaded``. Tables without a defined schema are
        skipped with a warning.

    Raises:
        RuntimeError: If a table would be truncated to zero rows.
    """
    client = bigquery_client()
    counts: dict[str, int] = {}

    _check_not_empty(tables, write_disposition, allow_empty)

    for table_name, rows in tables.items():
        if table_name not in SCHEMAS:
            log.warning("No BigQuery schema for table %s (skipped)", table_name)
            continue

        table_ref = _ensure_table(client, table_name)
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            schema=SCHEMAS[table_name],
            write_disposition=write_disposition,
        )
        job = client.load_table_from_file(
            io.BytesIO(_rows_to_ndjson(rows)),
            table_ref,
            job_config=job_config,
            location=BQ_LOCATION,
        )
        job.result()  # block until the load completes (raises on failure)

        counts[table_name] = job.output_rows
        log.info("Loaded %d rows into %s", job.output_rows, table_name)

    return counts