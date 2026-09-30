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

def clean_date_added(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuyển date_added sang kiểu datetime.

    Các giá trị không hợp lệ sẽ trở thành NaT.
    Không tự suy đoán ngày bị thiếu.
    """
    df = df.copy()
    if ('date_added' not in df.keys()):
        return "data doesn't contain date_added column"
    
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    
    return df

if __name__ == '__main__':
    data = load_all_data()
    for name, df in data.items():
        data[name] = clean_text_columns(df)
        data[name] = clean_date_added(df)
    print(data)