"""
Kiểm tra tính toàn vẹn của 7 bảng dữ liệu chuẩn hóa trước khi đưa vào SQLite.

Thiết kế:
- Kiểm tra cấu trúc/cột bắt buộc
- Kiểm tra khóa chính: NULL + duplicate
- Kiểm tra khóa ngoại: không có orphan key
- Kiểm tra phạm vi thời gian 2011-2020
- Kiểm tra fact có đủ 120 tháng và tổng số title
"""
from pathlib import Path
from typing import Any
import json
import pandas as pd

from config import DATA_DIR, NORMALIZED_DATA_DIR, START_YEAR, END_YEAR


TABLES: dict[str, list[str]] = {
    "dim_date": [
        "date_key", "date", "year", "month",
        "month_name", "quarter", "quarter_name"
    ],
    "dim_title": [
        "show_id", "title", "type", "date_added", "date_key",
        "release_year", "rating", "duration_minutes", "duration_seasons"
    ],
    "bridge_genre": ["show_id", "genre"],
    "bridge_country": ["show_id", "country"],
    "bridge_director": ["show_id", "director"],
    "bridge_actor": ["show_id", "actor"],
    "fact_monthly_addition": [
        "date_key", "monthly_additions", "month_index"
    ],
}


def load_normalized_data(
    input_dir: str | Path = NORMALIZED_DATA_DIR
) -> dict[str, pd.DataFrame]:
    """Đọc 7 bảng CSV chuẩn hóa."""
    input_path = Path(input_dir)
    return {
        name: pd.read_csv(input_path / f"{name}.csv")
        for name in TABLES
    }


def validate_structure(data: dict[str, pd.DataFrame]) -> list[str]:
    """Kiểm tra đủ bảng và đủ cột bắt buộc."""
    errors: list[str] = []

    for table_name, required_columns in TABLES.items():
        if table_name not in data:
            errors.append(f"Thiếu bảng: {table_name}")
            continue

        missing = [
            col for col in required_columns
            if col not in data[table_name].columns
        ]

        if missing:
            errors.append(
                f"{table_name}: thiếu cột {', '.join(missing)}"
            )

    return errors


def validate_primary_keys(data: dict[str, pd.DataFrame]) -> list[str]:
    """Kiểm tra khóa chính của các bảng."""
    checks = {
        "dim_date": "date_key",
        "dim_title": "show_id",
        "fact_monthly_addition": "date_key",
    }

    errors: list[str] = []

    for table_name, key in checks.items():
        df = data[table_name]

        if df[key].isna().any():
            errors.append(f"{table_name}.{key}: có giá trị NULL")

        if df[key].duplicated().any():
            errors.append(f"{table_name}.{key}: có khóa trùng")

    return errors


def validate_foreign_keys(data: dict[str, pd.DataFrame]) -> list[str]:
    """Kiểm tra các quan hệ khóa ngoại."""
    valid_dates = set(data["dim_date"]["date_key"].dropna())
    valid_titles = set(data["dim_title"]["show_id"].dropna())

    checks = [
        ("dim_title", "date_key", valid_dates),
        ("fact_monthly_addition", "date_key", valid_dates),
        ("bridge_genre", "show_id", valid_titles),
        ("bridge_country", "show_id", valid_titles),
        ("bridge_director", "show_id", valid_titles),
        ("bridge_actor", "show_id", valid_titles)
    ]

    errors: list[str] = []

    for table_name, column, valid_keys in checks:
        actual_keys = set(data[table_name][column].dropna())
        orphan_keys = actual_keys - valid_keys

        if orphan_keys:
            errors.append(
                f"{table_name}.{column}: "
                f"{len(orphan_keys)} khóa ngoại không tồn tại"
            )

    return errors


def validate_business_rules(data: dict[str, pd.DataFrame]) -> list[str]:
    """Kiểm tra các quy tắc nghiệp vụ của mô hình phân tích."""
    errors: list[str] = []

    dim_date = data["dim_date"]
    dim_title = data["dim_title"]
    fact = data["fact_monthly_addition"]

    expected_dates = (
        pd.date_range(
            f"{START_YEAR}-01-01",
            f"{END_YEAR}-12-31",
            freq="D"
        )
    )

    expected_months = (END_YEAR - START_YEAR + 1) * 12

    if len(dim_date) != len(expected_dates):
        errors.append(
            f"dim_date: {len(dim_date)} dòng, "
            f"mong đợi {len(expected_dates)}"
        )

    if len(fact) != expected_months:
        errors.append(
            f"fact_monthly_addition: {len(fact)} dòng, "
            f"mong đợi {expected_months}"
        )

    if fact["monthly_additions"].lt(0).any():
        errors.append(
            "fact_monthly_addition.monthly_additions: "
            "có giá trị âm"
        )

    if fact["month_index"].tolist() != list(range(expected_months)):
        errors.append(
            "fact_monthly_addition.month_index: "
            "không liên tục từ 0 đến 119"
        )

    total_fact = int(fact["monthly_additions"].sum())

    if total_fact != len(dim_title):
        errors.append(
            "Tổng monthly_additions không bằng số dòng dim_title: "
            f"{total_fact} != {len(dim_title)}"
        )

    dates = pd.to_datetime(
        dim_title["date_added"],
        errors="coerce"
    )

    invalid_scope = ~dates.dt.year.between(START_YEAR, END_YEAR)

    if invalid_scope.any():
        errors.append(
            f"dim_title: {int(invalid_scope.sum())} "
            f"title nằm ngoài phạm vi {START_YEAR}-{END_YEAR}"
        )

    return errors


def build_report(data: dict[str, pd.DataFrame]) -> dict[str, Any]:
    """Tạo báo cáo validation có thể lưu thành JSON."""
    errors: list[str] = []
    errors.extend(validate_structure(data))

    # Chỉ kiểm tra sâu khi cấu trúc đã đủ.
    if not errors:
        errors.extend(validate_primary_keys(data))
        errors.extend(validate_foreign_keys(data))
        errors.extend(validate_business_rules(data))

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "tables": {
            name: {
                "rows": len(df),
                "columns": len(df.columns),
            }
            for name, df in data.items()
        },
    }


def save_report(
    report: dict[str, Any],
    output_dir: str | Path = DATA_DIR
) -> Path:
    """Lưu kết quả validation."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / "validation_report.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return output_file


def main() -> None:
    data = load_normalized_data()
    report = build_report(data)

    print("=" * 60)
    print("VALIDATION - DỮ LIỆU CHUẨN HÓA")
    print("=" * 60)

    for name, info in report["tables"].items():
        print(
            f"{name:<25} "
            f"{info['rows']:>6} dòng | "
            f"{info['columns']:>2} cột"
        )

    print(f"\nKết quả: {report['status']}")

    if report["errors"]:
        print("\nLỖI:")
        for error in report["errors"]:
            print(f"- {error}")
    else:
        print("Tất cả kiểm tra đều đạt.")

    output_file = save_report(report)
    print(f"\nĐã lưu báo cáo: {output_file}")

    if report["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
