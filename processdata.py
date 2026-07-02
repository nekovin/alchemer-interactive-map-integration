# Pipeline to (re)build parks_data.json:
#   1. download the source data (Parks Victoria PARKRES, .gdb/.shp)
#   2. go to https://mapshaper.org/  (import it)
#   3. export in geojson  ->  PARKRES.json
#   4. run this script to preprocess into parks_data.json
"""Convert PARKRES.json (Parks Victoria GeoJSON) into parks_data.json for the map.

PARKRES.json is a FeatureCollection of Polygon/MultiPolygon features. Parks are
often split across several features under the same NAME, so we group by NAME and
emit each polygon's outer ring as a SEPARATE ring. index.html passes coords to
google.maps.Polygon `paths`, which draws each ring as its own loop (so separated
areas don't get connected by stretched lines).

Usage:
    python processdata.py
"""

import json

SOURCE = "PARKRES.json"
OUTPUT = "parks_data.json"

DEFAULT_COLOR = "#2E7D32"
SELECTED_COLOR = "#FF9800"

# Drop features whose NAME contains any of these substrings (partial/non-PV rows).
SKIP_CONTAINS = []
# Drop parks whose NAME exactly matches any of these.
SKIP_EXACT = []


def make_park_entry(park_name, geometries):
    """Build one park record from all the geometries sharing its NAME."""
    rings = []
    for geom in geometries:
        if geom["type"] == "Polygon":
            polygons = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            polygons = geom["coordinates"]
        else:
            raise ValueError(f"Unsupported geometry type: {geom['type']}")
        for polygon in polygons:
            # polygon[0] is the outer ring; [lng, lat] -> {lat, lng}
            rings.append([{"lat": p[1], "lng": p[0]} for p in polygon[0]])

    return {
        "id": park_name.lower().replace(" ", "_"),
        "name": park_name,
        "defaultColor": DEFAULT_COLOR,
        "selectedColor": SELECTED_COLOR,
        "coords": rings,
    }


def main():
    with open(SOURCE) as f:
        data = json.load(f)

    # group geometries by park NAME so a split park keeps all its pieces.
    parks_by_name = {}
    for feature in data["features"]:
        name = feature["properties"]["NAME"]
        if any(skip in name for skip in SKIP_CONTAINS):
            continue
        parks_by_name.setdefault(name, []).append(feature["geometry"])

    parks_data = [
        make_park_entry(name, geoms)
        for name, geoms in parks_by_name.items()
        if name not in SKIP_EXACT
    ]

    with open(OUTPUT, "w") as f:
        json.dump(parks_data, f, indent=4)

    print(f"{len(data['features'])} features -> {len(parks_data)} parks -> {OUTPUT}")


if __name__ == "__main__":
    main()
