"""Export the attribute table to CSV, optionally filtered by style/area type.

PV_PARKRES_V holds its classification in STYLE_TYPE; other PARKRES variants use
AREA_TYPE, so whichever is present is used.

Usage:
    python export_attributes.py                 # everything
    python export_attributes.py metro           # rows whose style contains "metro"
    python export_attributes.py "regional park" attributes.csv
"""

import sys

import geopandas as gpd

GDB_SOURCE = "PV_PARKRES_V.gdb"
OUTPUT = "attributes.csv"

# substring, case-insensitive: "metro" matches "METROPOLITAN PARK". None = no filter.
STYLE_FILTER = None
#STYLE_FILTER = 'METROPOLITAN PARK'
STYLE_FIELDS = ("AREA_TYPE", "STYLE_TYPE")


def style_field(df):
    """Whichever style column this schema uses."""
    for field in STYLE_FIELDS:
        if field in df.columns:
            return field
    raise KeyError(f"none of {STYLE_FIELDS} in {list(df.columns)}")


def export(gdb_path, style_filter=STYLE_FILTER, output=OUTPUT):
    layer = gpd.list_layers(gdb_path)["name"][0]
    # ignore_geometry: attributes only, so the polygons are never parsed.
    df = gpd.read_file(gdb_path, layer=layer, ignore_geometry=True)
    field = style_field(df)

    if style_filter:
        df = df[df[field].str.contains(style_filter, case=False, na=False)]

    df.to_csv(output, index=False)
    print(f"{layer}: {len(df)} rows x {len(df.columns)} cols -> {output}")
    print(df[field].value_counts().to_string())
    return df


def main():
    style_filter = sys.argv[1] if len(sys.argv) > 1 else STYLE_FILTER
    output = sys.argv[2] if len(sys.argv) > 2 else OUTPUT
    export(GDB_SOURCE, style_filter, output)


if __name__ == "__main__":
    main()
