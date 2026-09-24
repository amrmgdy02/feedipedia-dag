from __future__ import annotations

import json
import logging

from .api_client import iter_pages
from .config import GCS_BUCKET, API_PAGE_SIZE
from .gcp_clients import storage_client

log = logging.getLogger(__name__)


def _clear_prefix(bucket, prefix: str) -> int:
    """Delete any pages already staged under ``prefix`` and return how many.

    A rerun of the same ``run_id`` that yields fewer pages than the previous
    attempt would otherwise leave the surplus ``page-NNNNNN.ndjson`` objects
    behind, and the transform — which reads everything under the prefix — would
    ingest both attempts and emit duplicate rows. The prefix belongs to this run
    and is about to be rewritten, so clearing it first is the safe order.
    """
    stale = list(bucket.list_blobs(prefix=f"{prefix}/"))
    if not stale:
        return 0
    log.warning(
        "Clearing %d page(s) already staged under gs://%s/%s before re-extracting",
        len(stale),
        GCS_BUCKET,
        prefix,
    )
    for blob in stale:
        blob.delete()
    return len(stale)


def _stream_resource_to_gcs(resource: str, run_id: str, page_size: int = API_PAGE_SIZE) -> list[str]:

    bucket = storage_client().bucket(GCS_BUCKET)
    prefix = f"raw/{resource}/{run_id}"
    _clear_prefix(bucket, prefix)
    objects: list[str] = []
    for page_no, docs in iter_pages(resource, page_size=page_size):
        lines = "\n".join(json.dumps(d) for d in docs) + ("\n" if docs else "")
        blob_name = f"{prefix}/page-{page_no:06d}.ndjson"
        bucket.blob(blob_name).upload_from_string(
            lines, content_type="application/x-ndjson"
        )
        objects.append(blob_name)
    return objects


def extract_datasheets(run_id: str) -> str:
    """Fetch /api/datasheets (depth=1) and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("datasheets", run_id)
    log.info("Staged %d datasheets pages under raw/datasheets/%s", len(objects), run_id)
    return f"raw/datasheets/{run_id}"


def extract_feeds(run_id: str) -> str:
    """Fetch /api/feeds (depth=1) and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("feeds", run_id)
    log.info("Staged %d feeds pages under raw/feeds/%s", len(objects), run_id)
    return f"raw/feeds/{run_id}"


def extract_taxon(run_id: str) -> str:
    """Fetch /api/taxon and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("taxon", run_id)
    log.info("Staged %d taxon pages under raw/taxon/%s", len(objects), run_id)
    return f"raw/taxon/{run_id}"


def extract_family(run_id: str) -> str:
    """Fetch /api/family and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("family", run_id)
    log.info("Staged %d family pages under raw/family/%s", len(objects), run_id)
    return f"raw/family/{run_id}"


def extract_licenses(run_id: str) -> str:
    """Fetch /api/licenses and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("licenses", run_id)
    log.info("Staged %d licenses pages under raw/licenses/%s", len(objects), run_id)
    return f"raw/licenses/{run_id}"


def extract_categories(run_id: str) -> str:
    """Fetch /api/categories and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("categories", run_id)
    log.info("Staged %d categories pages under raw/categories/%s", len(objects), run_id)
    return f"raw/categories/{run_id}"


def extract_countries(run_id: str) -> str:
    """Fetch /api/countries and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("countries", run_id)
    log.info("Staged %d countries pages under raw/countries/%s", len(objects), run_id)
    return f"raw/countries/{run_id}"


def extract_parameter_classes(run_id: str) -> str:
    """Fetch /api/parameter_classes and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("parameter_classes", run_id)
    log.info(
        "Staged %d parameter_classes pages under raw/parameter_classes/%s",
        len(objects),
        run_id,
    )
    return f"raw/parameter_classes/{run_id}"


def extract_parameters(run_id: str) -> str:
    """Fetch /api/parameters and stage raw pages on GCS."""
    objects = _stream_resource_to_gcs("parameters", run_id)
    log.info("Staged %d parameters pages under raw/parameters/%s", len(objects), run_id)
    return f"raw/parameters/{run_id}"
