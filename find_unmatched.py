"""Suggest park-name candidates for the labels gdb_to_json.py could not match.

For each unmatched label, scan its words against every park name and report the
names sharing the most words. Generic words ("park", "state", "reserve") appear in
hundreds of names, so they are ignored -- only distinctive words score a hit.

Usage:
    python find_unmatched.py
"""

import csv
import json
import re

import pandas as pd

PARKS_SOURCE = "parks_data.json"
UNMATCHED_SOURCE = "unmatched_labels.xlsx"
OUTPUT = "unmatched_hits.csv"

LABEL_FIELD = "Label"
MAX_HITS = 5
# a word in more than this many park names is too generic to be evidence.
MAX_DOC_FREQUENCY = 100


def words(name):
    """Distinct lowercase words in a name, punctuation stripped."""
    return set(re.sub(r"[^a-z0-9]+", " ", str(name).lower()).split())


def build_index(names):
    """{word: {names containing it}}, minus words too common to be meaningful."""
    index = {}
    for name in names:
        for word in words(name):
            index.setdefault(word, set()).add(name)
    return {w: n for w, n in index.items() if len(n) <= MAX_DOC_FREQUENCY}


def find_hits(label, index):
    """Park names sharing words with the label, most words shared first."""
    scores = {}
    for word in words(label):
        for name in index.get(word, ()):
            scores[name] = scores.get(name, 0) + 1
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:MAX_HITS]


def main():
    with open(PARKS_SOURCE) as file:
        data = json.load(file)

    names = [park["name"] for park in data]
    labels = pd.read_excel(UNMATCHED_SOURCE)[LABEL_FIELD].tolist()
    index = build_index(names)

    with open(OUTPUT, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([LABEL_FIELD, "n_hits", "hits"])
        for label in labels:
            hits = find_hits(label, index)
            writer.writerow(
                [label, len(hits), " | ".join(f"{name} ({n})" for name, n in hits)]
            )

    print(f"{len(labels)} labels -> {OUTPUT}")


if __name__ == "__main__":
    main()
