from google.cloud import bigquery


FAMILY_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Family ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="Primary key",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description="Keeping track of which schemas (fact tables) reference which dimension members (codes)",
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "sort_order",
        "STRING",
        mode="NULLABLE",
    ),
]


TAXON_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Taxon ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="Primary key",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
        description="Genus + species",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description="Keeping track of which schemas (fact tables) reference which dimension members (codes)",
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "name_full",
        "STRING",
        mode="NULLABLE",
        description="With authority when present",
    ),
    bigquery.SchemaField(
        "family_id",
        "STRING",
        mode="NULLABLE",
        description="FK → family.id",
    ),
    bigquery.SchemaField(
        "sort_order",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "legacy_drupal_node_id",
        "STRING",
        mode="NULLABLE",
        description="Audit",
    ),
]


from google.cloud import bigquery


PARAMETER_CLASS_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Parameter class ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="Parameter class Code",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
        description="e.g. Main analysis, Minerals",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description=(
            "Keeping track of which schemas (fact tables) reference "
            "which dimension members (codes)"
        ),
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "sort_order",
        "INTEGER",
        mode="NULLABLE",
    ),
]



PARAMETER_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Parameter ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="PK",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description=(
            "Keeping track of which schemas (fact tables) reference "
            "which dimension members (codes)"
        ),
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "parameter_class_id",
        "STRING",
        mode="NULLABLE",
        description="FK → parameter_classes.id",
    ),
    bigquery.SchemaField(
        "unit",
        "STRING",
        mode="NULLABLE",
        description="Canonical unit",
    ),
    bigquery.SchemaField(
        "sort_order",
        "INTEGER",
        mode="NULLABLE",
        description="Display order",
    ),
]



COUNTRY_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Country ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="PK",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description=(
            "Keeping track of which schemas (fact tables) reference "
            "which dimension members (codes)"
        ),
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "iso2",
        "STRING",
        mode="NULLABLE",
        description="ISO2",
    ),
    bigquery.SchemaField(
        "iso3",
        "STRING",
        mode="NULLABLE",
        description="ISO3",
    ),
    bigquery.SchemaField(
        "sort_order",
        "INTEGER",
        mode="NULLABLE",
    ),
]


CATEGORY_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Country ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="PK",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description=(
            "Keeping track of which schemas (fact tables) reference "
            "which dimension members (codes)"
        ),
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "sort_order",
        "INTEGER",
        mode="NULLABLE",
    ),
]



LICENSE_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="License ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="PK",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description=(
            "Keeping track of which schemas (fact tables) reference "
            "which dimension members (codes)"
        ),
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "url",
        "STRING",
        mode="NULLABLE",
    ),
]



DATASHEET_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Datasheet ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="Payload PK",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description=(
            "Keeping track of which schemas (fact tables) reference "
            "which dimension members (codes)"
        ),
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "status",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "archived",
        "BOOLEAN",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "published_at",
        "TIMESTAMP",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "agrovoc_uri",
        "STRING",
        mode="NULLABLE",
        description="AGROVOC concept URI",
    ),
    bigquery.SchemaField(
        "agrovoc_label",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "datasheet_citation",
        "STRING",
        mode="NULLABLE",
        description="Preferred citation string",
    ),
    bigquery.SchemaField(
        "geo_location_status",
        "STRING",
        mode="NULLABLE",
        description="known / not_known / …",
    ),
    bigquery.SchemaField(
        "geo_location_level",
        "STRING",
        mode="NULLABLE",
        description="country / region / worldwide",
    ),
    bigquery.SchemaField(
        "geo_worldwide",
        "BOOLEAN",
        mode="NULLABLE",
        description="Worldwide distribution flag",
    ),
    bigquery.SchemaField(
        "legacy_drupal_node_id",
        "STRING",
        mode="NULLABLE",
        description="URL redirect / audit only",
    ),
]



FEEDS_SCHEMA = [
    bigquery.SchemaField(
        "id",
        "STRING",
        mode="REQUIRED",
        description="Feeds ID",
    ),
    bigquery.SchemaField(
        "code",
        "STRING",
        mode="REQUIRED",
        description="Feeds Code",
    ),
    bigquery.SchemaField(
        "label",
        "STRING",
        mode="NULLABLE",
        description="Feeds Label",
    ),
    bigquery.SchemaField(
        "_referenced_by",
        "STRING",
        mode="REPEATED",
        description=(
            "Keeping track of which schemas (fact tables) reference "
            "which dimension members (codes)"
        ),
    ),
    bigquery.SchemaField(
        "description",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "status",
        "STRING",
        mode="NULLABLE",
        description="e.g. published, draft",
    ),
    bigquery.SchemaField(
        "archived",
        "BOOLEAN",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "last_updated",
        "TIMESTAMP",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "faostat_item_code",
        "STRING",
        mode="NULLABLE",
        description="QCL item code",
    ),
    bigquery.SchemaField(
        "faostat_item_name",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
            "faostat_pp_item_code",
            "STRING",
            mode="NULLABLE",
            description="Producer price item",
        ),
        bigquery.SchemaField(
            "faostat_pp_item_name",
            "STRING",
            mode="NULLABLE",
        ),
    bigquery.SchemaField(
            "faostat_cpc_item_code",
            "STRING",
            mode="NULLABLE",
            description="Producer price item",
    ),
    bigquery.SchemaField(
            "faostat_cpc_item_name",
            "STRING",
            mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "faostat_fbs_item_code",
        "STRING",
        mode="NULLABLE",
        description="Producer price item",
    ),
    bigquery.SchemaField(
        "faostat_fbs_item_name",
        "STRING",
        mode="NULLABLE",
    ),
]


