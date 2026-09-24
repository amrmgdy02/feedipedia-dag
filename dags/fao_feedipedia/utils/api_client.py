"""Generic paginated API client for the Feedipedia API (Payload CMS backend)."""

from __future__ import annotations
import time
import logging
from typing import Iterator

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import (
    API_BASE_URL,
    API_DEPTH,
    API_PAGE_SIZE,
    MAX_PAGES,
    REQUEST_TIMEOUT_SECONDS,
)

log = logging.getLogger(__name__)


def _session() -> requests.Session:
    """A session that retries transient failures instead of failing the run.

    The API is itself a Cloud Run service, so a cold start or a brief 502/503 is
    normal rather than exceptional. Retrying here costs seconds; letting it bubble
    up costs a whole task (Airflow) or a whole job (Cloud Run) re-run.
    ``backoff_factor`` gives 1s, 2s, 4s, 8s, 16s between attempts.
    """
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session


def iter_pages(
    resource: str,
    page_size: int = API_PAGE_SIZE,
    depth: int = API_DEPTH,
    max_pages: int = MAX_PAGES,
    delay_seconds: float = 0.2,
) -> Iterator[tuple[int, list[dict]]]:
    """Yield ``(page_number, docs)`` for every page of a Feedipedia collection.

    Args:
        resource: The API resource to fetch.
        page_size: The number of documents to fetch per page.
        depth: The depth of the API response.
        max_pages: The maximum number of pages to fetch.
        delay_seconds: The number of seconds to wait between requests.

    Yields:
        A tuple of ``(page_number, docs)`` for each page of the collection.
    """
    page = 1
    session = _session()

    while True:
        params = {"page": page, "limit": page_size}
        if depth and resource in ["datasheets", "feeds"]:
            params["depth"] = depth

        resp = session.get(
            f"{API_BASE_URL}/{resource}",
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()

        body = resp.json()
        if not isinstance(body, dict) or "docs" not in body:
            raise ValueError(
                f"Unexpected API response for '{resource}' page {page}: {str(body)[:200]}"
            )

        docs = body["docs"] or []
        yield page, docs

        if not body.get("hasNextPage"):
            break
        if page >= max_pages:
            raise RuntimeError(
                f"Reached max_pages={max_pages} for {resource!r} with more pages "
                f"remaining ({body.get('totalPages')} total) — raise MAX_PAGES "
                f"or API_PAGE_SIZE; refusing to load a truncated collection."
            )

        page += 1
        if delay_seconds:
            time.sleep(delay_seconds)


def probe_collection(resource: str) -> dict:
    """Cheaply fingerprint one collection without downloading it.

    Asks for a single document sorted newest-first, which yields the collection's
    latest ``updatedAt`` and its total document count in one request. Together
    those detect every kind of change: an insert or edit moves ``updated_at``, a
    delete moves ``total_docs``, and a delete-plus-insert in the same window still
    moves ``updated_at``.

    Note ``updatedAt`` is CMS *write* time, not editorial time — fine for change
    detection, but never show it to users as "last updated".
    """
    session = _session()
    resp = session.get(
        f"{API_BASE_URL}/{resource}",
        params={"limit": 1, "sort": "-updatedAt"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    resp.raise_for_status()
    body = resp.json()
    docs = body.get("docs") or []
    return {
        "total_docs": body.get("totalDocs"),
        "updated_at": docs[0].get("updatedAt") if docs else None,
    }


def source_fingerprint(resources) -> dict[str, dict]:
    """Fingerprint every collection: ``{resource: {total_docs, updated_at}}``."""
    return {resource: probe_collection(resource) for resource in resources}


def fetch_collection(
    resource: str,
    page_size: int = API_PAGE_SIZE,
    depth: int = API_DEPTH,
    max_pages: int = MAX_PAGES,
    delay_seconds: float = 0.2,
) -> list[dict]:
    """Convenience wrapper returning *all* documents for a resource in memory."""
    docs: list[dict] = []
    for _page, page_docs in iter_pages(
        resource,
        page_size=page_size,
        depth=depth,
        max_pages=max_pages,
        delay_seconds=delay_seconds,
    ):
        docs.extend(page_docs)
    return docs