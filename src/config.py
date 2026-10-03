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

# Bảng ánh xạ thủ công cho các quốc gia lịch sử và các tên gọi thông dụng
COUNTRY_CODE_OVERRIDE: dict[str, str] = {
    # 1. Quốc gia lịch sử -> map về vùng lãnh thổ hiện tại để vẽ bản đồ
    "West Germany": "DEU",   # Đức
    "East Germany": "DEU",   # Đức
    "Soviet Union": "RUS",   # Nga

    # 2. Tên thông dụng khác với tên chuẩn ISO 3166-1
    "Turkey": "TUR",         # ISO: Türkiye
    "Russia": "RUS",         # ISO: Russian Federation
    "Palestine": "PSE",      # ISO: Palestine, State of
    "Vatican City": "VAT",   # ISO: Holy See (Vatican City State)
}