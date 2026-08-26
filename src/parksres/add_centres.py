import json
import math

from pyproj import Transformer
from shapely.geometry import Polygon

from parksres import config

# GENERATED
CENTER_KEY = "center"
RADIUS_KEY = "radius"

CIRCLE_CATEGORIES = ("PP", "WP")
MAX_RADIUS = 3000
MIN_RADIUS = 250
METRIC_CRS = "EPSG:3111"


def center_of(coords):
    rings = [Polygon([(p["lng"], p["lat"]) for p in ring])
             for ring in coords if len(ring) >= 3]
    if not rings:
        return None
    point = max(rings, key=lambda r: r.area).representative_point()
    return {"lat": point.y, "lng": point.x}


def add_radii(parks):
    to_metres = Transformer.from_crs("EPSG:4326", METRIC_CRS, always_xy=True)

    groups = {}
    for park in parks:
        if park.get("category") in CIRCLE_CATEGORIES and park.get(CENTER_KEY):
            groups.setdefault(park["category"], []).append(park)

    shrunk = 0
    for members in groups.values():
        points = [to_metres.transform(p[CENTER_KEY]["lng"], p[CENTER_KEY]["lat"])
                  for p in members]
        for i, park in enumerate(members):
            gaps = [math.dist(points[i], points[j])
                    for j in range(len(members)) if j != i]
            radius = MAX_RADIUS if not gaps else min(MAX_RADIUS, min(gaps) / 2)
            park[RADIUS_KEY] = int(max(MIN_RADIUS, radius))
            shrunk += park[RADIUS_KEY] < MAX_RADIUS
    return groups, shrunk


def overlaps(groups):
    to_metres = Transformer.from_crs("EPSG:4326", METRIC_CRS, always_xy=True)
    count = 0
    for members in groups.values():
        points = [to_metres.transform(p[CENTER_KEY]["lng"], p[CENTER_KEY]["lat"])
                  for p in members]
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                gap = math.dist(points[i], points[j])
                if gap < members[i][RADIUS_KEY] + members[j][RADIUS_KEY]:
                    count += 1
    return count


def main():
    with open(config.PARKS_VIC_JSON) as file:
        parks = json.load(file)

    added = 0
    for park in parks:
        center = center_of(park["coords"])
        park[CENTER_KEY] = center
        added += center is not None

    groups, shrunk = add_radii(parks)
    circles = sum(len(m) for m in groups.values())
    remaining = overlaps(groups)

    with open(config.PARKS_VIC_JSON, "w") as file:
        json.dump(parks, file, indent=4)

    print(f"{len(parks)} parks, {added} with a centre -> {config.PARKS_VIC_JSON}")
    print(f"{circles} circles, {shrunk} shrunk below {MAX_RADIUS}m, "
          f"{remaining} overlapping pairs remaining")
# END GENERATED


if __name__ == '__main__':
    main()
