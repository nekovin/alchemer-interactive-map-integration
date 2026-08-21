import json

from shapely.geometry import Polygon

from parksres import config

# GENERATED
CENTER_KEY = "center"


def center_of(coords):
    rings = [Polygon([(p["lng"], p["lat"]) for p in ring])
             for ring in coords if len(ring) >= 3]
    if not rings:
        return None
    point = max(rings, key=lambda r: r.area).representative_point()
    return {"lat": point.y, "lng": point.x}


def main():
    with open(config.PARKS_VIC_JSON) as file:
        parks = json.load(file)

    added = 0
    for park in parks:
        center = center_of(park["coords"])
        park[CENTER_KEY] = center
        added += center is not None

    with open(config.PARKS_VIC_JSON, "w") as file:
        json.dump(parks, file, indent=4)

    print(f"{len(parks)} parks, {added} with a centre -> {config.PARKS_VIC_JSON}")
# END GENERATED


if __name__ == '__main__':
    main()
