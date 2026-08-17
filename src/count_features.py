import sys

import geopandas as gpd

GDB_SOURCE = "PV_PARKRES_V.gdb"
COUNT_FIELD = "STYLE_TYPE"


def count_features(gdb_path, field):
    layer = gpd.list_layers(gdb_path)["name"][0]
    df = gpd.read_file(gdb_path, layer=layer, ignore_geometry=True)

    print(f"{layer}: {len(df)} features, {df[field].nunique()} distinct {field}")
    print(df[field].value_counts(dropna=False).to_string())
    return df[field].value_counts(dropna=False)


def main():
    field = sys.argv[1] if len(sys.argv) > 1 else COUNT_FIELD
    count_features(GDB_SOURCE, field)


if __name__ == "__main__":
    main()
