"""Read CROWNLAND.gdb (Crown land PARKRES) into parks_data.json format.

Same output shape as gdb_to_json.py, but for the Crown land schema, which differs
from PV_PARKRES_V: categories live in AREA_TYPE (not STYLE_TYPE), and names repeat
across features (~8978 features over ~3563 names), so grouping by NAME matters here.

    [{"id", "name", "defaultColor", "selectedColor", "coords": [[{lat, lng}, ...]],
      "category", "manager"}]

Each polygon's outer ring is emitted as a SEPARATE ring, so page2.js can pass coords
straight to google.maps.Polygon `paths` without separated areas being joined up.

Usage:
    python crownland_to_json.py                          # -> crownland_parks_data.json
    python crownland_to_json.py CROWNLAND.gdb out.json
    python crownland_to_json.py CROWNLAND.gdb out.json --pv-only
"""

import json
import sys

import geopandas as gpd
import pandas as pd

GDB_SOURCE = "CROWNLAND.gdb"
OUTPUT = "crownland_parks_data.json"

NAME_FIELD = "NAME"
CATEGORY_FIELD = "AREA_TYPE"
MANAGER_FIELD = "MANAGER"
PV_MANAGERS = ("Parks Victoria", "Parks Victoria as COM")

DEFAULT_COLOR = "#2E7D32"
SELECTED_COLOR = "#FF9800"


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


def clean(value):
    """pandas NaN -> None, so json.dump writes null instead of invalid NaN."""
    return None if pd.isna(value) else value


def read_crownland(gdb_path, pv_only=False):
    """Group features by NAME into park records."""
    layer = gpd.list_layers(gdb_path)["name"][0]
    gdf = gpd.read_file(gdb_path, layer=layer).to_crs("EPSG:4326")
    if pv_only:
        gdf = gdf[gdf[MANAGER_FIELD].isin(PV_MANAGERS)]

    parks = {}
    for name, category, manager, geom in zip(
        gdf[NAME_FIELD], gdf[CATEGORY_FIELD], gdf[MANAGER_FIELD], gdf.geometry
    ):
        if geom is None or geom.is_empty or pd.isna(name):
            continue
        park = parks.setdefault(
            name,
            {
                "id": name.lower().replace(" ", "_"),
                "name": name,
                "defaultColor": DEFAULT_COLOR,
                "selectedColor": SELECTED_COLOR,
                "coords": [],
                # first feature of a repeated name wins.
                "category": clean(category),
                "manager": clean(manager),
            },
        )
        park["coords"].extend(rings(geom))

    return layer, len(gdf), list(parks.values())


def main():
    gdb = sys.argv[1] if len(sys.argv) > 1 else GDB_SOURCE
    output = sys.argv[2] if len(sys.argv) > 2 else OUTPUT
    pv_only = "--pv-only" in sys.argv

    layer, n_features, parks_data = read_crownland(gdb, pv_only)

    with open(output, "w") as file:
        json.dump(parks_data, file, indent=4)

    n_rings = sum(len(p["coords"]) for p in parks_data)
    print(f"{layer}: {n_features} features -> {len(parks_data)} parks -> {output}")
    print(f"{n_rings} rings, {len({p['category'] for p in parks_data})} categories")


if __name__ == "__main__":
    main()
