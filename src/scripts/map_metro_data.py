import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # GENERATED

import config

# GENERATED
NAME_COLUMNS = ("Statutory reserve", "Known As", "Also known as")


def read_data():
    metro = pd.read_excel(config.METRO_LIST)
    with open(config.PARKS_JSON) as file:
        parks = json.load(file)
    return metro, parks


def map_data(metro, parks):
    # TODO
    return []


def main():
    metro, parks = read_data()
    missed = map_data(metro, parks)
    print(f"{len(metro)} rows, {len(missed)} missed")
# END GENERATED


if __name__ == '__main__':
    main()
