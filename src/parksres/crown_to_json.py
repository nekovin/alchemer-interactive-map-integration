import json

import geopandas as gpd
import pandas as pd

from . import config
from .config import DEFAULT_COLOR, SELECTED_COLOR

# GENERATED
NAME_FIELD = "NAME"
TYPE_FIELD = "AREA_TYPE"



def ring(coords):
    return [{"lat": y, "lng": x} for x, y in coords]


def rings(geom):
    polygons = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    out = []
    for polygon in polygons:
        out.append(ring(polygon.exterior.coords))
        out.extend(ring(interior.coords) for interior in polygon.interiors)
    return out


def read_crown(gdb=config.CROWN_GDB):
    layer = gpd.list_layers(gdb)["name"][0]
    return layer, gpd.read_file(gdb, layer=layer).to_crs("EPSG:4326")


def build(gdf):
    coords_by_name = {}
    types = {}
    for name, area_type, geom in zip(gdf[NAME_FIELD], gdf[TYPE_FIELD], gdf.geometry):
        if geom is None or not name:
            continue
        coords_by_name.setdefault(name, []).extend(rings(geom))
        types.setdefault(name, None if pd.isna(area_type) else area_type)

    return [
        {
            "id": name.lower().replace(" ", "_"),
            "name": name,
            "defaultColor": DEFAULT_COLOR,
            "selectedColor": SELECTED_COLOR,
            "coords": coords,
            "type": types[name],
        }
        for name, coords in coords_by_name.items()
    ]


def main():
    layer, gdf = read_crown()
    crown = build(gdf)

    with open(config.CROWN_JSON, "w") as file:
        json.dump(crown, file, indent=4)

    rings_total = sum(len(p["coords"]) for p in crown)
    print(f"{layer}: {len(gdf)} features -> {len(crown)} names, {rings_total} rings")
    print(f"-> {config.CROWN_JSON}")
# END GENERATED


if __name__ == '__main__':
    main()
