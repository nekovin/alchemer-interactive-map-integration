"""Read an Esri File Geodatabase (.gdb folder) straight into parks_data.json format.

Does in one step what the old pipeline did in four (download -> mapshaper import ->
geojson export -> processdata.py). Output matches processdata.py exactly:

    [{"id", "name", "defaultColor", "selectedColor", "coords": [[{lat, lng}, ...]]}]

Parks are often split across several features under the same NAME, so we group by
NAME and emit each polygon's outer ring as a SEPARATE ring. page2.js passes coords
to google.maps.Polygon `paths`, which draws each ring as its own loop (so separated
areas don't get connected by stretched lines).

Usage:
    python gdb_to_json.py PV_PARKRES_V.gdb                   # -> parks_data.json
    python gdb_to_json.py PV_PARKRES_V.gdb out.json          # custom output
"""

import json
import re
import sys

import geopandas as gpd
import pandas as pd

OUTPUT = "parks_data.json"
NAME_FIELD = "NAME"

PV_SOURCE = "PV_parks_piers.xlsx"
UNMATCHED_OUTPUT = "unmatched_labels.xlsx"
LABEL_FIELD = "Label"
CATEGORY_FIELD = "Category"
DEFAULT_CATEGORY = None

DEFAULT_COLOR = "#0B5EDA"
SELECTED_COLOR = "#FF0000"

SKIP_CONTAINS = []
SKIP_EXACT = []

CATEGORY_SOURCE_FIELD = "STYLE_TYPE" 


def ring(coords):
    """A coordinate sequence as [{lat, lng}, ...]; source is [lng, lat]."""
    return [{"lat": y, "lng": x} for x, y in coords]


def rings(geom):
    """Every ring of a (Multi)Polygon, outer and inner, as [{lat, lng}, ...] lists.

    Inner rings are kept so lakes and excised blocks render as holes rather than
    being painted over: google.maps.Polygon `paths` applies the even-odd rule, so a
    ring nested inside another becomes a hole automatically.
    """
    polygons = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    out = []
    for polygon in polygons:
        out.append(ring(polygon.exterior.coords))
        out.extend(ring(interior.coords) for interior in polygon.interiors)
    return out


def normalise(name):
    """Loose key for matching: case, punctuation and '_New' suffixes don't count."""
    name = re.sub(r"_new\b", "", str(name).strip().lower())
    name = name.replace("&", "and")
    return re.sub(r"[^a-z0-9]+", " ", name).strip()


def read_pv(pv_path):
    """Read the Label/Category sheet into {normalised label: (label, category)}."""
    df = pd.read_excel(pv_path)
    lookup = {}
    for label, category in zip(df[LABEL_FIELD], df[CATEGORY_FIELD]):
        # later duplicate rows win, matching pandas' own last-write-wins semantics.
        lookup[normalise(label)] = (str(label).strip(), category)
    return lookup


def match_name_to_category(parks_data, lookup):
    """Tag each park with its category; return the labels that matched nothing."""
    matched = set()
    for park in parks_data:
        key = normalise(park["name"])
        label, category = lookup.get(key, (None, DEFAULT_CATEGORY))
        # separate key: "category" holds the .gdb's own STYLE_TYPE, which covers
        # every park, so the spreadsheet must not overwrite it.
        park["pvCategory"] = category
        if label is not None:
            matched.add(key)

    return [
        {LABEL_FIELD: label, CATEGORY_FIELD: category}
        for key, (label, category) in lookup.items()
        if key not in matched
    ]


def main():
    gdb = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else OUTPUT

    layer = gpd.list_layers(gdb)["name"][0]
    gdf = gpd.read_file(gdb, layer=layer).to_crs("EPSG:4326")

    parks_by_name = {}
    categories = {}
    for name, category, geom in zip(gdf[NAME_FIELD], gdf[CATEGORY_SOURCE_FIELD], gdf.geometry):
        if geom is None or not name:
            continue
        if any(skip in name for skip in SKIP_CONTAINS) or name in SKIP_EXACT:
            continue
        parks_by_name.setdefault(name, []).extend(rings(geom))
        categories.setdefault(name, None if pd.isna(category) else category)

    parks_data = [
        {
            "id": name.lower().replace(" ", "_"),
            "name": name,
            "defaultColor": DEFAULT_COLOR,
            "selectedColor": SELECTED_COLOR,
            "coords": coords,
            "type": categories[name]
        }
        for name, coords in parks_by_name.items()
    ]

    lookup = read_pv(PV_SOURCE)
    unmatched = match_name_to_category(parks_data, lookup)
    pd.DataFrame(unmatched).to_excel(UNMATCHED_OUTPUT, index=False)

    with open(output, "w") as f:
        json.dump(parks_data, f, indent=4)

    tagged = sum(1 for p in parks_data if p["pvCategory"] is not DEFAULT_CATEGORY)
    print(f"{layer}: {len(gdf)} features -> {len(parks_data)} parks -> {output}")
    print(f"{PV_SOURCE}: {len(lookup)} labels -> {tagged} tagged, {len(unmatched)} unmatched")
    print(f"unmatched labels -> {UNMATCHED_OUTPUT}")


if __name__ == "__main__":
    main()
