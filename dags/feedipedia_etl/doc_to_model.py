from typing import Any, Dict, List


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
        _transform_family_doc(id=index + 1, family_doc=family_doc)
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
        "family_id": taxon_doc.get("family").get("id") if taxon_doc.get("family") else None,
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
        _transform_taxon_doc(id=index + 1, taxon_doc=taxon_doc)
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
        "sort_order": (
            str(parameter_class_doc["sort_order"])
            if parameter_class_doc.get("sort_order") is not None
            else None
        ),
    }


def transform_parameter_class_docs(
    parameter_class_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia parameter class documents into dim_parameter_class rows."""

    return [
        _transform_parameter_class_doc(
            id=index + 1,
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
        "parameter_class_id": (
            str(parameter_class.get("id"))
            if parameter_class
            and parameter_class.get("id") is not None
            else None
        ),
        "unit": parameter_doc.get("unit"),
        "sort_order": (
            str(parameter_doc.get("sort_order"))
            if parameter_doc.get("sort_order") is not None
            else None
        ),
    }


def transform_parameter_docs(
    parameter_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia parameter documents into dim_parameter rows."""

    return [
        _transform_parameter_doc(
            id=index + 1,
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
        "code": country_doc.get("code"),
        "label": country_doc.get("name"),
        "_referenced_by": [],
        "description": None,
        "iso2": country_doc.get("code"),
        "iso3": country_doc.get("iso3"),
        "sort_order": (
            str(country_doc.get("sort_order"))
            if country_doc.get("sort_order") is not None
            else None
        ),
    }


def transform_country_docs(
    country_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia country documents into dim_country rows."""

    return [
        _transform_country_doc(
            id=index + 1,
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
        "sort_order": (
            str(category_doc["sort_order"])
            if category_doc.get("sort_order") is not None
            else None
        ),
    }


def transform_category_docs(
    category_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia category documents into dim_category rows."""

    return [
        _transform_category_doc(
            id=index + 1,
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
            id=index + 1,
            license_doc=license_doc,
        )
        for index, license_doc in enumerate(license_docs)
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

    return {
        "id": id,
        "code": datasheet_id,
        "label": datasheet_doc.get("title"),
        "legacy_drupal_node_id": datasheet_doc.get("legacy_drupal_node_id"),
        "status": datasheet_doc.get("_status"),
        "archived": datasheet_doc.get("archived"),
        "published_at": datasheet_doc.get("publishedAt"),
        "agrovoc_uri": datasheet_doc.get("agrovoc_uri"),
        "agrovoc_label": datasheet_doc.get("agrovoc_label"),
        "datasheet_citation": datasheet_doc.get("datasheet_citation"),
        "geo_location_status": datasheet_doc.get("geo").get("location_status") if datasheet_doc.get("geo") else None,
        "geo_location_level": datasheet_doc.get("geo").get("location_level") if datasheet_doc.get("geo") else None,
        "geo_worldwide": datasheet_doc.get("geo").get("worldwide") if datasheet_doc.get("geo") else None,
        "_referenced_by": [],
        "description": None,
        "sort_order": (
            str(datasheet_doc["sort_order"])
            if datasheet_doc.get("sort_order") is not None
            else None
        ),
    }
    
    
def transform_datasheet_docs(
    datasheet_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia datasheet documents into dim_datasheet rows."""

    return [
        _transform_datasheet_doc(
            id=index + 1,
            datasheet_doc=datasheet_doc,
        )
        for index, datasheet_doc in enumerate(datasheet_docs)
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

    return {
        "id": id,
        "code": feed_id,
        "label": feed_doc.get("name"),
        "_referenced_by": [],
        "description": None,
        "status": feed_doc.get("_status"),
        "archived": feed_doc.get("archived"),
        "last_updated": feed_doc.get("last_updated"),
        "faostat_item_code": feed_doc.get("faostat_item_code"),
        "faostat_item_name": feed_doc.get("faostat_item_name"),
        "faostat_pp_item_code": feed_doc.get("faostat_pp_item_code"),
        "faostat_pp_item_name": feed_doc.get("faostat_pp_item_name"),
        "faostat_cpc_item_code": feed_doc.get("faostat_cpc_item_code"),
        "faostat_cpc_item_name": feed_doc.get("faostat_cpc_item_name"),
        "faostat_fbs_item_code": feed_doc.get("faostat_fbs_item_code"),
        "faostat_fbs_item_name": feed_doc.get("faostat_fbs_item_name"),
        "legacy_drupal_node_id": feed_doc.get("legacy_drupal_node_id"),
    }
    
    
def transform_feed_docs(
    feed_docs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Transform Feedipedia feed documents into dim_feed rows."""

    return [
        _transform_feed_doc(
            id=index + 1,
            feed_doc=feed_doc,
        )
        for index, feed_doc in enumerate(feed_docs)
    ]