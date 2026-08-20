"""Merge hand-drawn places from manual_parks.geojson into a parks_data JSON.

Anything missing from PV_PARKRES_V.gdb (council parks and foreshore, piers not held
as Crown land) gets drawn at https://geojson.io and added to manual_parks.geojson.
This merges those in, matching by name: an existing park is replaced, a new one
appended.

Usage:
    python merge_manual.py                          # in place on parks_data.json
    python merge_manual.py parks_data.json out.json
"""

import json
import sys

PARKS_SOURCE = "parks_data.json"
MANUAL_SOURCE = "manual_parks.geojson"

DEFAULT_COLOR = "#0B5EDA"
SELECTED_COLOR = "#FF0000"


def rings(geometry):
    """Every ring of a GeoJSON (Multi)Polygon, outer and inner, as [{lat, lng}, ...].

    A GeoJSON polygon is [outer_ring, *inner_rings], so all of them are kept: the
    even-odd rule in google.maps.Polygon `paths` turns the nested ones into holes.
    """
    if geometry["type"] == "Polygon":
        polygons = [geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        polygons = geometry["coordinates"]
    else:
        raise ValueError(f"Unsupported geometry type: {geometry['type']}")
    # source coordinates are [lng, lat]
    return [
        [{"lat": p[1], "lng": p[0]} for p in polygon_ring]
        for polygon in polygons
        for polygon_ring in polygon
    ]


def read_manual(manual_path):
    """Turn the hand-drawn features into park records, skipping empty geometry."""
    with open(manual_path) as file:
        collection = json.load(file)

    parks = []
    for feature in collection["features"]:
        properties = feature["properties"]
        name = properties["name"]
        coords = [ring for ring in rings(feature["geometry"]) if ring]
        if not coords:
            print(f"  skipped {name!r}: no coordinates drawn yet")
            continue
        parks.append(
            {
                "id": name.lower().replace(" ", "_"),
                "name": name,
                "defaultColor": DEFAULT_COLOR,
                "selectedColor": SELECTED_COLOR,
                "coords": coords,
                "category": properties.get("category"),
                "manager": properties.get("manager"),
                "source": "manual",
            }
        )
    return parks


def merge(parks_data, manual):
    """Replace parks with a matching name, append the rest."""
    by_name = {park["name"]: park for park in parks_data}
    replaced = sum(1 for park in manual if park["name"] in by_name)
    for park in manual:
        by_name[park["name"]] = park
    return list(by_name.values()), replaced


def main():
    parks_path = sys.argv[1] if len(sys.argv) > 1 else PARKS_SOURCE
    output = sys.argv[2] if len(sys.argv) > 2 else parks_path

    with open(parks_path) as file:
        parks_data = json.load(file)

    manual = read_manual(MANUAL_SOURCE)
    merged, replaced = merge(parks_data, manual)

    with open(output, "w") as file:
        json.dump(merged, file, indent=4)

    print(f"{len(parks_data)} parks + {len(manual)} manual "
          f"({replaced} replaced) -> {len(merged)} -> {output}")


if __name__ == "__main__":
    main()
