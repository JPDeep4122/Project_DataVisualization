from typing import Any
import pandas as pd

from ingestion import load_netflix_titles
from pprint import pprint


def audit_structure(df: pd.DataFrame) -> dict[str, Any]:
    """
    Kiểm tra cấu trúc cơ bản của DataFrame:
    - Số dòng
    - Số cột
    - Tên cột
    - Kiểu dữ liệu
    """

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict()
    }


def audit_duplicate(df: pd.DataFrame) -> int:
    """Kiểm tra số dòng bị trùng hoàn toàn trong DataFrame."""

    return int(df.duplicated().sum())


def audit_key(df: pd.DataFrame, key_column: str | None = None) -> dict[str, Any] | None:
    """Kiểm tra tính chính xác của trường key_column"""
    if not key_column:
        key_column = df.columns[df.columns.str.contains(r"id$", case=False, regex=True)].tolist()
        if not key_column:
            print("Dữ liệu đã cho không có trường định danh")
            return
        if len(key_column) > 1:
            print("Dữ liệu đã cho có hơn 1 cột định danh, lấy cột định danh đầu tiên.")
        key_column = key_column[0]

    return {
        "key": key_column,
        "null_count": int(df[key_column].isna().sum()),
        "duplicate_count": int(df[key_column].duplicated().sum()),
        "unique_count": int(df[key_column].nunique())
    }


def audit_multivalue(df: pd.DataFrame) -> dict[str, Any]:
    """Kiểm tra các cột chứa nhiều giá trị trong cùng một cell."""
    result = {}
    for column in list(df.columns):
        series = df[column].dropna().astype(str)
        multi_count = int(series.str.contains(",", regex=False).sum())
        value_counts = series.str.split(",").str.len()
        avg_values_per_row = float(value_counts.mean())
        if avg_values_per_row != 1:
            result[column] = {
                "non_null_count": int(series.count()),
                "multivalue_rows": multi_count,
                "single_value_rows": int((value_counts == 1).sum()),
                "max_values_per_row": int(value_counts.max()),
                "average_values_per_row": avg_values_per_row
            }
    return result


def audit_date(df: pd.DataFrame) -> dict[str, dict[str, Any]] | None:
    """Kiểm tra các cột ngày quan trọng."""
    date_columns = df.columns[df.columns.str.contains(r"^date", case=False, regex=True)].tolist()
    if not date_columns:
        print("Dữ liệu đã cho không có trường ngày tháng")
        return

    result = {}
    for date_cols in date_columns:
        parsed = pd.to_datetime(df[date_cols], errors="coerce")
        result[date_cols] = {
            "original_dtype": str(df[date_cols].dtype),
            "null_count": int(df[date_cols].isna().sum()),
            "invalid_count": int(parsed.isna().sum() - df[date_cols].isna().sum()),
            "min_date": (parsed.min().strftime("%Y-%m-%d") if parsed.notna().any() else None),
            "max_date": (parsed.max().strftime("%Y-%m-%d") if parsed.notna().any() else None)
        }

    return result


def audit_scope(
    df: pd.DataFrame,
    start_year: int = 2011,
    end_year: int = 2020
) -> dict[str, Any]:
    """
    Kiểm tra phạm vi dữ liệu theo date_added.
    Project hiện tại: 2011 <= year(date_added) <= 2020
    """
    dates = pd.to_datetime(df["date_added"], errors="coerce")
    years = dates.dt.year
    in_scope = years.between(start_year, end_year)

    return {
        "scope_column": "date_added",
        "start_year": start_year,
        "end_year": end_year,
        "total_rows": len(df),
        "in_scope_rows": int(in_scope.sum()),
        "out_of_scope_rows": int((~in_scope & years.notna()).sum()),
        "missing_date_rows": int(years.isna().sum()),
        "in_scope_percentage": float(in_scope.mean() * 100),
        "out_of_scope_years": sorted(years[~in_scope & years.notna()].unique().tolist())
    }


def run_audit(df: pd.DataFrame) -> dict[str, Any]:
    """Chạy toàn bộ audit và trả về một dictionary duy nhất."""
    return {
        "structure": audit_structure(df),
        "duplicate": audit_duplicate(df),
        "key": audit_key(df),
        "multivalue": audit_multivalue(df),
        "date": audit_date(df),
        "scope": audit_scope(df)
    }


if __name__ == "__main__":
    df = load_netflix_titles()
    audit_result = run_audit(df)
    for name, result in audit_result.items():
        print(name)
        pprint(result)
        print('-'*100)
    for column in audit_result["multivalue"].keys():
        print(df[column].head())
        print('-'*100)