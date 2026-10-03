"""
Tạo SQLite database từ 5 bảng dữ liệu chuẩn hóa.

Database:
    database/netflix.db

Quan hệ:
    dim_date
        ↑
        ├── dim_title
        └── fact_monthly_addition

    dim_title
        ↑
        ├── bridge_genre
        └── bridge_country
"""
from pathlib import Path
from typing import Any
import sqlite3
import pandas as pd

from config import NORMALIZED_DATA_DIR, DATABASE_DIR


DATABASE_FILE: Path = Path(DATABASE_DIR) / "netflix.db"


SCHEMAS: dict[str, str] = {
    "dim_date": """
        CREATE TABLE dim_date (
            date_key INTEGER PRIMARY KEY,
            date TEXT NOT NULL UNIQUE,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            month_name TEXT NOT NULL,
            quarter INTEGER NOT NULL,
            quarter_name TEXT NOT NULL
        )
    """,

    "dim_title": """
        CREATE TABLE dim_title (
            show_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            date_added TEXT NOT NULL,
            date_key INTEGER NOT NULL,
            release_year INTEGER,
            rating TEXT,
            duration_minutes INTEGER,
            duration_seasons INTEGER,

            FOREIGN KEY (date_key)
                REFERENCES dim_date(date_key)
        )
    """,

    "bridge_genre": """
        CREATE TABLE bridge_genre (
            show_id TEXT NOT NULL,
            genre TEXT NOT NULL,

            PRIMARY KEY (show_id, genre),

            FOREIGN KEY (show_id)
                REFERENCES dim_title(show_id)
        )
    """,

    "bridge_country": """
        CREATE TABLE bridge_country (
            show_id TEXT NOT NULL,
            country TEXT NOT NULL,
            country_code TEXT,

            PRIMARY KEY (show_id, country),

            FOREIGN KEY (show_id)
                REFERENCES dim_title(show_id)
        )
    """,

    "fact_monthly_addition": """
        CREATE TABLE fact_monthly_addition (
            date_key INTEGER PRIMARY KEY,
            monthly_additions INTEGER NOT NULL CHECK (monthly_additions >= 0),
            month_index INTEGER NOT NULL UNIQUE,

            FOREIGN KEY (date_key)
                REFERENCES dim_date(date_key)
        )
    """,
}


DROP_ORDER: list[str] = [
    "fact_monthly_addition",
    "bridge_genre",
    "bridge_country",
    "dim_title",
    "dim_date",
]

LOAD_ORDER: list[str] = [
    "dim_date",
    "dim_title",
    "fact_monthly_addition",
    "bridge_genre",
    "bridge_country",
]


def create_database(db_path: str | Path = DATABASE_FILE) -> Path:
    """Tạo database và các bảng với PK/FK/constraints."""
    output_path = Path(db_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(output_path)

    try:
        conn.execute("PRAGMA foreign_keys = ON;")

        for table_name in DROP_ORDER:
            conn.execute(f"DROP TABLE IF EXISTS {table_name};")

        for table_name in LOAD_ORDER:
            conn.execute(SCHEMAS[table_name])

        conn.commit()

    finally:
        conn.close()

    return output_path


def load_csv_to_database(db_path: str | Path = DATABASE_FILE) -> None:
    """Nạp 5 CSV chuẩn hóa vào SQLite."""
    conn = sqlite3.connect(Path(db_path))

    try:
        conn.execute("PRAGMA foreign_keys = ON;")

        for table_name in LOAD_ORDER:
            csv_path = (
                Path(NORMALIZED_DATA_DIR)
                / f"{table_name}.csv"
            )

            df = pd.read_csv(csv_path)

            df.to_sql(
                table_name,
                conn,
                if_exists="append",
                index=False,
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def validate_database(
    db_path: str | Path = DATABASE_FILE
) -> tuple[dict[str, int], list[tuple[Any, ...]]]:
    """Kiểm tra số dòng và khóa ngoại sau khi import."""
    conn = sqlite3.connect(Path(db_path))

    try:
        conn.execute("PRAGMA foreign_keys = ON;")

        results: dict[str, int] = {}

        for table_name in LOAD_ORDER:
            row = conn.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()

            results[table_name] = int(row[0])

        foreign_key_errors = conn.execute(
            "PRAGMA foreign_key_check;"
        ).fetchall()

        return results, foreign_key_errors

    finally:
        conn.close()


def main() -> None:
    print("=" * 60)
    print("TẠO SQLITE DATABASE")
    print("=" * 60)

    db_path = create_database()
    print(f"Đã tạo: {db_path}")

    load_csv_to_database(db_path)
    print("Đã nạp dữ liệu từ CSV.")

    row_counts, fk_errors = validate_database(db_path)

    print("\nSỐ DÒNG:")
    for table_name, count in row_counts.items():
        print(f"{table_name:<25} {count:>6}")

    print("\nFOREIGN KEY CHECK:")
    if fk_errors:
        for error in fk_errors:
            print(error)
        raise SystemExit(1)

    print("PASS - Không có lỗi khóa ngoại.")
    print(f"\nDatabase hoàn tất: {db_path}")


if __name__ == "__main__":
    main()
