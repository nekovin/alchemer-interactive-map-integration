# Running

The venv is already active. Scripts are installed as console entry points via `[project.scripts]` in `pyproject.toml` — call them by name, no `python -m`, no `.venv/bin/` prefix.

```
process-metro-data     # metro list -> data/metro.csv
process-types          # metro/pier/reserve -> data/types.csv (needs metro.csv first)
build-parks-vic        # -> src/parksres/parks_vic_data.json (needs types.csv first)
```

After adding a new entry point, re-run `pip install -e .`.

# Instructions

- Work from `PV_PARKRES_V.gdb` only. No CROWNLAND.
- Never read the contents of files in `data/`. Column names and schema only.
- References go in `docs/reference.md`.
