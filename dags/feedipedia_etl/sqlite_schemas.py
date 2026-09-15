"""SQLite table schemas — derived from BigQuery schemas but ready to use directly.

No conversion layer. Just column names and SQLite types. Order matters.
"""

SQLITE_SCHEMAS = {
    "dim_family": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array stored as text
        ("description", "TEXT"),
        ("sort_order", "TEXT"),
    ],
    
    "dim_taxon": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("name_full", "TEXT"),
        ("family_id", "TEXT"),
        ("sort_order", "TEXT"),
        ("legacy_drupal_node_id", "TEXT"),
    ],
    
    "dim_parameter_class": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("sort_order", "TEXT"),
    ],
    
    "dim_parameter": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("parameter_class_id", "TEXT"),
        ("unit", "TEXT"),
        ("sort_order", "TEXT"),
    ],
    
    "dim_country": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("iso2", "TEXT"),
        ("iso3", "TEXT"),
        ("sort_order", "TEXT"),
    ],
    
    "dim_category": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("sort_order", "TEXT"),
    ],
    
    "dim_license": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("url", "TEXT"),
    ],
    
    "dim_datasheet": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("status", "TEXT"),
        ("archived", "TEXT"),
        ("published_at", "TEXT"),
        ("agrovoc_uri", "TEXT"),
        ("agrovoc_label", "TEXT"),
        ("datasheet_citation", "TEXT"),
        ("geo_location_status", "TEXT"),
        ("geo_location_level", "TEXT"),
        ("geo_worldwide", "TEXT"),
        ("legacy_drupal_node_id", "TEXT"),
    ],
    
    "dim_feed": [
        ("id", "TEXT NOT NULL"),
        ("code", "TEXT NOT NULL"),
        ("label", "TEXT"),
        ("_referenced_by", "TEXT"),  # JSON array
        ("description", "TEXT"),
        ("status", "TEXT"),
        ("archived", "TEXT"),
        ("last_updated", "TEXT"),
        ("faostat_item_code", "TEXT"),
        ("faostat_item_name", "TEXT"),
        ("faostat_pp_item_code", "TEXT"),
        ("faostat_pp_item_name", "TEXT"),
    ],
}


def create_table_sql(table_name: str) -> str:
    """Generate CREATE TABLE DDL for a table."""
    if table_name not in SQLITE_SCHEMAS:
        raise ValueError(f"No schema defined for table: {table_name}")
    
    columns = SQLITE_SCHEMAS[table_name]
    col_defs = ", ".join(f'"{name}" {type_}' for name, type_ in columns)
    return f'CREATE TABLE "{table_name}" ({col_defs})'


def get_column_names(table_name: str) -> list[str]:
    """Get ordered list of column names for a table."""
    if table_name not in SQLITE_SCHEMAS:
        return []
    return [name for name, _ in SQLITE_SCHEMAS[table_name]]


if __name__ == "__main__":
    # Quick sanity check
    for table, cols in SQLITE_SCHEMAS.items():
        print(f"{table}: {len(cols)} columns")
        print(f"  {create_table_sql(table)[:80]}...")