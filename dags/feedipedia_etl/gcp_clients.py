"""Shared lazy GCP clients using Application Default Credentials (ADC).

On Cloud Run the runtime service account is picked up automatically via ADC.
Locally, run ``gcloud auth application-default login`` or set
``GOOGLE_APPLICATION_CREDENTIALS``. Clients are built once and reused across
the (threaded) extract workers and the transform/load stages.
"""

from __future__ import annotations
from .config import PROJECT_ID, BQ_PROJECT
import threading

from google.cloud import bigquery
from google.cloud import storage

_lock = threading.Lock()
_storage_client: storage.Client | None = None
_bigquery_client: bigquery.Client | None = None


def storage_client() -> storage.Client:
    """Return a lazily-initialised, shared Cloud Storage client."""
    global _storage_client
    if _storage_client is None:
        with _lock:
            if _storage_client is None:
                _storage_client = storage.Client(project=BQ_PROJECT)
    return _storage_client


def bigquery_client() -> bigquery.Client:
    """Return a lazily-initialised, shared BigQuery client."""
    global _bigquery_client
    if _bigquery_client is None:
        with _lock:
            if _bigquery_client is None:
                _bigquery_client = bigquery.Client(project=BQ_PROJECT)
    return _bigquery_client
