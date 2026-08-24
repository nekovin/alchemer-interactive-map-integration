import pandas as pd

from parksres import config
from parksres.common import normalise, read_parks, show

# GENERATED
LABEL = "Label"
CATEGORY = "Category"
KNOWN_AS = "Known as"
PART_OF = "Part Of"
FALLBACKS = (KNOWN_AS, PART_OF)

EXCLUDE = {normalise(n) for n in
           ("Other Specify", "No other park visited", "Don`t know")}


def read_sources():
    metro = pd.read_csv(config.METRO_CSV)
    pv = pd.read_excel(config.PV_PARKS_PIERS)
    return metro, pv


def match(index, candidates):
    for position, value in enumerate(candidates):
        if pd.isna(value) or not str(value).strip():
            continue
        park = index.get(normalise(value))
        if park:
            return park, position
    return {}, -1


def map_types(metro, pv, parks):
    index = {normalise(p["name"]): p for p in parks}

    # map_metro_data already resolved these via Known As, so reuse its hit
    rows = [{"source": "metro", "name": name, "category": "metro",
             "candidates": [hit], "columns": ["label"], "known_as": bool(known_as)}
            for name, hit, known_as in zip(metro["reserve"],
                                           metro["park"].fillna(""),
                                           metro["known_as"].fillna(False))]
    rows += [{"source": "pv", "name": row[LABEL], "category": row[CATEGORY],
              "candidates": [row[LABEL]] + [row[c] for c in FALLBACKS],
              "columns": ["label"] + list(FALLBACKS), "known_as": False}
             for row in pv.to_dict("records")]

    seen = {}
    for row in rows:
        if normalise(row["name"]) in EXCLUDE:
            continue
        park, position = match(index, row.pop("candidates"))
        column = row.pop("columns")[position] if park else ""
        row |= {
            "matched": bool(park),
            "matched_on": column,
            "known_as": bool(park) and (row["known_as"] or column == KNOWN_AS),
            "part_of": column == PART_OF,
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
    print(f"\n{table['matched_on'].value_counts().to_string()}")
    print(f"\nmissing:\n{table[~table['matched']][['source', 'name']].to_string(index=False)}")

    table.to_csv(config.TYPES_CSV, index=False)
    table[~table["matched"]].to_csv(config.MISSING_CSV, index=False)
    print(f"\n-> {config.TYPES_CSV}")
    print(f"-> {config.MISSING_CSV}")
# END GENERATED


if __name__ == '__main__':
    main()
