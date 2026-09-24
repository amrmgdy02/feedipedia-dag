from __future__ import annotations

import argparse
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

_DAGS_DIR = Path(__file__).resolve().parent
if str(_DAGS_DIR) not in sys.path:
    sys.path.insert(0, str(_DAGS_DIR))

from feedipedia_etl import extract as extract_mod
from feedipedia_etl import load as load_mod
from feedipedia_etl import transform as transform_mod
from feedipedia_etl.config import GCS_BUCKET, make_run_id
from feedipedia_etl.gcp_clients import storage_client

log = logging.getLogger("feedipedia_etl.main")

EXTRACT_RESOURCES = {
    "datasheets": extract_mod.extract_datasheets,
    "feeds": extract_mod.extract_feeds,
    "taxon": extract_mod.extract_taxon,
    "family": extract_mod.extract_family,
    "categories": extract_mod.extract_categories,
    "licenses": extract_mod.extract_licenses,
    "countries": extract_mod.extract_countries,
    "parameter_classes": extract_mod.extract_parameter_classes,
    "parameters": extract_mod.extract_parameters,
}


def _get_max_workers() -> int:
    raw = os.getenv("FEEDIPEDIA_get_max_workers", "")
    if raw:
        try:
            workers = int(raw)
            if workers >= 1:
                return workers
        except ValueError:
            pass
        log.warning("Ignoring invalid FEEDIPEDIA_get_max_workers=%r", raw)
    return len(EXTRACT_RESOURCES)


def run_etl(run_id: str | None = None) -> dict[str, int]:
    """Extract -> transform -> load. Returns per-table load counts."""
    run_id = run_id or make_run_id()
    log.info("Run id: %s", run_id)

    max_workers = _get_max_workers()
    log.info(
        "Extracting %d collection(s) with %d worker(s), run id %s",
        len(EXTRACT_RESOURCES),
        max_workers,
        run_id,
    )

    prefixes: dict[str, str] = {}
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(extract_fn, run_id=run_id): resource
            for resource, extract_fn in EXTRACT_RESOURCES.items()
        }
        for future in as_completed(futures):
            resource = futures[future]
            try:
                prefixes[resource] = future.result()
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{resource}: {exc}")
                log.exception("Extract failed for %s", resource)

    if failures:
        raise RuntimeError("Extract failed for: " + "; ".join(failures))

    for resource in EXTRACT_RESOURCES:
        prefix = prefixes[resource]
        blobs = list(
            storage_client().bucket(GCS_BUCKET).list_blobs(prefix=f"{prefix}/")
        )
        if not blobs:
            raise RuntimeError(
                f"Extract produced no staged pages for {resource!r}: "
                f"gs://{GCS_BUCKET}/{prefix}"
            )
        log.info(
            "Extracted %s -> %d page(s) under gs://%s/%s",
            resource,
            len(blobs),
            GCS_BUCKET,
            prefix,
        )

    tables = transform_mod.transform_all(run_id=run_id, prefixes=prefixes)
    log.info("Transform complete: %d table(s) ready to load", len(tables))

    loaded = load_mod.load_bigquery_tables(tables)
    log.info("Load complete: %d table(s) loaded into BigQuery", len(loaded))
    return loaded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="feedipedia-etl",
        description="Run the Feedipedia ETL standalone (Cloud Run job).",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Logical run id, e.g. 20240101T060000 (default: UTC now).",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(
            logging, os.getenv("FEEDIPEDIA_LOG_LEVEL", "INFO").upper(), logging.INFO
        ),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        loaded = run_etl(run_id=args.run_id)
    except Exception:
        log.exception("Feedipedia ETL run failed")
        return 1

    log.info("ETL run completed successfully: %d table(s) loaded", len(loaded))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
