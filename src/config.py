from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
AUDIT_DATA_DIR = DATA_DIR / "audit"
NORMALIZED_DATA_DIR = DATA_DIR / "normalized"

DATABASE_DIR = PROJECT_ROOT / "database"
NETFLIX_DATABASE = DATABASE_DIR / "netflix.db"

START_YEAR = 2011
END_YEAR = 2020