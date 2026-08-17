import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# GENERATED
ROOT = Path(os.getenv("REPOROOT") or "")
if not ROOT.is_dir():
    ROOT = Path(__file__).resolve().parents[1]

DATADIR = ROOT / "data"
PACKAGEDIR = ROOT / "src" / "parksres"

GDB = ROOT / "PV_PARKRES_V.gdb"
METRO_LIST = DATADIR / "Metro Park List FINAL.xlsx"

PARKS_JSON = PACKAGEDIR / "parks_data.json"

KEY = os.getenv("key")
# END GENERATED
