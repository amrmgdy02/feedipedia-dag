import logging
from typing import Any, Dict, List, Tuple

from feedipedia_etl.utils import (
    REGION_COUNTRIES,
    extract_lexical_plain_text,
    to_float,
    to_int,
    to_str,
)

log = logging.getLogger(__name__)


def _ref_code(value: Any) -> str | None:
    """Return the code of a relationship field, whether expanded or a bare id.

    Payload returns relationships either as a nested document (``{"id": 7, ...}``)
    or, when not populated, as the raw id. Both resolve to the same dimension code.
    """
    if value is None:
        return None
    if isinstance(value, dict):
        return to_str(value.get("id"))
    return to_str(value)

def _transform_family_doc(id, family_doc: Dict[str, Any]) -> Dict[str, Any]:
    family_id = family_doc.get("id")

    if family_id is None:
        raise ValueError(
            f"Family document is missing required 'id': {family_doc}"
        )

    family_id = str(family_id)

    return {
        "id": id,
        "code": family_id,
        "label": family_doc.get("name"),
        "sort_order": (
            str(family_doc["sort_order"])
            if family_doc.get("sort_order") is not None
            else None
        ),
        "_referenced_by": [],
        "description": None,
    }


def transform_family_docs(
    family_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia family documents into dim_family rows."""

    return [
        _transform_family_doc(id=str(index + 1), family_doc=family_doc)
        for index, family_doc in enumerate(family_docs)
    ]


def _transform_taxon_doc(id, taxon_doc: Dict[str, Any]) -> Dict[str, Any]:
    taxon_id = taxon_doc.get("id")

    if taxon_id is None:
        raise ValueError(
            f"Taxon document is missing required 'id': {taxon_doc}"
        )

    taxon_id = str(taxon_id)

    return {
        "id": id,
        "code": taxon_id,
        "label": taxon_doc.get("name_simple"),
        "name_full": taxon_doc.get("name_full"),
        "family_id": _ref_code(taxon_doc.get("family")),
        "_referenced_by": [],
        "description": None,
        "sort_order": (
            str(taxon_doc["sort_order"])
            if taxon_doc.get("sort_order") is not None
            else None
        ),
        "legacy_drupal_node_id": taxon_doc.get("legacy_drupal_node_id") if taxon_doc.get("legacy_drupal_node_id") else None,
    }
    
    
def transform_taxon_docs(
    taxon_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia taxon documents into dim_taxon rows."""

    return [
        _transform_taxon_doc(id=str(index + 1), taxon_doc=taxon_doc)
        for index, taxon_doc in enumerate(taxon_docs)
    ]
    
    

def _transform_parameter_class_doc(
    id,
    parameter_class_doc: Dict[str, Any],
) -> Dict[str, Any]:
    parameter_class_id = parameter_class_doc.get("id")

    if parameter_class_id is None:
        raise ValueError(
            f"Parameter class document is missing required 'id': "
            f"{parameter_class_doc}"
        )

    parameter_class_id = str(parameter_class_id)

    return {
        "id": id,
        "code": parameter_class_id,
        "label": parameter_class_doc.get("name"),
        "_referenced_by": [],
        "description": None,
        "sort_order": to_int(parameter_class_doc.get("sort_order")),
    }


def transform_parameter_class_docs(
    parameter_class_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia parameter class documents into dim_parameter_class rows."""

    return [
        _transform_parameter_class_doc(
            id=str(index + 1),
            parameter_class_doc=parameter_class_doc,
        )
        for index, parameter_class_doc in enumerate(parameter_class_docs)
    ]
    
    
def _transform_parameter_doc(
    id,
    parameter_doc: Dict[str, Any],
) -> Dict[str, Any]:
    parameter_id = parameter_doc.get("id")

    if parameter_id is None:
        raise ValueError(
            f"Parameter document is missing required 'id': "
            f"{parameter_doc}"
        )

    parameter_id = str(parameter_id)

    parameter_class = parameter_doc.get("parameter_class")

    return {
        "id": id,
        "code": parameter_id,
        "label": parameter_doc.get("name"),
        "_referenced_by": [],
        "description": parameter_doc.get("description"),
        "parameter_class_id": _ref_code(parameter_class),
        "unit": parameter_doc.get("unit"),
        "sort_order": to_int(parameter_doc.get("sort_order")),
    }


def transform_parameter_docs(
    parameter_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia parameter documents into dim_parameter rows."""

    return [
        _transform_parameter_doc(
            id=str(index + 1),
            parameter_doc=parameter_doc,
        )
        for index, parameter_doc in enumerate(parameter_docs)
    ]
    
    
    
def _transform_country_doc(
    id,
    country_doc: Dict[str, Any],
) -> Dict[str, Any]:
    country_id = country_doc.get("id")

    if country_id is None:
        raise ValueError(
            f"Country document is missing required 'id': "
            f"{country_doc}"
        )

    country_id = str(country_id)

    return {
        "id": id,
        "code": country_id,
        "label": country_doc.get("name"),
        "_referenced_by": [],
        "description": None,
        "iso2": country_doc.get("code"),
        "iso3": country_doc.get("iso3"),
        "sort_order": to_int(country_doc.get("sort_order")),
    }


def transform_country_docs(
    country_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia country documents into dim_country rows."""

    return [
        _transform_country_doc(
            id=str(index + 1),
            country_doc=country_doc,
        )
        for index, country_doc in enumerate(country_docs)
    ]
    
    
    
def _transform_category_doc(
    id,
    category_doc: Dict[str, Any],
) -> Dict[str, Any]:
    category_id = category_doc.get("id")

    if category_id is None:
        raise ValueError(
            f"Category document is missing required 'id': "
            f"{category_doc}"
        )

    category_id = str(category_id)

    return {
        "id": id,
        "code": category_id,
        "label": category_doc.get("name"),
        "_referenced_by": [],
        "description": None,
        "sort_order": to_int(category_doc.get("sort_order")),
    }


def transform_category_docs(
    category_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia category documents into dim_category rows."""

    return [
        _transform_category_doc(
            id=str(index + 1),
            category_doc=category_doc,
        )
        for index, category_doc in enumerate(category_docs)
    ]
    
    
    
def _transform_license_doc(
    id,
    license_doc: Dict[str, Any],
) -> Dict[str, Any]:
    license_id = license_doc.get("id")

    if license_id is None:
        raise ValueError(
            f"License document is missing required 'id': "
            f"{license_doc}"
        )

    license_id = str(license_id)

    return {
        "id": id,
        "code": license_id,
        "label": license_doc.get("name"),
        "_referenced_by": [],
        "description": None,
        "url": license_doc.get("url"),
    }


def transform_license_docs(
    license_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia license documents into dim_license rows."""

    return [
        _transform_license_doc(
            id=str(index + 1),
            license_doc=license_doc,
        )
        for index, license_doc in enumerate(license_docs)
    ]
    

    
def _get_geo_data(id, datasheet_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build fct_datasheet_geo rows for one datasheet (empty list when it has no geo)."""
    geo_data = datasheet_doc.get("geo")
    if not geo_data:
        return []

    if geo_data.get("worldwide", False) is True:
        return [
            {
                "datasheet": id,
                "country": None,
                "status": "worldwide",
                "source_level": "worldwide",
                "region_code": None,
                "note": "Worldwide flag; expand to all countries only when a single datasheet is selected" # from the csv
            }
        ]

    native_regions = geo_data.get("native_regions", [])
    introduced_regions = geo_data.get("introduced_regions", [])
    native_countries = geo_data.get("native_countries", [])
    introduced_countries = geo_data.get("introduced_countries", [])
    
    rows = []
    
    for native_region in native_regions:
        region_rows = [
            {
                "datasheet": id,
                "country": str(country["country_id"]),
                "status": "native",
                "source_level": "region",
                "region_code": native_region,
                "note": None
            }
            for country in REGION_COUNTRIES.get(native_region, [])
        ]
        rows.extend(region_rows)
        
    for introduced_region in introduced_regions:
        region_rows = [
            {
                "datasheet": id,
                "country": str(country["country_id"]),
                "status": "introduced",
                "source_level": "region",
                "region_code": introduced_region,
                "note": None
            }
            for country in REGION_COUNTRIES.get(introduced_region, [])
        ]
        rows.extend(region_rows)
        
    for native_country in native_countries:
        rows.append(
            {
                "datasheet": id,
                "country": to_str(native_country.get("id")),
                "status": "native",
                "source_level": "country",
                "region_code": None,
                "note": None
            }
        )
        
    for introduced_country in introduced_countries:
        rows.append(
            {
                "datasheet": id,
                "country": to_str(introduced_country.get("id")),
                "status": "introduced",
                "source_level": "country",
                "region_code": None,
                "note": None
            }
        )
            
    return rows # need to convert the raw country ids to bigQuery id



def _get_datasheet_taxons(datasheet_id, datasheet_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build fct_datasheet_taxa rows for one datasheet."""
    rows = datasheet_doc.get("taxa") or []
    return [
        {
            "datasheet": datasheet_id,
            "taxon": str(taxon.get("id")),
        }
        for taxon in rows
        if taxon.get("id") is not None
    ]
    
    
def _get_datasheet_categories(datasheet_id, datasheet_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build fct_datasheet_categories rows for one datasheet."""

    rows = datasheet_doc.get("categories") or []
    return [
        {
            "datasheet": datasheet_id,
            "category": str(category.get("id")),
        }
        for category in rows
        if category.get("id") is not None
    ]
    

EXCEL_CELL_CHAR_LIMIT = 32767


def _get_datasheet_fields(datasheet_id, datasheet_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    fields = datasheet_doc.get("datasheet_fields") or []

    rows = []
    for field in sorted(fields, key=lambda f: (f.get("sort_order") is None, f.get("sort_order"))):
        text = extract_lexical_plain_text(field.get("field_content"))
        rows.append(
            {
                "datasheet": datasheet_id,
                "field_name": to_str(field.get("field_name")),
                "field_text_plain": to_str(text),
                "char_count": len(text),
                "excel_truncated": len(text) > EXCEL_CELL_CHAR_LIMIT,
            }
        )
    return rows


def _get_datasheet_feeds(datasheet_id, datasheet_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build fct_datasheet_feeds rows for one datasheet."""

    rows = datasheet_doc.get("feeds") or []
    return [
        {
            "datasheet": datasheet_id,
            "feed": str(feed.get("id")),
        }
        for feed in rows
        if feed.get("id") is not None
    ]


def _transform_datasheet_doc(
    id,
    datasheet_doc: Dict[str, Any],
) -> Dict[str, Any]:
    datasheet_id = datasheet_doc.get("id")

    if datasheet_id is None:
        raise ValueError(
            f"Datasheet document is missing required 'id': "
            f"{datasheet_doc}"
        )

    datasheet_id = str(datasheet_id)
    
    
    datasheet = {
        "id": id,
        "code": datasheet_id,
        "label": datasheet_doc.get("title"),
        "legacy_drupal_node_id": to_str(datasheet_doc.get("legacy_drupal_node_id")),
        "status": datasheet_doc.get("_status"),
        "archived": bool(datasheet_doc.get("archived")),
        "published_at": datasheet_doc.get("publishedAt"),
        "agrovoc_uri": datasheet_doc.get("agrovoc_uri"),
        "agrovoc_label": datasheet_doc.get("agrovoc_label"),
        "datasheet_citation": datasheet_doc.get("datasheet_citation"),
        "geo_location_status": datasheet_doc.get("geo").get("location_status") if datasheet_doc.get("geo") else None,
        "geo_location_level": datasheet_doc.get("geo").get("location_level") if datasheet_doc.get("geo") else None,
        "geo_worldwide": bool((datasheet_doc.get("geo") or {}).get("worldwide")),
        "_referenced_by": [],
        "description": None,
    }
    
    datasheet_geo = _get_geo_data(id, datasheet_doc)
    datasheet_taxa = _get_datasheet_taxons(id, datasheet_doc)
    datasheet_categories = _get_datasheet_categories(id, datasheet_doc)
    datasheet_feeds = _get_datasheet_feeds(id, datasheet_doc)
    datasheet_fields = _get_datasheet_fields(id, datasheet_doc)
    
    res = {
        "datasheet": datasheet,
        "datasheet_geo": datasheet_geo,
        "datasheet_taxa": datasheet_taxa,
        "datasheet_categories": datasheet_categories,
        "datasheet_feeds": datasheet_feeds,
        "datasheet_fields": datasheet_fields,
    }

    return res
    
    
def transform_datasheet_docs(
    datasheet_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia datasheet documents into dim_datasheet rows."""

    return [
        _transform_datasheet_doc(
            id=str(index + 1),
            datasheet_doc=datasheet_doc,
        )
        for index, datasheet_doc in enumerate(datasheet_docs)
    ]
    
    
    
def _get_feed_values(feed_id, feed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build fct_feed_values rows for one feed, typed for their BigQuery columns."""
    values = feed_doc.get("feed_values") or []

    return [
        {
            "feed": feed_id,
            "parameter": _ref_code(value.get("parameter")),
            "value_avg": to_float(value.get("value_avg")),
            "value_min": to_float(value.get("value_min")),
            "value_max": to_float(value.get("value_max")),
            "value_std": to_float(value.get("value_std")),
            "sample_size": to_float(value.get("sample_size")),
            "measurement_basis": to_str(value.get("measurement_basis")),
            "unit_override": to_str(value.get("unit_override")),
        }
        for value in values
        if value.get("id") is not None
    ]
    
    
def _transform_feed_doc(
    id,
    feed_doc: Dict[str, Any],
) -> Dict[str, Any]:
    feed_id = feed_doc.get("id")

    if feed_id is None:
        raise ValueError(
            f"Feed document is missing required 'id': "
            f"{feed_doc}"
        )

    feed_id = str(feed_id)
    
    feed = {
        "id": id,
        "code": feed_id,
        "label": feed_doc.get("name"),
        "_referenced_by": [],
        "description": None,
        "status": feed_doc.get("_status"),
        "archived": bool(feed_doc.get("archived")),
        "last_updated": feed_doc.get("last_updated"),
        "faostat_item_code": feed_doc.get("faostat_item_code"),
        "faostat_item_name": feed_doc.get("faostat_item_name"),
        "faostat_pp_item_code": feed_doc.get("faostat_pp_item_code"),
        "faostat_pp_item_name": feed_doc.get("faostat_pp_item_name"),
        "faostat_cpc_item_code": feed_doc.get("faostat_cpc_item_code"),
        "faostat_cpc_item_name": feed_doc.get("faostat_cpc_item_name"),
        "faostat_fbs_item_code": feed_doc.get("faostat_fbs_item_code"),
        "faostat_fbs_item_name": feed_doc.get("faostat_fbs_item_name"),
    }
    
    feed_values = _get_feed_values(id, feed_doc)

    res = {
        "feed": feed,
        "feed_values": feed_values,
    }

    return res


def transform_feed_docs(
    feed_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia feed documents into dim_feed rows."""

    return [
        _transform_feed_doc(
            id=str(index + 1),
            feed_doc=feed_doc,
        )
        for index, feed_doc in enumerate(feed_docs)
    ]