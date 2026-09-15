"""Extract tasks: stream raw Feedipedia collections from the API to GCS.

Raw pages are stored as NDJSON (one JSON object per line) under
``raw/<resource>/<run_id>/page-<n>.ndjson``. Only the short GCS prefix is
passed between tasks via XCom -- never the raw payload.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from airflow.models import Variable
from airflow.providers.google.cloud.hooks.gcs import GCSHook

from .api_client import iter_pages
from .config import GCS_BUCKET_ENV, LOCAL_DATA_DIR


# def _resolve_bucket() -> str:
#     bucket = Variable.get("feedipedia_gcs_bucket", GCS_BUCKET_ENV)
#     if not bucket:
#         raise RuntimeError(
#             "No GCS bucket configured. Set Airflow Variable 'feedipedia_gcs_bucket' "
#             "or env 'FEEDIPEDIA_GCS_BUCKET'."
#         )
#     return bucket


def _run_id(context: dict) -> str:
    """Logical execution date, so extract/transform/load share one GCS prefix.

    Falls back to the local wall-clock time when run outside an Airflow context
    (e.g. unit tests).
    """
    ts = context.get("ts_nodash")
    if ts:
        return ts
    ts = context.get("ts")
    if ts:
        return str(ts).replace("-", "").replace(":", "").replace(" ", "").split(".")[0]
    fallback = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    logging.getLogger("airflow.task").warning(
        "No Airflow ts_nodash in context, using wall clock '%s'", fallback
    )
    return fallback


# def _stream_resource_to_gcs(
#     hook: GCSHook,
#     bucket: str,
#     resource: str,
#     run_id: str,
# ) -> list[str]:
#     """Stream every page of resource as NDJSON to GCS; return page object paths."""
#     prefix = f"raw/{resource}/{run_id}"
#     objects: list[str] = []
#     for page_no, docs in iter_pages(resource):
#         lines = "\n".join(json.dumps(d) for d in docs) + ("\n" if docs else "")
#         obj = f"{prefix}/page-{page_no:06d}.ndjson"
#         hook.upload(bucket, obj, data=lines.encode("utf-8"), mime_type="application/x-ndjson")
#         objects.append(obj)
#     return objects


def _save_to_file(
    dir: str,
    resource: str,
    run_id: str,
) -> list[str]:
    from pathlib import Path

    subdir = dir.replace("\\", "/").strip("/")
    base = Path(LOCAL_DATA_DIR) / subdir / resource / run_id
    base.mkdir(parents=True, exist_ok=True)

    objects: list[str] = []
    for page_no, docs in iter_pages(resource):
        lines = "\n".join(json.dumps(d) for d in docs) + ("\n" if docs else "")
        obj = f"{subdir}/{resource}/{run_id}/page-{page_no:06d}.ndjson"
        (base / f"page-{page_no:06d}.ndjson").write_text(lines, encoding="utf-8")
        objects.append(obj)
    return objects


def extract_datasheets(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/datasheets (depth=1) and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "datasheets", run_id)
    objects = _save_to_file("/raw", "datasheets", run_id)
    log.info("Staged %d datasheets pages under raw/datasheets/%s", len(objects), run_id)
    return f"raw/datasheets/{run_id}"


def extract_feeds(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/feeds (depth=1) and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "feeds", run_id)
    objects = _save_to_file("/raw", "feeds", run_id)
    log.info("Staged %d feeds pages under raw/feeds/%s", len(objects), run_id)
    return f"raw/feeds/{run_id}"


def extract_taxon(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/taxon and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "taxon", run_id)
    objects = _save_to_file("/raw", "taxon", run_id)
    log.info("Staged %d taxon pages under raw/taxon/%s", len(objects), run_id)
    return f"raw/taxon/{run_id}"


def extract_family(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/family and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "family", run_id)
    objects = _save_to_file("/raw", "family", run_id)
    log.info("Staged %d family pages under raw/family/%s", len(objects), run_id)
    return f"raw/family/{run_id}"


def extract_licenses(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/licenses and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "licenses", run_id)
    objects = _save_to_file("/raw", "licenses", run_id)
    log.info("Staged %d licenses pages under raw/licenses/%s", len(objects), run_id)
    return f"raw/licenses/{run_id}"


def extract_categories(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/categories and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "categories", run_id)
    objects = _save_to_file("/raw", "categories", run_id)
    log.info("Staged %d categories pages under raw/categories/%s", len(objects), run_id)
    return f"raw/categories/{run_id}"


def extract_countries(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/countries and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "countries", run_id)
    objects = _save_to_file("/raw", "countries", run_id)
    log.info("Staged %d countries pages under raw/countries/%s", len(objects), run_id)
    return f"raw/countries/{run_id}"


def extract_parameter_classes(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/parameter_classes and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "parameter_classes", run_id)
    objects = _save_to_file("/raw", "parameter_classes", run_id)
    log.info(
        "Staged %d parameter_classes pages under raw/parameter_classes/%s",
        len(objects),
        run_id,
    )
    return f"raw/parameter_classes/{run_id}"


def extract_parameters(**context) -> str:  # type: ignore[no-untyped-def]
    """Fetch /api/parameters and stage raw pages on GCS."""
    log = context["ti"].log
    #bucket = _resolve_bucket()
    run_id = _run_id(context)
    #hook = GCSHook()
    #objects = _stream_resource_to_gcs(hook, bucket, "parameters", run_id)
    objects = _save_to_file("/raw", "parameters", run_id)
    log.info("Staged %d parameters pages under raw/parameters/%s", len(objects), run_id)
    return f"raw/parameters/{run_id}"