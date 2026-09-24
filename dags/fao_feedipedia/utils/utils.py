"""Utility helpers: Lexical rich-text extraction and small JSON helpers."""

from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger(__name__)


REFERENCE_MAP: dict[str, dict[str, str]] = {
    "fct_datasheet_geo":        {"datasheet": "dim_datasheet", "country": "dim_country"},
    "fct_datasheet_taxa":       {"datasheet": "dim_datasheet", "taxon": "dim_taxon"},
    "fct_datasheet_categories": {"datasheet": "dim_datasheet", "category": "dim_category"},
    "fct_datasheet_feeds":      {"datasheet": "dim_datasheet", "feed": "dim_feed"},
    "fct_datasheet_fields":     {"datasheet": "dim_datasheet"},
    "fct_feed_values":          {"feed": "dim_feed", "parameter": "dim_parameter"},
    "dim_taxon":                {"family_id": "dim_family"},
    "dim_parameter":            {"parameter_class_id": "dim_parameter_class"},
}


REGION_COUNTRIES = {
    'caribbean': 
    [
        {'country_id': 8, 'country_name': 'Antigua And Barbuda', 'iso3': 'ATG'},
        {'country_id': 19, 'country_name': 'Bahamas', 'iso3': 'BHS'},
        {'country_id': 25, 'country_name': 'Barbados', 'iso3': 'BRB'},
        {'country_id': 42, 'country_name': 'Cuba', 'iso3': 'CUB'},
        {'country_id': 47, 'country_name': 'Dominica', 'iso3': 'DMA'},
        {'country_id': 49, 'country_name': 'Dominican Republic', 'iso3': 'DOM'},
        {'country_id': 70, 'country_name': 'Grenada', 'iso3': 'GRD'},
        {'country_id': 76, 'country_name': 'Haiti', 'iso3': 'HTI'},
        {'country_id': 86, 'country_name': 'Jamaica', 'iso3': 'JAM'},
        {'country_id': 94, 'country_name': 'Saint Kitts And Nevis', 'iso3': 'KNA'},
        {'country_id': 101, 'country_name': 'Saint Lucia', 'iso3': 'LCA'},
        {'country_id': 179, 'country_name': 'Trinidad And Tobago', 'iso3': 'TTO'},
        {'country_id': 190, 'country_name': 'Saint Vincent and the Grenadines', 'iso3': 'VCT'}
    ],
    
    'central_africa':
    [
        {'country_id': 29, 'country_name': 'Central African Republic', 'iso3': 'CAF'},
        {'country_id': 35, 'country_name': 'Cameroon', 'iso3': 'CMR'}, 
        {'country_id': 36, 'country_name': 'Democratic Republic of the Congo', 'iso3': 'COD'},
        {'country_id': 37, 'country_name': 'Congo', 'iso3': 'COG'},
        {'country_id': 61, 'country_name': 'Gabon', 'iso3': 'GAB'},
        {'country_id': 68, 'country_name': 'Equatorial Guinea', 'iso3': 'GNQ'},
        {'country_id': 164, 'country_name': 'Sao Tome And Principe', 'iso3': 'STP'},
        {'country_id': 172, 'country_name': 'Chad', 'iso3': 'TCD'}
    ],
        
    'central_america': 
    [
        {'country_id': 22, 'country_name': 'Belize', 'iso3': 'BLZ'},
        {'country_id': 41, 'country_name': 'Costa Rica', 'iso3': 'CRI'},
        {'country_id': 71, 'country_name': 'Guatemala', 'iso3': 'GTM'},
        {'country_id': 74, 'country_name': 'Honduras', 'iso3': 'HND'},
        {'country_id': 130, 'country_name': 'Nicaragua', 'iso3': 'NIC'},
        {'country_id': 138, 'country_name': 'Panama', 'iso3': 'PAN'},
        {'country_id': 159, 'country_name': 'El Salvador', 'iso3': 'SLV'}
    ],
    
    'central_asia': 
    [
        {'country_id': 89,
        'country_name': 'Kazakhstan', 'iso3': 'KAZ'},
        {'country_id': 91, 'country_name': 'Kyrgyzstan', 'iso3': 'KGZ'},
        {'country_id': 175, 'country_name': 'Tajikistan', 'iso3': 'TJK'},
        {'country_id': 176, 'country_name': 'Turkmenistan', 'iso3': 'TKM'},
        {'country_id': 189, 'country_name': 'Uzbekistan', 'iso3': 'UZB'}
    ],
        
    'east_africa': 
    [
        {'country_id': 12, 'country_name': 'Burundi', 'iso3': 'BDI'},
        {'country_id': 39, 'country_name': 'Comoros', 'iso3': 'COM'},
        {'country_id': 46, 'country_name': 'Djibouti', 'iso3': 'DJI'},
        {'country_id': 53, 'country_name': 'Eritrea', 'iso3': 'ERI'},
        {'country_id': 56, 'country_name': 'Ethiopia', 'iso3': 'ETH'},
        {'country_id': 90, 'country_name': 'Kenya', 'iso3': 'KEN'},
        {'country_id': 112, 'country_name': 'Madagascar', 'iso3': 'MDG'},
        {'country_id': 122, 'country_name': 'Mozambique', 'iso3': 'MOZ'},
        {'country_id': 124, 'country_name': 'Mauritius', 'iso3': 'MUS'},
        {'country_id': 125, 'country_name': 'Malawi', 'iso3': 'MWI'},
        {'country_id': 152, 'country_name': 'Rwanda', 'iso3': 'RWA'},
        {'country_id': 161, 'country_name': 'Somalia', 'iso3': 'SOM'},
        {'country_id': 163, 'country_name': 'South Sudan', 'iso3': 'SSD'},
        {'country_id': 170, 'country_name': 'Seychelles', 'iso3': 'SYC'},
        {'country_id': 184, 'country_name': 'United Republic of Tanzania', 'iso3': 'TZA'},
        {'country_id': 185, 'country_name': 'Uganda', 'iso3': 'UGA'},
        {'country_id': 197, 'country_name': 'Zambia', 'iso3': 'ZMB'},
        {'country_id': 198, 'country_name': 'Zimbabwe', 'iso3': 'ZWE'}
    ],
        
    'east_asia':
    [
        {'country_id': 33, 'country_name': 'China', 'iso3': 'CHN'},
        {'country_id': 88, 'country_name': 'Japan', 'iso3': 'JPN'},
        {'country_id': 95, 'country_name': 'Republic Of Korea', 'iso3': 'KOR'},
        {'country_id': 121, 'country_name': 'Mongolia', 'iso3': 'MNG'},
        {'country_id': 145, 'country_name': "Democratic People's Republic of Korea", 'iso3': 'PRK'},
        {'country_id': 183, 'country_name': 'Taiwan Province of China', 'iso3': 'TWN'}
    ],
        
    'europe': 
    [
        {'country_id': 3, 'country_name': 'Albania', 'iso3': 'ALB'},
        {'country_id': 4, 'country_name': 'Andorra', 'iso3': 'AND'},
        {'country_id': 10, 'country_name': 'Austria', 'iso3': 'AUT'},
        {'country_id': 13, 'country_name': 'Belgium', 'iso3': 'BEL'},
        {'country_id': 17, 'country_name': 'Bulgaria', 'iso3': 'BGR'},
        {'country_id': 20, 'country_name': 'Bosnia and Herzegovina', 'iso3': 'BIH'},
        {'country_id': 21, 'country_name': 'Belarus', 'iso3': 'BLR'},
        {'country_id': 31, 'country_name': 'Switzerland', 'iso3': 'CHE'},
        {'country_id': 43, 'country_name': 'Cyprus', 'iso3': 'CYP'},
        {'country_id': 44, 'country_name': 'Czechia', 'iso3': 'CZE'},
        {'country_id': 45, 'country_name': 'Germany', 'iso3': 'DEU'},
        {'country_id': 48, 'country_name': 'Denmark', 'iso3': 'DNK'},
        {'country_id': 54, 'country_name': 'Spain', 'iso3': 'ESP'},
        {'country_id': 55, 'country_name': 'Estonia', 'iso3': 'EST'},
        {'country_id': 57, 'country_name': 'Finland', 'iso3': 'FIN'},
        {'country_id': 59, 'country_name': 'France', 'iso3': 'FRA'},
        {'country_id': 62, 'country_name': 'United Kingdom of Great Britain and Northern Ireland', 'iso3': 'GBR'},
        {'country_id': 69, 'country_name': 'Greece', 'iso3': 'GRC'},
        {'country_id': 75, 'country_name': 'Croatia', 'iso3': 'HRV'},
        {'country_id': 77, 'country_name': 'Hungary', 'iso3': 'HUN'},
        {'country_id': 80, 'country_name': 'Ireland', 'iso3': 'IRL'},
        {'country_id': 83, 'country_name': 'Iceland', 'iso3': 'ISL'},
        {'country_id': 85, 'country_name': 'Italy', 'iso3': 'ITA'},
        {'country_id': 102, 'country_name': 'Liechtenstein', 'iso3': 'LIE'},
        {'country_id': 105, 'country_name': 'Lithuania', 'iso3': 'LTU'},
        {'country_id': 106, 'country_name': 'Luxembourg', 'iso3': 'LUX'},
        {'country_id': 107, 'country_name': 'Latvia', 'iso3': 'LVA'},
        {'country_id': 110, 'country_name': 'Monaco', 'iso3': 'MCO'},
        {'country_id': 111, 'country_name': 'Republic of Moldova', 'iso3': 'MDA'},
        {'country_id': 116, 'country_name': 'North Macedonia', 'iso3': 'MKD'},
        {'country_id': 118, 'country_name': 'Malta', 'iso3': 'MLT'},
        {'country_id': 120, 'country_name': 'Montenegro', 'iso3': 'MNE'},
        {'country_id': 131, 'country_name': 'Netherlands (Kingdom of the)', 'iso3': 'NLD'},
        {'country_id': 132, 'country_name': 'Norway', 'iso3': 'NOR'},
        {'country_id': 143, 'country_name': 'Poland', 'iso3': 'POL'},
        {'country_id': 146, 'country_name': 'Portugal', 'iso3': 'PRT'},
        {'country_id': 150, 'country_name': 'Romania', 'iso3': 'ROU'},
        {'country_id': 151, 'country_name': 'Russian Federation', 'iso3': 'RUS'},
        {'country_id': 162, 'country_name': 'Serbia', 'iso3': 'SRB'},
        {'country_id': 166, 'country_name': 'Slovakia', 'iso3': 'SVK'},
        {'country_id': 167, 'country_name': 'Slovenia', 'iso3': 'SVN'},
        {'country_id': 168, 'country_name': 'Sweden', 'iso3': 'SWE'},
        {'country_id': 186, 'country_name': 'Ukraine', 'iso3': 'UKR'}
    ],
        
    'mediterranean': 
    [
        {'country_id': 43, 'country_name': 'Cyprus', 'iso3': 'CYP'},
        {'country_id': 50, 'country_name': 'Algeria', 'iso3': 'DZA'},
        {'country_id': 52, 'country_name': 'Egypt', 'iso3': 'EGY'},
        {'country_id': 54, 'country_name': 'Spain', 'iso3': 'ESP'},
        {'country_id': 59, 'country_name': 'France', 'iso3': 'FRA'},
        {'country_id': 69, 'country_name': 'Greece', 'iso3': 'GRC'},
        {'country_id': 75, 'country_name': 'Croatia', 'iso3': 'HRV'},
        {'country_id': 84, 'country_name': 'Israel', 'iso3': 'ISR'},
        {'country_id': 85, 'country_name': 'Italy', 'iso3': 'ITA'},
        {'country_id': 98, 'country_name': 'Lebanon', 'iso3': 'LBN'},
        {'country_id': 100, 'country_name': 'Libya', 'iso3': 'LBY'},
        {'country_id': 109, 'country_name': 'Morocco', 'iso3': 'MAR'},
        {'country_id': 118, 'country_name': 'Malta', 'iso3': 'MLT'},
        {'country_id': 171, 'country_name': 'Syrian Arab Republic', 'iso3': 'SYR'},
        {'country_id': 180, 'country_name': 'Tunisia', 'iso3': 'TUN'},
        {'country_id': 181, 'country_name': 'Türkiye', 'iso3': 'TUR'}],
        
    'north_africa': 
    [
        {'country_id': 50, 'country_name': 'Algeria', 'iso3': 'DZA'},
        {'country_id': 52, 'country_name': 'Egypt', 'iso3': 'EGY'},
        {'country_id': 100, 'country_name': 'Libya', 'iso3': 'LBY'},
        {'country_id': 109, 'country_name': 'Morocco', 'iso3': 'MAR'},
        {'country_id': 154, 'country_name': 'Sudan', 'iso3': 'SDN'},
        {'country_id': 180, 'country_name': 'Tunisia', 'iso3': 'TUN'}
    ],
    
    'north_america': 
    [
        {'country_id': 30, 'country_name': 'Canada', 'iso3': 'CAN'},
        {'country_id': 114, 'country_name': 'Mexico', 'iso3': 'MEX'},
        {'country_id': 188, 'country_name': 'United States of America','iso3': 'USA'}
    ],
        
    'oceania': 
    [
        {'country_id': 9, 'country_name': 'Australia', 'iso3': 'AUS'},
        {'country_id': 58, 'country_name': 'Fiji', 'iso3': 'FJI'},
        {'country_id': 135, 'country_name': 'New Zealand', 'iso3': 'NZL'},
        {'country_id': 142, 'country_name': 'Papua New Guinea', 'iso3': 'PNG'},
        {'country_id': 157, 'country_name': 'Solomon Islands', 'iso3': 'SLB'},
        {'country_id': 178, 'country_name': 'Tonga', 'iso3': 'TON'},
        {'country_id': 193, 'country_name': 'Vanuatu', 'iso3': 'VUT'},
        {'country_id': 194, 'country_name': 'Samoa', 'iso3': 'WSM'}
    ],
        
    'south_america': 
    [
        {'country_id': 6, 'country_name': 'Argentina','iso3': 'ARG'},
        {'country_id': 23, 'country_name': 'Bolivia (Plurinational State of)', 'iso3': 'BOL'},
        {'country_id': 24, 'country_name': 'Brazil', 'iso3': 'BRA'},
        {'country_id': 32, 'country_name': 'Chile', 'iso3': 'CHL'},
        {'country_id': 38, 'country_name': 'Colombia', 'iso3': 'COL'},
        {'country_id': 51, 'country_name': 'Ecuador', 'iso3': 'ECU'},
        {'country_id': 72, 'country_name': 'Guyana', 'iso3': 'GUY'},
        {'country_id': 139, 'country_name': 'Peru', 'iso3': 'PER'},
        {'country_id': 147, 'country_name': 'Paraguay', 'iso3': 'PRY'},
        {'country_id': 165, 'country_name': 'Suriname', 'iso3': 'SUR'},
        {'country_id': 187, 'country_name': 'Uruguay', 'iso3': 'URY'},
        {'country_id': 191, 'country_name': 'Venezuela (Bolivarian Republic Of)', 'iso3': 'VEN'}
    ],
        
    'south_asia': 
    [
        {'country_id': 1, 'country_name': 'Afghanistan', 'iso3': 'AFG'},
        {'country_id': 16, 'country_name': 'Bangladesh', 'iso3': 'BGD'},
        {'country_id': 27, 'country_name': 'Bhutan', 'iso3': 'BTN'},
        {'country_id': 79, 'country_name': 'India', 'iso3': 'IND'},
        {'country_id': 103, 'country_name': 'Sri Lanka', 'iso3': 'LKA'},
        {'country_id': 113, 'country_name': 'Maldives', 'iso3': 'MDV'},
        {'country_id': 133, 'country_name': 'Nepal', 'iso3': 'NPL'},
        {'country_id': 137, 'country_name': 'Pakistan', 'iso3': 'PAK'}],
        
    'southeast_asia': 
    [
        {'country_id': 26, 'country_name': 'Brunei Darussalam','iso3': 'BRN'},
        {'country_id': 78, 'country_name': 'Indonesia', 'iso3': 'IDN'},
        {'country_id': 92, 'country_name': 'Cambodia', 'iso3': 'KHM'},
        {'country_id': 97,'country_name': "Lao People's Democratic Republic", 'iso3': 'LAO'},
        {'country_id': 119, 'country_name': 'Myanmar', 'iso3': 'MMR'},
        {'country_id': 126, 'country_name': 'Malaysia', 'iso3': 'MYS'},
        {'country_id': 140, 'country_name': 'Philippines', 'iso3': 'PHL'},
        {'country_id': 156, 'country_name': 'Singapore', 'iso3': 'SGP'},
        {'country_id': 174, 'country_name': 'Thailand', 'iso3': 'THA'},
        {'country_id': 177, 'country_name': 'Timor-Leste', 'iso3': 'TLS'},
        {'country_id': 192, 'country_name': 'Viet Nam', 'iso3': 'VNM'}
    ],
        
    'southern_africa': 
    [
        {'country_id': 2,
        'country_name': 'Angola', 'iso3': 'AGO'},
        {'country_id': 28, 'country_name': 'Botswana', 'iso3': 'BWA'},
        {'country_id': 104, 'country_name': 'Lesotho', 'iso3': 'LSO'},
        {'country_id': 112, 'country_name': 'Madagascar', 'iso3': 'MDG'},
        {'country_id': 122, 'country_name': 'Mozambique', 'iso3': 'MOZ'},
        {'country_id': 124, 'country_name': 'Mauritius', 'iso3': 'MUS'},
        {'country_id': 125, 'country_name': 'Malawi', 'iso3': 'MWI'},
        {'country_id': 127, 'country_name': 'Namibia', 'iso3': 'NAM'},
        {'country_id': 169, 'country_name': 'Eswatini', 'iso3': 'SWZ'},
        {'country_id': 196, 'country_name': 'South Africa', 'iso3': 'ZAF'},
        {'country_id': 197, 'country_name': 'Zambia', 'iso3': 'ZMB'},
        {'country_id': 198, 'country_name': 'Zimbabwe', 'iso3': 'ZWE'}
    ], 
        
    'west_africa': 
    [
        {'country_id': 14, 'country_name': 'Benin', 'iso3': 'BEN'},
        {'country_id': 15, 'country_name': 'Burkina Faso', 'iso3': 'BFA'},
        {'country_id': 34, 'country_name': "Côte D'Ivoire", 'iso3': 'CIV'},
        {'country_id': 40, 'country_name': 'Cabo Verde', 'iso3': 'CPV'},
        {'country_id': 64, 'country_name': 'Ghana', 'iso3': 'GHA'},
        {'country_id': 65, 'country_name': 'Guinea', 'iso3': 'GIN'},
        {'country_id': 66, 'country_name': 'Gambia', 'iso3': 'GMB'},
        {'country_id': 67, 'country_name': 'Guinea-Bissau', 'iso3': 'GNB'},
        {'country_id': 99, 'country_name': 'Liberia', 'iso3': 'LBR'},
        {'country_id': 117, 'country_name': 'Mali', 'iso3': 'MLI'},
        {'country_id': 123, 'country_name': 'Mauritania', 'iso3': 'MRT'},
        {'country_id': 128, 'country_name': 'Niger', 'iso3': 'NER'},
        {'country_id': 129, 'country_name': 'Nigeria', 'iso3': 'NGA'},
        {'country_id': 155, 'country_name': 'Senegal', 'iso3': 'SEN'},
        {'country_id': 158, 'country_name': 'Sierra Leone', 'iso3': 'SLE'},
        {'country_id': 173, 'country_name': 'Togo', 'iso3': 'TGO'}
    ],
        
    'west_asia_middle_east': 
    [
        {'country_id': 5, 'country_name': 'United Arab Emirates', 'iso3': 'ARE'},
        {'country_id': 18, 'country_name': 'Bahrain', 'iso3': 'BHR'},
        {'country_id': 81, 'country_name': 'Iran (Islamic Republic Of)', 'iso3': 'IRN'},
        {'country_id': 82, 'country_name': 'Iraq', 'iso3': 'IRQ'},
        {'country_id': 84, 'country_name': 'Israel', 'iso3': 'ISR'},
        {'country_id': 87, 'country_name': 'Jordan', 'iso3': 'JOR'},
        {'country_id': 96, 'country_name': 'Kuwait', 'iso3': 'KWT'},
        {'country_id': 98, 'country_name': 'Lebanon', 'iso3': 'LBN'},
        {'country_id': 136, 'country_name': 'Oman', 'iso3': 'OMN'},
        {'country_id': 149, 'country_name': 'Qatar', 'iso3': 'QAT'},
        {'country_id': 153, 'country_name': 'Saudi Arabia', 'iso3': 'SAU'},
        {'country_id': 171, 'country_name': 'Syrian Arab Republic', 'iso3': 'SYR'},
        {'country_id': 195, 'country_name': 'Yemen', 'iso3': 'YEM'}
    ]
 }


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


