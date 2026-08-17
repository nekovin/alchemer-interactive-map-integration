import json
import re

import pandas as pd

from parksres import config

# GENERATED
NAME_COLUMNS = ("Statutory reserve listed in Schedule 2", "Known As", "Also known as") # 6 columns for Also known as


def read_data():
    metro = pd.read_excel(config.METRO_LIST)
    with open(config.PARKS_JSON) as file:
        parks = json.load(file)
    return metro, parks


def normalise(name):
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower().replace("&", "and")).strip()


def map_data(metro, parks):
    index = {normalise(p["name"]): p["name"] for p in parks}
    columns = [c for c in metro.columns if str(c).strip().startswith(NAME_COLUMNS)]

    rows = []
    for _, row in metro.iterrows():
        hits = [(c, row[c], index[normalise(row[c])])
                for c in columns
                if pd.notna(row[c]) and normalise(row[c]) in index]
        rows.append({
            "reserve": row[columns[0]],
            "matched": bool(hits),
            "matched_on": hits[0][0] if hits else "",
            "known_as": bool(hits) and not hits[0][0].startswith(NAME_COLUMNS[0]),
            "park": hits[0][2] if hits else "",
            "n_hits": len(hits),
        })
    return pd.DataFrame(rows)


def main():
    metro, parks = read_data()
    table = map_data(metro, parks)

    pd.set_option("display.max_rows", None, "display.width", 200)
    print(table.to_string(index=False))
    print(f"\n{len(table)} reserves, {table['matched'].sum()} matched, "
          f"{(~table['matched']).sum()} missing, "
          f"{table['known_as'].sum()} via known-as")
    table.to_csv(config.DATADIR / "metro_mapped.csv", index=False)
# END GENERATED


if __name__ == '__main__':
    main()
