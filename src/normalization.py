"""Chuẩn hóa dữ liệu Netflix thành mô hình dữ liệu phân tích 5 bảng.

Chi tiết thiết kế, quan hệ và quy trình: docs/03_data_normalization.md
"""
from pathlib import Path
import pandas as pd
from config import PROCESSED_DATA_DIR, NORMALIZED_DATA_DIR, START_YEAR, END_YEAR


def create_dim_date(start_year=START_YEAR, end_year=END_YEAR):
    """Tạo bảng dim_date cho toàn bộ phạm vi phân tích."""
    dates = pd.date_range(f"{start_year}-01-01", f"{end_year}-12-31", freq="D")
    return pd.DataFrame({
        "date_key": dates.strftime("%Y%m%d").astype(int),
        "date": dates.strftime("%Y-%m-%d"),
        "year": dates.year,
        "month": dates.month,
        "month_name": dates.month_name(),
        "quarter": dates.quarter,
        "quarter_name": "Q" + dates.quarter.astype(str),
    })


def create_dim_title(df, start_year=START_YEAR, end_year=END_YEAR):
    """Tạo dim_title và chỉ giữ title thuộc phạm vi nghiên cứu."""
    dates = pd.to_datetime(df["date_added"], errors="coerce")
    mask = dates.dt.year.between(start_year, end_year)
    result, dates = df.loc[mask].copy(), dates.loc[mask]
    return pd.DataFrame({
        "show_id": result["show_id"].astype("string"),
        "title": result["title"],
        "type": result["type"],
        "date_added": dates.dt.strftime("%Y-%m-%d"),
        "date_key": pd.to_numeric(dates.dt.strftime("%Y%m%d"), errors="coerce").astype("Int64"),
        "release_year": pd.to_numeric(result["release_year"], errors="coerce").astype("Int64"),
        "rating": result["rating"],
        "duration_minutes": pd.to_numeric(result["duration_minutes"], errors="coerce").astype("Int64"),
        "duration_seasons": pd.to_numeric(result["duration_seasons"], errors="coerce").astype("Int64"),
    }).reset_index(drop=True)


def create_fact_monthly_addition(dim_title, start_year=START_YEAR, end_year=END_YEAR):
    """Tạo bảng số title được thêm theo từng tháng."""
    dates = pd.to_datetime(dim_title["date_added"], errors="coerce").dropna()
    counts = dates.dt.to_period("M").value_counts().sort_index()
    months = pd.period_range(f"{start_year}-01", f"{end_year}-12", freq="M")
    result = counts.reindex(months, fill_value=0).reset_index()
    result.columns = ["month_period", "monthly_additions"]
    result["date_key"] = result["month_period"].dt.strftime("%Y%m01").astype(int)
    result["monthly_additions"] = result["monthly_additions"].astype(int)
    result["month_index"] = range(len(result))
    return result[["date_key", "monthly_additions", "month_index"]]


def create_bridge_genre(df):
    """Tách listed_in thành các cặp show_id - genre."""
    result = df[["show_id", "listed_in"]].copy()
    result["genre"] = result["listed_in"].fillna("").astype(str).str.split(",")
    result = result.explode("genre")
    result["genre"] = result["genre"].str.strip()
    return result.loc[result["genre"].notna() & (result["genre"] != ""), ["show_id", "genre"]].drop_duplicates().reset_index(drop=True)


def create_bridge_country(df):
    """Tách country thành các cặp show_id - country."""
    result = df[["show_id", "country"]].copy()
    result["country"] = result["country"].fillna("").astype(str).str.split(",")
    result = result.explode("country")
    result["country"] = result["country"].str.strip()
    return result.loc[result["country"].notna() & (result["country"] != ""), ["show_id", "country"]].drop_duplicates().reset_index(drop=True)


def normalize_data(df, start_year=START_YEAR, end_year=END_YEAR):
    """Tạo toàn bộ 5 bảng chuẩn hóa."""
    dim_date = create_dim_date(start_year, end_year)
    dim_title = create_dim_title(df, start_year, end_year)
    scoped_df = df[df["show_id"].isin(dim_title["show_id"])]
    return {
        "dim_date": dim_date,
        "dim_title": dim_title,
        "bridge_genre": create_bridge_genre(scoped_df),
        "bridge_country": create_bridge_country(scoped_df),
        "fact_monthly_addition": create_fact_monthly_addition(dim_title, start_year, end_year),
    }


def validate_normalized_data(data):
    """Kiểm tra khóa chính, khóa ngoại và bản ghi trùng."""
    dim_date, dim_title = data["dim_date"], data["dim_title"]
    fact, genre, country = data["fact_monthly_addition"], data["bridge_genre"], data["bridge_country"]
    valid_dates = set(dim_date["date_key"].dropna())
    valid_titles = set(dim_title["show_id"].dropna())
    return {
        "dim_date": {"rows": len(dim_date), "duplicate_date_key": int(dim_date["date_key"].duplicated().sum()), "null_date_key": int(dim_date["date_key"].isna().sum())},
        "dim_title": {"rows": len(dim_title), "duplicate_show_id": int(dim_title["show_id"].duplicated().sum()), "null_show_id": int(dim_title["show_id"].isna().sum()), "orphan_date_key": len(set(dim_title["date_key"].dropna()) - valid_dates)},
        "fact_monthly_addition": {"rows": len(fact), "duplicate_date_key": int(fact["date_key"].duplicated().sum()), "null_date_key": int(fact["date_key"].isna().sum()), "orphan_date_key": len(set(fact["date_key"].dropna()) - valid_dates), "total_additions": int(fact["monthly_additions"].sum())},
        "bridge_genre": {"rows": len(genre), "orphan_show_id": len(set(genre["show_id"].dropna()) - valid_titles), "duplicate_pairs": int(genre.duplicated(["show_id", "genre"]).sum())},
        "bridge_country": {"rows": len(country), "orphan_show_id": len(set(country["show_id"].dropna()) - valid_titles), "duplicate_pairs": int(country.duplicated(["show_id", "country"]).sum())},
    }


def save_normalized_data(data, output_dir=NORMALIZED_DATA_DIR):
    """Lưu 5 bảng chuẩn hóa thành các file CSV."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    for name, df in data.items():
        path = output_path / f"{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"Đã lưu: {path}")


def print_normalization_summary(data, validation):
    """In tóm tắt kích thước bảng và kết quả kiểm tra."""
    print("\n" + "=" * 50 + "\nTỔNG QUAN CHUẨN HÓA\n" + "=" * 50)
    for name, df in data.items():
        print(f"{name:<25} {len(df):>8} dòng ({len(df.columns)} cột)")
    print("\n" + "=" * 50 + "\nKIỂM TRA TÍNH TOÀN VẸN\n" + "=" * 50)
    for table, checks in validation.items():
        print(f"\n[{table}]")
        for name, value in checks.items():
            print(f"  {name:<25}: {value}")


def main():
    """Đọc dữ liệu sạch, chuẩn hóa, kiểm tra và lưu kết quả."""
    input_file = PROCESSED_DATA_DIR / "netflix_titles.csv"
    df = pd.read_csv(input_file)
    print(f"Đã đọc {len(df)} dòng từ {input_file}")
    data = normalize_data(df, START_YEAR, END_YEAR)
    validation = validate_normalized_data(data)
    print_normalization_summary(data, validation)
    save_normalized_data(data)
    print("\nĐã hoàn thành chuẩn hóa dữ liệu.")


if __name__ == "__main__":
    main()
