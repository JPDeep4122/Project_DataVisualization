"""
Pipeline toàn diện chạy toàn bộ luồng xử lý dữ liệu của dự án:
1. Ingestion: Đọc dữ liệu thô từ data/raw/
2. Cleaning: Làm sạch dữ liệu và lưu vào data/processed/
3. Normalization: Chuẩn hóa 5 bảng phân tích và lưu vào data/normalized/
4. Validation: Kiểm tra tính toàn vẹn và xuất báo cáo JSON
5. Database: Khởi tạo SQLite database tại database/netflix.db
"""
from pathlib import Path
from typing import Any
import pandas as pd

from ingestion import load_netflix_titles
from cleaning import clean_netflix_titles, save_cleaned_data
from normalization import normalize_data, save_normalized_data
from validation import load_normalized_data, build_report, save_report
from database import create_database, load_csv_to_database, validate_database
from config import START_YEAR, END_YEAR


def run_pipeline(
    start_year: int = START_YEAR,
    end_year: int = END_YEAR
) -> None:
    """Chạy toàn bộ pipeline ETL và khởi tạo cơ sở dữ liệu."""
    print("=" * 60)
    print("BẮT ĐẦU DATA PIPELINE")
    print("=" * 60)

    # 1. Ingestion
    print("\n[1/5] Ingestion: Đọc dữ liệu thô...")
    raw_df: pd.DataFrame = load_netflix_titles()

    # 2. Cleaning
    print("\n[2/5] Cleaning: Làm sạch dữ liệu...")
    cleaned_df: pd.DataFrame = clean_netflix_titles(raw_df)
    save_cleaned_data(cleaned_df)

    # 3. Normalization
    print("\n[3/5] Normalization: Chuẩn hóa mô hình dữ liệu...")
    normalized_data: dict[str, pd.DataFrame] = normalize_data(
        cleaned_df,
        start_year=start_year,
        end_year=end_year
    )
    save_normalized_data(normalized_data)

    # 4. Validation
    print("\n[4/5] Validation: Kiểm tra toàn vẹn dữ liệu...")
    validation_data: dict[str, pd.DataFrame] = load_normalized_data()
    report: dict[str, Any] = build_report(validation_data)
    save_report(report)
    print(f"Kết quả kiểm tra: {report['status']}")
    if report["status"] == "FAIL":
        raise ValueError(f"Dữ liệu không đạt kiểm tra: {report['errors']}")

    # 5. Database
    print("\n[5/5] Database: Khởi tạo và nạp SQLite database...")
    db_path: Path = create_database()
    load_csv_to_database(db_path)
    counts, fk_errors = validate_database(db_path)
    if fk_errors:
        raise ValueError(f"Lỗi khóa ngoại SQLite: {fk_errors}")

    print("\n" + "=" * 60)
    print(f"PIPELINE HOÀN TẤT THÀNH CÔNG! CSDL: {db_path}")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
