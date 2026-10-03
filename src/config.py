from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
AUDIT_DATA_DIR: Path = DATA_DIR / "audit"
NORMALIZED_DATA_DIR: Path = DATA_DIR / "normalized"

DATABASE_DIR: Path = PROJECT_ROOT / "database"
NETFLIX_DATABASE: Path = DATABASE_DIR / "netflix.db"
DATABASE_PATH: Path = NETFLIX_DATABASE

START_YEAR: int = 2011
END_YEAR: int = 2020