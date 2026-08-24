import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# GENERATED
_root = Path(os.getenv("REPOROOT") or "")
ROOT = _root if _root.is_dir() else Path(__file__).resolve().parents[2]

DATADIR = ROOT / "data"
PACKAGEDIR = ROOT / "src" / "parksres"

GDB = DATADIR / "PV_PARKRES_V.gdb"
METRO_LIST = DATADIR / "Metro Park List FINAL.xlsx"
PV_PARKS_PIERS = DATADIR / "PV_parks_piers.xlsx"

PARKS_JSON = DATADIR / "parks_data.json"
PARKS_VIC_JSON = DATADIR / "parks_vic_data_full.json"
METRO_CSV = DATADIR / "metro.csv"
TYPES_CSV = DATADIR / "types.csv"
MISSING_CSV = DATADIR / "missing.csv"

KEY = os.getenv("key")
# END GENERATED

CROWN_GDB = DATADIR / "Order_RWJCZ1/ll_gda2020/filegdb/whole_of_dataset/victoria/CROWNLAND.gdb"
CROWN_JSON = DATADIR / "crown_data.json"

PV_SOURCE = DATADIR / "PV_parks_piers.xlsx"
UNMATCHED_OUTPUT = DATADIR / "unmatched_labels.xlsx"

DEFAULT_COLOR = "#0B5EDA"
SELECTED_COLOR = "#FF0000"
UNMANAGED_COLOR = "#2E7D32"