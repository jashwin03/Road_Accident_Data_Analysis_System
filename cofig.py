import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'road_accident.db'}")

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "outputs"
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = REPORT_DIR / "charts"

for _d in (RAW_DIR, OUTPUT_DIR, REPORT_DIR, CHART_DIR):
    _d.mkdir(parents=True, exist_ok=True)

SEVERITY_CATEGORIES = ["Fatal", "Serious", "Minor"]