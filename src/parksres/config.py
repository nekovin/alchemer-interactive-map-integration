import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# GENERATED
_root = Path(os.getenv("REPOROOT") or "")
ROOT = _root if _root.is_dir() else Path(__file__).resolve().parents[2]

DATADIR = ROOT / "data"
PACKAGEDIR = ROOT / "src" / "parksres"

GDB = ROOT / "PV_PARKRES_V.gdb"
METRO_LIST = DATADIR / "Metro Park List FINAL.xlsx"
PV_PARKS_PIERS = DATADIR / "PV_parks_piers.xlsx"

PARKS_JSON = PACKAGEDIR / "parks_data.json"
PARKS_VIC_JSON = PACKAGEDIR / "parks_vic_data.json"
METRO_CSV = DATADIR / "metro.csv"
TYPES_CSV = DATADIR / "types.csv"

KEY = os.getenv("key")
# END GENERATED