DATASHEET_FIELDS_SCHEMA = [
    bigquery.SchemaField(
        "datasheet",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "field_name",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "field_text_plain",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "char_count",
        "INT64",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "excel_truncated",
        "BOOLEAN",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_data_ingestion_id",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "_ingestion_time",
        "TIMESTAMP",
        mode="REQUIRED",
    ),
]


# Bridge tables (many-to-many relationships)

DATASHEET_FEEDS_SCHEMA = [
    bigquery.SchemaField(
        "datasheet",
        "STRING",
        mode="REQUIRED",
        description="FK → datasheets.id",
    ),
    bigquery.SchemaField(
        "feed",
        "STRING",
        mode="REQUIRED",
        description="FK → feeds.id",
    ),
     bigquery.SchemaField(
        "_data_ingestion_id",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "_ingestion_time",
        "TIMESTAMP",
        mode="REQUIRED",
    ),
]

# datasheet, country, status, source_level, region_code, note, _data_ingestion_id, and _ingestion_time
DATASHEET_GEO_SCHEMA = [
    bigquery.SchemaField(
        "datasheet",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "country",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "status",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "source_level",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "region_code",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "note",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "_data_ingestion_id",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "_ingestion_time",
        "TIMESTAMP",
        mode="REQUIRED",
    ),
]

DATASHEET_CATEGORY_SCHEMA = [
    bigquery.SchemaField(
        "datasheet",
        "STRING",
        mode="REQUIRED",
        description="FK → datasheets.id",
    ),
    bigquery.SchemaField(
        "category",
        "STRING",
        mode="REQUIRED",
        description="FK → categories.id",
    ),
     bigquery.SchemaField(
        "_data_ingestion_id",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "_ingestion_time",
        "TIMESTAMP",
        mode="REQUIRED",
    ),
]


DATASHEET_TAXA_SCHEMA = [
    bigquery.SchemaField(
        "datasheet",
        "STRING",
        mode="REQUIRED",
        description="FK → datasheets.id",
    ),
    bigquery.SchemaField(
        "taxon",
        "STRING",
        mode="REQUIRED",
        description="FK → taxons.id",
    ),
     bigquery.SchemaField(
        "_data_ingestion_id",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "_ingestion_time",
        "TIMESTAMP",
        mode="REQUIRED",
    ),
]


# FACT TABLES
FEED_VALUES_SCHEMA = [
    bigquery.SchemaField(
        "feed",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "parameter",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "value_avg",
        "FLOAT",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "value_min",
        "FLOAT",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "value_max",
        "FLOAT",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "value_std",
        "FLOAT",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "sample_size",
        "FLOAT",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "measurement_basis",
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "unit_override",
        "STRING",
        mode="NULLABLE",
        description="Overrides parameters.unit when set"
    ),
     bigquery.SchemaField(
        "_data_ingestion_id",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "_ingestion_time",
        "TIMESTAMP",
        mode="REQUIRED",
    ),
]


SCHEMAS = {
    "dim_family": FAMILY_SCHEMA,
    "dim_taxon": TAXON_SCHEMA,
    "dim_parameter_class": PARAMETER_CLASS_SCHEMA,
    "dim_parameter": PARAMETER_SCHEMA,
    "dim_country": COUNTRY_SCHEMA,
    "dim_category": CATEGORY_SCHEMA,
    "dim_license": LICENSE_SCHEMA,
    "dim_datasheet": DATASHEET_SCHEMA,
    "dim_feed": FEEDS_SCHEMA,
    "fct_datasheet_fields": DATASHEET_FIELDS_SCHEMA,
    "fct_datasheet_geo": DATASHEET_GEO_SCHEMA,
    "fct_datasheet_taxa": DATASHEET_TAXA_SCHEMA,
    "fct_datasheet_categories": DATASHEET_CATEGORY_SCHEMA,
    "fct_datasheet_feeds": DATASHEET_FEEDS_SCHEMA,
    "fct_feed_values": FEED_VALUES_SCHEMA,
}
