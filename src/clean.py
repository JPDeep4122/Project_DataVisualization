import pandas as pd
from ingestion import load_all_data

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa các cột dạng text:
    - Loại bỏ khoảng trắng đầu/cuối
    - Chuyển chuỗi rỗng thành NaN
    """

    df = df.copy()
    text_columns = df.select_dtypes(include='str').columns

    for column in text_columns:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace('', pd.NA)

    return df


if __name__ == '__main__':
    data = load_all_data()
    for name, df in data.items():
        data[name] = clean_text_columns(df)
    print(data)