import pandas as pd

from parksres import config
from parksres.scripts.common import normalise, read_parks, show

# GENERATED
def read_sources():
    metro = pd.read_csv(config.METRO_CSV)
    pv = pd.read_excel(config.PV_PARKS_PIERS)
    return metro, pv


def map_types(metro, pv, parks):
    index = {normalise(p["name"]): p for p in parks}

    # map_metro_data already resolved these via Known As, so reuse its hit
    rows = [{"source": "metro", "name": name, "category": "metro",
             "hit": hit, "known_as": bool(known_as)}
            for name, hit, known_as in zip(metro["reserve"],
                                           metro["park"].fillna(""),
                                           metro["known_as"].fillna(False))]
    rows += [{"source": "pv", "name": label, "category": category,
              "hit": label, "known_as": False}
             for label, category in zip(pv["Label"], pv["Category"])]

    seen = {}
    for row in rows:
        park = index.get(normalise(row.pop("hit")), {})
        row |= {
            "matched": bool(park),
            "known_as": row["known_as"] and bool(park),
            "park": park.get("name", ""),
            "type": park.get("type", ""),
        }
        seen.setdefault(normalise(row["name"]), row)
    return pd.DataFrame(seen.values())


def main():
    metro, pv = read_sources()
    table = map_types(metro, pv, read_parks())

    show(table)
    print(f"\n{len(table)} entries, {table['matched'].sum()} matched, "
          f"{(~table['matched']).sum()} missing, "
          f"{table['known_as'].sum()} via known-as")
    print(f"\n{table['category'].value_counts().to_string()}")
    print(f"\nmissing:\n{table[~table['matched']][['source', 'name']].to_string(index=False)}")

    table.to_csv(config.TYPES_CSV, index=False)
    print(f"\n-> {config.TYPES_CSV}")
# END GENERATED


if __name__ == '__main__':
    main()
