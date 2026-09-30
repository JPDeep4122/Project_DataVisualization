from config import RAW_DATA_DIR
import pandas as pd

from ingestion import load_all_data
from pprint import pprint

def audit_structure(data: dict[str, pd.DataFrame]) -> dict[str, dict]:
    """
    Kiểm tra cấu trúc cơ bản của từng DataFrame:
    - Số dòng
    - Số cột
    - Tên cột
    - Kiểu dữ liệu
    """
    result = {}

    for name, df in data.items():
        result[name] = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict()
        }

    return result

def audit_duplicate(data: dict[str, pd.DataFrame]) -> dict[str, int]:
    """
    Kiểm tra số dòng bị trùng hoàn toàn trong từng DataFrame.

    Lưu ý:
    Đây là duplicate toàn bộ row, không phải duplicate của một cột khóa.
    """
    result = {}

    for name, df in data.items():
        result[name] = int(df.duplicated().sum())

    return result

def audit_key(data: dict[str, pd.DataFrame]) -> dict[str, dict]:
    """
    Kiểm tra các khóa chính được xác định cho từng bảng.

    Không kiểm tra credits.id như Primary Key vì credits.id
    là khóa ngoại tham chiếu đến titles.id và được phép lặp.
    """
    key_columns = {
        "netflix_titles": "show_id",
        "titles": "id"
    }

    result = {}

    for name, key in key_columns.items():
        df = data[name]

        result[name] = {
            "key": key,
            "null_count": int(df[key].isna().sum()),
            "duplicate_count": int(df[key].duplicated().sum()),
            "unique_count": int(df[key].nunique())
        }

    return result

def audit_relationship(
    parent_table: pd.DataFrame,
    child_table: pd.DataFrame,
    parent_name: str,
    child_name: str,
    parent_key: str,
    child_key: str
) -> dict:
    """
    Kiểm tra quan hệ giữa bảng cha và bảng con.

    Ví dụ:
        titles.id      -> credits.id

    Kiểm tra:
    - Số dòng của parent/child
    - Số khóa duy nhất
    - Child key có tồn tại trong parent hay không
    - Số orphan key
    - Số parent không có child
    - Referential integrity
    """

    parent_ids = set(parent_table[parent_key].dropna())
    child_ids = set(child_table[child_key].dropna())

    orphan_child_keys = child_ids - parent_ids
    parent_without_child = parent_ids - child_ids

    return {
        "parent_table": parent_name,
        "parent_key": parent_key,
        "child_table": child_name,
        "foreign_key": child_key,
        "parent_rows": len(parent_table),
        "child_rows": len(child_table),
        "parent_keys": len(parent_ids),
        "child_keys": len(child_ids),
        "orphan_child_keys": len(orphan_child_keys),
        "parent_without_child": len(parent_without_child),
        "referential_integrity": child_ids.issubset(parent_ids)
    }

def audit_multivalue( data: dict[str, pd.DataFrame]) -> dict[str, dict[str, dict]]:
    """
    Kiểm tra các cột chứa nhiều giá trị trong cùng một cell.

    Hiện tại kiểm tra:
    - netflix_titles.listed_in
    - netflix_titles.country

    Mục đích:
    Phát hiện các cột cần normalize/explode thành bridge table.
    """
    multivalue_columns = {
        "netflix_titles": ["listed_in", "country"]
    }

    result = {}

    for table_name, columns in multivalue_columns.items():
        df = data[table_name]
        result[table_name] = {}

        for column in columns:
            series = df[column].dropna().astype(str)
            multi_count = int(series.str.contains(",", regex=False).sum())
            value_counts = series.str.split(",").str.len()

            result[table_name][column] = {
                "non_null_count": int(series.count()),
                "multivalue_rows": multi_count,
                "single_value_rows": int((value_counts == 1).sum()),
                "max_values_per_row": int(value_counts.max()),
                "average_values_per_row": float(value_counts.mean())
            }

    return result

def audit_date(
    data: dict[str, pd.DataFrame]
) -> dict[str, dict]:
    """
    Kiểm tra các cột ngày quan trọng.

    Hiện tại tập trung vào:
    netflix_titles.date_added
    """
    date_columns = {
        "netflix_titles": ["date_added"]
    }
    result = {}

    for table_name, columns in date_columns.items():
        df = data[table_name]
        result[table_name] = {}

        for column in columns:
            parsed = pd.to_datetime(df[column], errors="coerce")

            result[table_name][column] = {
                "original_dtype": str(df[column].dtype),
                "null_count": int(df[column].isna().sum()),
                "invalid_count": int(parsed.isna().sum() - df[column].isna().sum()),
                "min_date": (parsed.min().strftime("%Y-%m-%d") if parsed.notna().any() else None),
                "max_date": (parsed.max().strftime("%Y-%m-%d") if parsed.notna().any() else None)
            }
    return result

def audit_scope(
    data: dict[str, pd.DataFrame],
    start_year: int = 2011,
    end_year: int = 2020
) -> dict:
    """
    Kiểm tra phạm vi dữ liệu theo date_added.

    Project hiện tại:
        2011 <= year(date_added) <= 2020
    """
    df = data["netflix_titles"].copy()

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

def run_audit(data: dict[str, pd.DataFrame]) -> dict:
    """
    Chạy toàn bộ audit và trả về một dictionary duy nhất.
    """
    return {
        "structure": audit_structure(data),
        "duplicate": audit_duplicate(data),
        "key": audit_key(data),
        "relationship": {
            "titles_credits": audit_relationship(
                parent_table=data["titles"],
                child_table=data["credits"],
                parent_name="titles",
                child_name="credits",
                parent_key="id",
                child_key="id"
            )
        },
        "multivalue": audit_multivalue(data),
        "date": audit_date(data),
        "scope": audit_scope(data)
    }

if __name__ == "__main__":
    data = load_all_data()
    audit_result = run_audit(data)
    for name, result in audit_result.items():
        print(name)
        pprint(result)
        print('-'*100)