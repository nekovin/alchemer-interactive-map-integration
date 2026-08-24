import pandas as pd

from parksres import config
from parksres.common import normalise, read_parks, show
from typing import Optional
#import argparse
from argparse import Namespace, ArgumentParser

# GENERATED
NAME_COLUMNS = ("Statutory reserve listed in Schedule 2", "Known As", "Also known as") # 6 columns for Also known as


def read_data():
    return pd.read_excel(config.METRO_LIST), read_parks()


def map_data(metro, parks):
    index = {normalise(p["name"]): p for p in parks}
    columns = [c for c in metro.columns if str(c).strip().startswith(NAME_COLUMNS)]

    rows = []
    for _, row in metro.iterrows():
        hits = [(c, index[normalise(row[c])])
                for c in columns
                if pd.notna(row[c]) and normalise(row[c]) in index]
        column, park = hits[0] if hits else ("", {})
        rows.append({
            "reserve": row[columns[0]],
            "matched": bool(hits),
            "matched_on": column,
            "known_as": bool(hits) and not column.startswith(NAME_COLUMNS[0]),
            "park": park.get("name", ""),
            "type": park.get("type", ""),
            "pv_category": park.get("pvCategory", ""),
            "n_hits": len(hits),
        })
    return pd.DataFrame(rows)

class Args(Namespace):
    save: bool
    
from collections.abc import Sequence

def main(argv: Sequence[str] | None=None) -> None:
    
    parser = ArgumentParser(
        description="Add 'save' if you want to save the data"
    )
    
    #save: Optional[bool]
    
    parser.add_argument('--save', action="store_true")
    
    args: Args = parser.parse_args(argv)
    
    save = args.save
    
    metro, parks = read_data()
    table = map_data(metro, parks)

    show(table)
    print(f"\n{len(table)} reserves, {table['matched'].sum()} matched, "
          f"{(~table['matched']).sum()} missing, "
          f"{table['known_as'].sum()} via known-as")
    print(f"\n{table[table['matched']]['type'].value_counts(dropna=False).to_string()}")
    print(f"\nmissing:\n{table[~table['matched']]['reserve'].to_string(index=False)}")

    if save:
        table.to_csv(config.METRO_CSV, index=False)
        print(f"\n-> {config.METRO_CSV}")
    else:
        print("\nnot saved (use --save)")
# END GENERATED



if __name__ == '__main__':
    main()
