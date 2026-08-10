"""Dump the CROWNLAND.gdb attribute table to CSV: one column per field, one row per feature.

Usage:
    python crownland_to_csv.py                          # -> crownland.csv
    python crownland_to_csv.py CROWNLAND.gdb out.csv
"""

import sys

import geopandas as gpd

GDB_SOURCE = "CROWNLAND.gdb"
OUTPUT = "crownland.csv"


def read_attributes(gdb_path):
    """Every attribute column, no geometry (so the polygons are never parsed)."""
    layer = gpd.list_layers(gdb_path)["name"][0]
    return layer, gpd.read_file(gdb_path, layer=layer, ignore_geometry=True)


def main():
    gdb = sys.argv[1] if len(sys.argv) > 1 else GDB_SOURCE
    output = sys.argv[2] if len(sys.argv) > 2 else OUTPUT

    layer, df = read_attributes(gdb)
    df.to_csv(output, index=False)

    print(f"{layer}: {len(df)} rows x {len(df.columns)} columns -> {output}")
    print(", ".join(df.columns))


if __name__ == "__main__":
    main()
