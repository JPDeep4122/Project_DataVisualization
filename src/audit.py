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

if __name__ == "__main__":
    for name, descript in audit_key(load_all_data()).items():
        print(name)
        pprint(descript)
        print("-"*100)

    data = load_all_data()
    print(f"các cột của credits:\n{data["credits"].columns.tolist()}")
    print("-"*100)
    print(f"20 dòng đầu của credits:\n{data["credits"].head(20).to_string()}")
    print("-"*100)
    print(f"thông tin chung về credits:\n{data["credits"].info()}")
    print("-"*100)
    print(data["credits"].groupby("id").agg(times=("id", "count")).reset_index())
    print("-"*100)

    pprint(audit_relationship(data["titles"], data["credits"]))
    print("-"*100)
    print(f"5 dòng đầu của bảng credits:\n{data["credits"].head()}")
    print("-"*100)