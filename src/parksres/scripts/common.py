import json
import re

import pandas as pd

from parksres import config

# GENERATED
ABBREVIATIONS = {
    "st": "street",
    "rd": "road",
    "ave": "avenue",
    "av": "avenue",
    "pde": "parade",
    "cres": "crescent",
    "cr": "crescent",
    "dr": "drive",
    "hwy": "highway",
    "pl": "place",
    "ct": "court",
    "tce": "terrace",
    "ln": "lane",
    "esp": "esplanade",
    "pk": "park",
    "res": "reserve",
    "gdns": "gardens",
    "mt": "mount",
    "pt": "point",
    "nth": "north",
    "sth": "south",
    "e": "east",
    "w": "west",
}

# leading "st" is Saint, not Street: "St Kilda" vs "Dendy St"
LEADING = {"st": "saint"}


def expand(word, first):
    if first and word in LEADING:
        return LEADING[word]
    return ABBREVIATIONS.get(word, word)


def normalise(name):
    words = re.sub(r"[^a-z0-9]+", " ", str(name).lower().replace("&", "and")).split()
    return " ".join(expand(w, i == 0) for i, w in enumerate(words))


def read_parks():
    with open(config.PARKS_JSON) as file:
        return json.load(file)


def show(table):
    pd.set_option("display.max_rows", None, "display.width", 250)
    print(table.to_string(index=False))
# END GENERATED
