import json

import geopandas as gpd

from . import config
from .config import DEFAULT_COLOR, SELECTED_COLOR

# GENERATED
NAME_FIELD = "SA4_NAME26"
CODE_FIELD = "SA4_CODE26"
STATE_FIELD = "STE_NAME26"
STATE = "Victoria"
SIMPLIFY = 0.001
PRECISION = 5


def ring(coords):
    return [{"lat": round(y, PRECISION), "lng": round(x, PRECISION)} for x, y in coords]


def rings(geom):
    polygons = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    out = []
    for polygon in polygons:
        out.append(ring(polygon.exterior.coords))
        out.extend(ring(interior.coords) for interior in polygon.interiors)
    return out


def read_areas(shp=config.AREAS_SHP):
    gdf = gpd.read_file(shp).to_crs("EPSG:4326")
    gdf = gdf[gdf[STATE_FIELD] == STATE].copy()
    gdf["geometry"] = gdf.geometry.simplify(SIMPLIFY)
    return gdf


def build(gdf):
    areas = []
    for code, name, geom in zip(gdf[CODE_FIELD], gdf[NAME_FIELD], gdf.geometry):
        if geom is None or not name:
            continue
        areas.append({
            "id": str(code),
            "name": name,
            "defaultColor": DEFAULT_COLOR,
            "selectedColor": SELECTED_COLOR,
            "coords": rings(geom),
        })
    return areas


def main():
    gdf = read_areas()
    areas = build(gdf)

    with open(config.AREAS_JSON, "w") as file:
        json.dump(areas, file, separators=(",", ":"))

    print(f"{len(gdf)} {STATE} features -> {len(areas)} areas")
    print(f"-> {config.AREAS_JSON}")
# END GENERATED


if __name__ == '__main__':
    main()
