from __future__ import annotations

import threading

from google.cloud import bigquery
from google.cloud import storage

from .config import BQ_PROJECT

_lock = threading.Lock()
_storage_client: storage.Client | None = None
_bigquery_client: bigquery.Client | None = None
_credentials = None
_project: str | None = None


def configure(credentials=None, project: str | None = None) -> None:
    global _credentials, _project, _storage_client, _bigquery_client
    with _lock:
        _credentials = credentials
        _project = project
        _storage_client = None
        _bigquery_client = None


def storage_client() -> storage.Client:
    """Return a lazily-initialised, shared Cloud Storage client."""
    global _storage_client
    if _storage_client is None:
        with _lock:
            if _storage_client is None:
                _storage_client = storage.Client(
                    project=_project or BQ_PROJECT,
                    credentials=_credentials,
                )
    return _storage_client


def bigquery_client() -> bigquery.Client:
    """Return a lazily-initialised, shared BigQuery client."""
    global _bigquery_client
    if _bigquery_client is None:
        with _lock:
            if _bigquery_client is None:
                _bigquery_client = bigquery.Client(
                    project=_project or BQ_PROJECT,
                    credentials=_credentials,
                )
    return _bigquery_client
