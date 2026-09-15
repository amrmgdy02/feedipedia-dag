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
        "STRING",
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
        "STRING",
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
        "STRING",
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
        "STRING",
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
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "published_at",
        "STRING",
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
        "STRING",
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
        "STRING",
        mode="NULLABLE",
    ),
    bigquery.SchemaField(
        "last_updated",
        "STRING",
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
]