def to_str(value: Any) -> str | None:
    """Coerce a value to str/None for BigQuery STRING columns.

    Unlike a bare ``str(value)``, a missing value stays ``NULL`` instead of
    becoming the literal text ``"None"``.
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value or None
    return str(value)


def resolve_bridge_ref_ids(
    bridge_rows: list[dict[str, Any]],
    referenced_rows: list[dict[str, Any]],
    ref_column_name: str,
) -> list[dict[str, Any]]:
    """Swap a bridge column's natural key for the referenced table's surrogate id.

    ``bridge_rows[*][ref_column_name]`` holds the source system's code; it is
    replaced in place with the ``id`` of the row in ``referenced_rows`` carrying
    that ``code``. Codes with no match resolve to ``None`` rather than silently
    keeping the unresolved value, and are reported so a broken join surfaces in
    the logs instead of reaching BigQuery.

    Args:
        bridge_rows: Rows to resolve (mutated in place).
        referenced_rows: Rows of the referenced dimension, carrying ``code``/``id``.
        ref_column_name: Column on ``bridge_rows`` holding the code to resolve.

    Returns:
        ``bridge_rows``, for convenient chaining.
    """
    id_by_code = {
        row["code"]: row.get("id") for row in referenced_rows if row.get("code") is not None
    }

    unresolved: dict[Any, int] = {}
    for bridge_row in bridge_rows:
        code = bridge_row.get(ref_column_name)
        if code is None:
            continue
        if code in id_by_code:
            bridge_row[ref_column_name] = id_by_code[code]
        else:
            bridge_row[ref_column_name] = None
            unresolved[code] = unresolved.get(code, 0) + 1

    if unresolved:
        sample = sorted(unresolved.items(), key=lambda kv: -kv[1])[:5]
        log.warning(
            "Could not resolve %d row(s) across %d distinct code(s) for column %r; "
            "set to NULL. Most frequent: %s",
            sum(unresolved.values()),
            len(unresolved),
            ref_column_name,
            ", ".join(f"{code!r} x{count}" for code, count in sample),
        )

    return bridge_rows


def fill_referenced_by(tables: dict[str, list[dict[str, Any]]]) -> None:
    
    hits: dict[str, dict[Any, set[str]]] = {}

    for source_table, fk_columns in REFERENCE_MAP.items():
        for row in tables.get(source_table, []):
            for fk_column, target_table in fk_columns.items():
                target_id = row.get(fk_column)
                if target_id is None:
                    continue
                hits.setdefault(target_table, {}).setdefault(target_id, set()).add(source_table)

    for table_name, rows in tables.items():
        if not table_name.startswith("dim_"):
            continue
        table_hits = hits.get(table_name, {})
        for row in rows:
            row["_referenced_by"] = sorted(table_hits.get(row.get("id"), set()))