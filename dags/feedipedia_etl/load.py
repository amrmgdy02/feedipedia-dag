from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import ALL_TABLES, LOCAL_DATA_DIR, SQLITE_DB_PATH
from .sqlite_schemas import SQLITE_SCHEMAS, get_column_names

log = logging.getLogger(__name__)


def _scalar(value: Any) -> Any:
    if value is None or isinstance(value, (int, float, str, bytes)):
        return value
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (datetime, timezone)):
        return value.isoformat()
    return json.dumps(value, ensure_ascii=False)


def _read_rows(path: Path) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))

    if not rows:
        cols = get_column_names(path.stem)
        return rows, cols

    cols = get_column_names(path.stem)
    
    seen = set(cols)
    for r in rows:
        for key in r.keys():
            if key not in seen:
                seen.add(key)
                cols.append(key)
    
    return rows, cols


def _create_table(conn: sqlite3.Connection, table: str, cols: list[str]) -> None:
    schema = SQLITE_SCHEMAS.get(table, {})
    schema_cols = {name: type_ for name, type_ in schema}
    
    col_defs = []
    for c in cols:
        if c in schema_cols:
            col_defs.append(f'"{c}" {schema_cols[c]}')
        else:
            # Extra column not in schema; use TEXT
            col_defs.append(f'"{c}" TEXT')
    
    if not col_defs:
        raise ValueError(f"No columns for table {table!r}")
    
    ddl = f'CREATE TABLE "{table}" ({", ".join(col_defs)})'
    conn.execute(f'DROP TABLE IF EXISTS "{table}"')
    conn.execute(ddl)
    conn.commit()


def load_ndjson_table(db_path: str | Path, table: str, ndjson_path: str | Path,
                      drop_first: bool = True) -> int:
    ndjson_path = Path(ndjson_path)
    if not ndjson_path.exists():
        raise FileNotFoundError(f"Staging NDJSON not found: {ndjson_path}")

    rows, cols = _read_rows(ndjson_path)
    if not rows:
        log.info("%s: no rows to load (empty file)", table)
        return 0

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    
    if drop_first:
        _create_table(conn, table, cols)

    placeholders = ", ".join("?" for _ in cols)
    quoted = ", ".join(f'"{c}"' for c in cols)
    insert_sql = f'INSERT INTO "{table}" ({quoted}) VALUES ({placeholders})'

    data = [[_scalar(row.get(c)) for c in cols] for row in rows]
    conn.executemany(insert_sql, data)
    conn.commit()
    conn.close()
    
    log.info("Loaded %d rows into %s from %s", len(data), table, ndjson_path)
    return len(data)


def load_staging_dir(db_path: str | Path, staging_dir: str | Path,
                     table_names: list[str] | None = None) -> dict[str, int]:
    staging_dir = Path(staging_dir)
    if not staging_dir.is_dir():
        raise NotADirectoryError(f"Staging directory not found: {staging_dir}")

    ndjson_files = sorted(staging_dir.glob("*.ndjson"))
    if table_names is not None:
        wanted = set(table_names)
        ndjson_files = [p for p in ndjson_files if p.stem in wanted]

    if not ndjson_files:
        log.warning("No NDJSON files in %s", staging_dir)
        return {}

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    loaded: dict[str, int] = {}
    
    try:
        for path in ndjson_files:
            table = path.stem
            rows, cols = _read_rows(path)
            if not rows:
                log.info("%s: skipped (empty file)", table)
                continue
            
            _create_table(conn, table, cols)
            quoted_cols = ", ".join(f'"{c}"' for c in cols)
            placeholders = ", ".join("?" for _ in cols)
            insert = f'INSERT INTO "{table}" ({quoted_cols}) VALUES ({placeholders})'
            
            data = [[_scalar(row.get(c)) for c in cols] for row in rows]
            conn.executemany(insert, data)
            conn.commit()
            loaded[table] = len(data)
            log.info("Loaded %d rows into %s", len(data), table)
    finally:
        conn.close()
    
    return loaded


def _run_id(context: dict) -> str:
    """Logical execution date."""
    ts = context.get("ts_nodash")
    if ts:
        return str(ts)
    ts = context.get("ts")
    if ts:
        return str(ts).replace("-", "").replace(":", "").replace(" ", "").split(".")[0]
    fallback = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    log.warning("No Airflow ts_nodash in context, using wall clock '%s'", fallback)
    return fallback


def load_sqlite_tables(table_names: list[str], **context) -> dict[str, int]:
    """Airflow task: load staging NDJSON into SQLite."""
    ti = context["ti"]
    run_id = _run_id(context)
    db_path = context.get("db_path") or SQLITE_DB_PATH
    staging_dir = context.get("staging_dir") or Path(LOCAL_DATA_DIR) / "staging" / run_id

    counts = load_staging_dir(
        db_path=db_path,
        staging_dir=staging_dir,
        table_names=list(table_names),
    )
    missing = [t for t in table_names if t not in counts]
    if missing:
        log.warning("No staging NDJSON found for tables (skipped): %s",
                    ", ".join(missing))
    return counts
