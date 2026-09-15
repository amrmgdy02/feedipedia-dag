"""Generic paginated API client for the Feedipedia API (Payload CMS backend)."""

from __future__ import annotations
import time
import logging
from typing import Iterator

import requests

from .config import (
    API_BASE_URL,
    API_DEPTH,
    API_PAGE_SIZE,
    MAX_PAGES,
    REQUEST_TIMEOUT_SECONDS,
)

log = logging.getLogger("airflow.task")


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
    session = requests.Session()

    while True:
        params = {"page": page}
        if depth and resource in ("datasheets"):
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

        if not body.get("hasNextPage") or page >= max_pages:
            break

        page += 1
        if delay_seconds:
            time.sleep(delay_seconds)


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