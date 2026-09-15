"""Utility helpers: Lexical rich-text extraction and small JSON helpers."""

from __future__ import annotations

from typing import Any


def lexical_to_text(node: Any) -> str:
    """Extract plain text from a Lexical rich-text JSON tree (datasheet fields).

    Feedipedia stores field content as Lexical editor JSON like::

        {"root": {"children": [{"type": "paragraph",
                                "children": [{"type": "text", "text": "..."}]}]}}

    Args:
        node: A Lexical JSON node (dict), a list of nodes, or a plain string.

    Returns:
        Concatenated plain text across all text nodes.
    """
    if node is None:
        return ""

    if isinstance(node, list):
        return "\n".join(lexical_to_text(n) for n in node)

    if isinstance(node, dict):
        # Field content is stored as {"root": {lexical tree}}.
        root = node.get("root")
        if isinstance(root, dict):
            return lexical_to_text(root)
        node_type = node.get("type")
        if node_type in ("root", "paragraph", "list", "quote"):
            children = node.get("children")
            return lexical_to_text(children) if children else ""
        text = node.get("text")
        if text is not None:
            return str(text)
        children = node.get("children")
        if children:
            return lexical_to_text(children)
        return ""

    return str(node)


def extract_lexical_plain_text(field_content: Any) -> str:
    """Wrapper around :func:`lexical_to_text` for ``datasheet_fields[].field_content``."""
    return lexical_to_text(field_content).strip()


def to_int(value: Any) -> int | None:
    """Coerce a value to int/None for BigQuery INT64 columns."""
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_float(value: Any) -> float | None:
    """Coerce a value to float/None for BigQuery FLOAT64 columns."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_list(value: Any) -> list:
    """Return a list for arrays, wrap single objects, and handle None."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]