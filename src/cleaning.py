from pathlib import Path
import pandas as pd
from ingestion import load_netflix_titles

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

def clean_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa duration thành dạng số nguyên, bỏ các hậu tố min và seasons
    Thêm 2 trường duration_minutes và duration_seasons và gắn các giá trị phù hợp 
    theo từng type "Movie" và "TV Show" vào 
    """
    df = df.copy()

    duration_value = df['duration'].astype("string").str.extract(r"(\d+)", expand=False)
    duration_value = pd.to_numeric(duration_value, errors="coerce").astype("Int64")

    df["duration_minutes"] = pd.NA
    df["duration_seasons"] = pd.NA

    movie_mask = df["type"].eq("Movie")
    tv_mask = df["type"].eq("TV Show")

    df.loc[movie_mask, "duration_minutes"] = duration_value[movie_mask]
    df.loc[tv_mask, "duration_seasons"] = duration_value[tv_mask]

    df["duration_minutes"] = df["duration_minutes"].astype("Int64")
    df["duration_seasons"] = df["duration_seasons"].astype("Int64")

    return df

def clean_release_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa release_year về kiểu số nguyên nullable.
    """
    df = df.copy()
    if ('release_year' not in df.keys()):
        return "data doesn't contain release_year column"

    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').astype('Int64')

    return df


def clean_netflix_titles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Làm sạch netflix_titles.csv
    """
    df = df.copy()
    
    df = clean_text_columns(df)
    df = clean_date_added(df)
    df = clean_duration(df)
    df = clean_release_year(df)

    return df


def cleaning_summary(
    before: pd.DataFrame,
    after: pd.DataFrame
) -> pd.DataFrame:
    """Tóm tắt số dòng và số cột trước và sau khi làm sạch."""
    return pd.DataFrame([{
        "rows_before": len(before.index),
        "rows_after": len(after.index),
        "columns_before": len(before.columns),
        "columns_after": len(after.columns),
        "rows_removed": (
            len(before) - len(after)
        )
    }])


def save_cleaned_data(
    cleaned_data: pd.DataFrame | dict[str, pd.DataFrame],
    output_dir: str | Path = "data/processed",
    filename: str = "netflix_titles.csv"
) -> None:
    """Lưu dữ liệu đã làm sạch vào thư mục output_dir."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if isinstance(cleaned_data, pd.DataFrame):
        file_path = output_path / filename
        cleaned_data.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig"
        )
        print(f"Saved: {file_path}")
    elif isinstance(cleaned_data, dict):
        for name, df in cleaned_data.items():
            file_path = (
                output_path /
                f"{name}.csv"
            )

            df.to_csv(
                file_path,
                index=False,
                encoding="utf-8-sig"
            )

            print(f"Saved: {file_path}")


def clean_all_data(data: pd.DataFrame | dict[str, pd.DataFrame]) -> pd.DataFrame | dict[str, pd.DataFrame]:
    """Hàm wrapper tương thích ngược khi chạy pipeline."""
    if isinstance(data, pd.DataFrame):
        return clean_netflix_titles(data)
    return {
        name: clean_netflix_titles(df) if name == "netflix_titles" else clean_text_columns(df)
        for name, df in data.items()
    }


if __name__ == "__main__":

    data = load_netflix_titles()
    cleaned_data = clean_netflix_titles(data)
    summary = cleaning_summary(data, cleaned_data)

    print("\n=== CLEANING SUMMARY ===")
    print(summary.to_string(index=False))

    # Save
    save_cleaned_data(cleaned_data)