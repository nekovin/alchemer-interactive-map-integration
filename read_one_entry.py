"""Peek at one record from each source to see what fields are available.

Usage:
    python read_one_entry.py                    # first entry
    python read_one_entry.py "Bunyip State Park"  # entry matching that name
"""

import json
import sys

import geopandas as gpd

GDB_SOURCE = "PV_PARKRES_V.gdb"
PARKS_SOURCE = "4463_parks_data.json"
NAME_FIELD = "Albert Park"


def read_one_entry(gdb_path, name=None):
    """One row of the .gdb, every attribute column, geometry summarised."""
    layer = gpd.list_layers(gdb_path)["name"][0]
    if name is None:
        # max_features=1 so we read a single row, not all 3022.
        gdf = gpd.read_file(gdb_path, layer=layer, max_features=1)
    else:
        # filter in the driver: '' escapes a quote in SQL.
        escaped = name.replace("'", "''")
        gdf = gpd.read_file(gdb_path, layer=layer, where=f"{NAME_FIELD} = '{escaped}'")

    if gdf.empty:
        print(f"{layer}: no row with {NAME_FIELD} = {name!r}")
        return None

    row = gdf.iloc[0]
    print(f"layer: {layer} ({len(gdf)} match(es))")
    for field, value in row.items():
        if field == "geometry":
            print(f"  {field:<24} {value.geom_type}, {len(value.geoms)} part(s)")
        else:
            print(f"  {field:<24} {value!r}")
    return row


def read_one_park(parks_path, name=None):
    """One entry from the converted JSON, coords summarised."""
    with open(parks_path) as file:
        data = json.load(file)

    if name is None:
        park = data[0]
    else:
        park = next((p for p in data if p["name"] == name), None)

    print(f"\n{parks_path}: {len(data)} parks")
    if park is None:
        print(f"  no park named {name!r}")
        return None

    for key, value in park.items():
        if key == "coords":
            print(f"  {key:<24} {len(value)} ring(s), first point {value[0][0]}")
        else:
            print(f"  {key:<24} {value!r}")
    return park


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else None
    read_one_entry(GDB_SOURCE, name)
    #read_one_park(PARKS_SOURCE, name)


if __name__ == "__main__":
    main()
