import json

import pandas as pd

from parksres import config
from parksres.scripts.common import normalise, read_parks, show

# GENERATED
DEFAULT_COLOR = "#2E7D32"
SELECTED_COLOR = "#FF9800"


def read_types():
    types = pd.read_csv(config.TYPES_CSV)
    return types[types["matched"]]


def build(types, parks):
    index = {normalise(p["name"]): p for p in parks}

    out = {}
    for row in types.to_dict("records"):
        park = index.get(normalise(row["park"]))
        if park is None:
            continue
        out[park["name"]] = {
            "id": park["name"].lower().replace(" ", "_"),
            "name": park["name"],
            "defaultColor": DEFAULT_COLOR,
            "selectedColor": SELECTED_COLOR,
            "coords": park["coords"],
            "type": park.get("type"),
            "category": row["category"],
            "label": row["name"],
            "knownAs": bool(row["known_as"]),
        }
    return list(out.values())


def main():
    types = read_types()
    parks_vic = build(types, read_parks())

    with open(config.PARKS_VIC_JSON, "w") as file:
        json.dump(parks_vic, file, indent=4)

    show(pd.DataFrame(
        [{k: v for k, v in p.items() if k != "coords"} for p in parks_vic]
    ))
    print(f"\n{len(types)} matched entries -> {len(parks_vic)} parks")
    print(f"\n-> {config.PARKS_VIC_JSON}")
# END GENERATED


if __name__ == '__main__':
    main()
