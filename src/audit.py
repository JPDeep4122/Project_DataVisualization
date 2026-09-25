from config import RAW_DATA_DIR
import pandas as pd

from ingestion import load_all_data
from pprint import pprint

def audit_missing(data: dict[str, pd.DataFrame]):
    result = {}

    for name, df in data.items():
        result[name] = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict()
        }

    return result





if __name__ == "__main__":
    for data, descript in audit_missing(load_all_data()).items():
        print(data)
        pprint(descript)
        print("-"*100)