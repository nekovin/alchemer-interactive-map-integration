import argparse
import json

import pandas as pd

from parksres import config
from parksres.common import normalise, read_parks, show

# GENERATED
DEFAULT_COLOR = "#0B5EDA"
SELECTED_COLOR = "#FF0000"
UNMANAGED_COLOR = "#2E7D32"

UNMANAGED_CATEGORY = "Other"

CATEGORY_RENAME = {
    "METRO PARKS/GARDENS": "Metro",
    "metro": "Metro",
    "NATIONAL/STATE PARKS": "State",
}


def rename(category):
    return CATEGORY_RENAME.get(category, category)


def read_types():
    types = pd.read_csv(config.TYPES_CSV)
    return types[types["matched"]]


def entry(park, row=None):
    return {
        "id": park["name"].lower().replace(" ", "_"),
        "name": park["name"],
        "defaultColor": DEFAULT_COLOR if row is not None else UNMANAGED_COLOR,
        "selectedColor": SELECTED_COLOR,
        "coords": park["coords"],
        "type": park.get("type"),
        "category": rename(row["category"]) if row is not None else UNMANAGED_CATEGORY,
        "label": row["name"] if row is not None else park["name"],
        "knownAs": bool(row["known_as"]) if row is not None else False,
    }


def build(types, parks, keep_all=False):
    index = {normalise(p["name"]): p for p in parks}

    out = {}
    for row in types.to_dict("records"):
        park = index.get(normalise(row["park"]))
        if park is None:
            continue
        out[park["name"]] = entry(park, row)

    if keep_all:
        for park in parks:
            out.setdefault(park["name"], entry(park))
    return list(out.values())


def main():
    parser = argparse.ArgumentParser(
        description="Build parks_vic_data.json from parks_data.json + types.csv")
    parser.add_argument("-a", "--all", action="store_true",
                        help="include every park, uncategorised ones tagged Other")
    args = parser.parse_args()

    types = read_types()
    parks_vic = build(types, read_parks(), keep_all=args.all)

    with open(config.PARKS_VIC_JSON, "w") as file:
        json.dump(parks_vic, file, indent=4)

    show(pd.DataFrame(
        [{k: v for k, v in p.items() if k != "coords"} for p in parks_vic]
    ))
    listed = sum(p["category"] != UNMANAGED_CATEGORY for p in parks_vic)
    print(f"\n{len(types)} matched entries -> {len(parks_vic)} parks "
          f"({listed} categorised, {len(parks_vic) - listed} {UNMANAGED_CATEGORY})")
    print(f"\n-> {config.PARKS_VIC_JSON}")
# END GENERATED


if __name__ == '__main__':
    main()
