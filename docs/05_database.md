# 05. SQLite Database Storage

## 1. Mục đích và vị trí trong Data Pipeline

Giai đoạn **SQLite Database Storage** là điểm đích của nhánh Kỹ thuật dữ liệu (Data Engineering) trong Data Pipeline của dự án. Sau khi dữ liệu đã được làm sạch, chuẩn hóa và kiểm định thành công, toàn bộ 5 bảng dữ liệu từ `data/normalized/` được nạp vào một cơ sở dữ liệu quan hệ duy nhất đặt tại [`database/netflix.db`](file:///D:/UTE/IDVI/Project_DataVisualization/database/netflix.db).

```text
Raw CSV (data/raw/)
  ↓
Ingestion (src/ingestion.py)
  ↓
Data Audit (docs/01_data_audit.md)
  ↓
Data Cleaning (src/cleaning.py)
  ↓
Data Normalization (src/normalization.py)
  ↓
Data Validation (src/validation.py)
  ↓
SQLite Database (src/database.py -> database/netflix.db)  ← BƯỚC HIỆN TẠI
  ├── Phân tích Khám phá (Jupyter Notebook EDA)
  ├── Trực quan hóa Tương tác (Streamlit Dashboard)
  └── Huấn luyện Mô hình Dự báo (Linear Regression Model)
```

### Mục tiêu chính

1. **Thiết lập Single Source of Truth**: Cung cấp một nguồn dữ liệu có cấu trúc, chuẩn hóa và toàn vẹn cho toàn bộ các thành phần ứng dụng của dự án.
2. **Thực thi các ràng buộc quan hệ mức CSDL**: Áp dụng các ràng buộc toàn vẹn thực tế (Primary Key, Foreign Key, Not Null, Unique, Check Constraints) với cơ chế giám sát khóa ngoại (`PRAGMA foreign_keys = ON;`).
3. **Tối ưu hóa hiệu năng truy vấn SQL**: Cho phép ứng dụng Dashboard và Notebook thực hiện các phép kết (JOIN), gom nhóm (GROUP BY), và lọc dữ liệu (WHERE) với tốc độ cao hơn nhiều so với việc đọc trực tiếp từng file CSV.

---

## 2. Lược đồ Cơ sở dữ liệu và DDL (Database Schema)

Module [`src/database.py`](file:///D:/UTE/IDVI/Project_DataVisualization/src/database.py) định nghĩa cấu trúc 5 bảng quan hệ bằng ngôn ngữ DDL chuẩn của SQLite:

### 2.1. Bảng `dim_date` (Chiều thời gian)

```sql
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    date TEXT NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    quarter INTEGER NOT NULL,
    quarter_name TEXT NOT NULL
);
```

- `date_key`: Khóa chính nguyên (`YYYYMMDD`).
- `date`: Định dạng `YYYY-MM-DD`, ràng buộc `UNIQUE` đảm bảo không có hai ngày trùng nhau.

### 2.2. Bảng `dim_title` (Chiều tác phẩm)

```sql
CREATE TABLE dim_title (
    show_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    date_added TEXT NOT NULL,
    date_key INTEGER NOT NULL,
    release_year INTEGER,
    rating TEXT,
    duration_minutes INTEGER,
    duration_seasons INTEGER,

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);
```

- `show_id`: Khóa chính định danh tác phẩm (`s1`, `s2`, ...).
- `date_key`: Khóa ngoại tham chiếu chặt chẽ đến `dim_date(date_key)`.
- `duration_minutes` & `duration_seasons`: Lưu riêng thời lượng phút cho Movie và số mùa cho TV Show.

### 2.3. Bảng `bridge_genre` (Bảng cầu nối thể loại)

```sql
CREATE TABLE bridge_genre (
    show_id TEXT NOT NULL,
    genre TEXT NOT NULL,

    PRIMARY KEY (show_id, genre),

    FOREIGN KEY (show_id)
        REFERENCES dim_title(show_id)
);
```

- Khóa chính kết hợp: `PRIMARY KEY (show_id, genre)` đảm bảo một tựa phim không thể bị gán trùng một thể loại nhiều lần.
- Khóa ngoại: Tham chiếu đến `dim_title(show_id)`.

### 2.4. Bảng `bridge_country` (Bảng cầu nối quốc gia)

```sql
CREATE TABLE bridge_country (
    show_id TEXT NOT NULL,
    country TEXT NOT NULL,
    country_code TEXT,

    PRIMARY KEY (show_id, country),

    FOREIGN KEY (show_id)
        REFERENCES dim_title(show_id)
);
```

- `country_code`: Mã ISO 3166-1 alpha-3 (ví dụ `USA`, `DEU`, `VNM`) phục vụ vẽ biểu đồ bản đồ.
- Khóa chính kết hợp: `PRIMARY KEY (show_id, country)`.
- Khóa ngoại: Tham chiếu đến `dim_title(show_id)`.

### 2.5. Bảng `fact_monthly_addition` (Bảng sự kiện chuỗi thời gian)

```sql
CREATE TABLE fact_monthly_addition (
    date_key INTEGER PRIMARY KEY,
    monthly_additions INTEGER NOT NULL CHECK (monthly_additions >= 0),
    month_index INTEGER NOT NULL UNIQUE,

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);
```

- `date_key`: Ngày đầu tiên của mỗi tháng (`YYYYMM01`), vừa là Khóa chính vừa là Khóa ngoại tham chiếu `dim_date(date_key)`.
- Ràng buộc kiểm tra: `CHECK (monthly_additions >= 0)` ngăn chặn số lượng tác phẩm âm.
- `month_index`: Ràng buộc `UNIQUE` đảm bảo trục thời gian hồi quy luôn duy nhất.

---

## 3. Quản lý thứ tự phụ thuộc (Dependency Management)

Khi làm việc với cơ sở dữ liệu quan hệ có kích hoạt ràng buộc khóa ngoại (`PRAGMA foreign_keys = ON;`), thứ tự thực thi thao tác là yếu tố quyết định sự ổn định của hệ thống:

```text
       ┌───────────┐
       │ dim_date  │ ◄─── Bảng gốc (Độc lập, không có FK)
       └─────┬─────┘
             │
             ├──────────────────────────┐
             ▼                          ▼
       ┌───────────┐             ┌────────────────────────┐
       │ dim_title │             │ fact_monthly_addition  │
       └─────┬─────┘             └────────────────────────┘
             │
             ├──────────────────────────┐
             ▼                          ▼
      ┌──────────────┐           ┌───────────────┐
      │ bridge_genre │           │bridge_country │ ◄─── Bảng lá (Phụ thuộc sâu nhất)
      └──────────────┘           └───────────────┘
```

### 3.1. Thứ tự Xóa bảng (`DROP_ORDER`)
Khi cần làm mới CSDL, các bảng con (chứa khóa ngoại) **phải được xóa trước** các bảng cha (chứa khóa chính được tham chiếu) để tránh lỗi vi phạm ràng buộc:
```python
DROP_ORDER = [
    "fact_monthly_addition",  # Xóa bảng con tham chiếu dim_date
    "bridge_genre",           # Xóa bảng con tham chiếu dim_title
    "bridge_country",         # Xóa bảng con tham chiếu dim_title
    "dim_title",              # Xóa bảng trung gian tham chiếu dim_date
    "dim_date",               # Xóa bảng gốc cuối cùng
]
```

### 3.2. Thứ tự Tạo và Nạp dữ liệu (`LOAD_ORDER`)
Khi nạp dữ liệu, các bảng cha **phải được tạo và nạp dữ liệu trước** để giá trị khóa chính đã sẵn sàng tồn tại khi bảng con tham chiếu tới:
```python
LOAD_ORDER = [
    "dim_date",               # Nạp bảng cha đầu tiên (độc lập)
    "dim_title",              # Nạp bảng kế tiếp (đã có dim_date để tham chiếu)
    "fact_monthly_addition",  # Nạp bảng sự kiện (đã có dim_date)
    "bridge_genre",           # Nạp bảng cầu nối (đã có dim_title)
    "bridge_country",         # Nạp bảng cầu nối (đã có dim_title)
]
```

---

## 4. Đặc tả chi tiết các hàm trong `src/database.py`

### 4.1. `create_database(db_path: str | Path) -> Path`
- Tạo thư mục cha `database/` nếu chưa tồn tại.
- Mở kết nối SQLite và kích hoạt `PRAGMA foreign_keys = ON;`.
- Xóa các bảng cũ theo thứ tự `DROP_ORDER`.
- Tạo mới các bảng rỗng theo thứ tự `LOAD_ORDER` dựa trên từ điển `SCHEMAS`.
- Commit transaction và đóng kết nối.

### 4.2. `load_csv_to_database(db_path: str | Path) -> None`
- Mở kết nối và bật kiểm tra khóa ngoại.
- Lần lượt đọc từng tệp CSV từ `data/normalized/{table_name}.csv`.
- Ghi dữ liệu vào bảng tương ứng thông qua `df.to_sql(table_name, conn, if_exists="append", index=False)`.
- Nếu xảy ra bất kỳ lỗi nào trong quá trình nạp, tự động gọi `conn.rollback()` để đảm bảo tính nguyên tử (*Atomicity*).

### 4.3. `validate_database(db_path: str | Path) -> tuple[dict[str, int], list[tuple[Any, ...]]]`
- Truy vấn đếm số lượng dòng thực tế của từng bảng trong SQLite: `SELECT COUNT(*) FROM {table_name}`.
- Thực thi câu lệnh kiểm tra tính toàn vẹn khóa ngoại mức CSDL:
  ```sql
  PRAGMA foreign_key_check;
  ```
- Trả về từ điển số dòng và danh sách các vi phạm khóa ngoại (nếu có).

### 4.4. `main() -> None`
- Điều phối toàn bộ quy trình: Khởi tạo CSDL $\rightarrow$ Nạp dữ liệu $\rightarrow$ Kiểm định $\rightarrow$ Báo cáo tổng kết.

---

## 5. Kết quả khởi tạo cơ sở dữ liệu thực tế

Khi chạy `src/database.py`, kết quả hiển thị:

```text
============================================================
TẠO SQLITE DATABASE
============================================================
Đã tạo: D:\UTE\IDVI\Project_DataVisualization\database\netflix.db
Đã nạp dữ liệu từ CSV.

SỐ DÒNG:
dim_date                    3653
dim_title                   7294
fact_monthly_addition        120
bridge_genre               16026
bridge_country              8528

FOREIGN KEY CHECK:
PASS - Không có lỗi khóa ngoại.

Database hoàn tất: D:\UTE\IDVI\Project_DataVisualization\database\netflix.db
```

### Đánh giá chất lượng dữ liệu trong SQLite:
- **Tập tin cơ sở dữ liệu**: [`database/netflix.db`](file:///D:/UTE/IDVI/Project_DataVisualization/database/netflix.db) được tạo hoàn chỉnh.
- **Tính toàn vẹn tham chiếu**: Lệnh `PRAGMA foreign_key_check;` trả về danh sách rỗng (`[]`), xác nhận **100% các liên kết khóa ngoại đều hợp lệ**, không có bản ghi nào bị mồ côi.

---

## 6. Các câu lệnh SQL mẫu phục vụ Phân tích & Dashboard

Dưới đây là một số câu lệnh SQL mẫu có thể thực thi trực tiếp trên [`database/netflix.db`](file:///D:/UTE/IDVI/Project_DataVisualization/database/netflix.db):

### 6.1. Xu hướng bổ sung nội dung theo năm và tháng (Dashboard Trend Chart)

```sql
SELECT 
    d.year,
    d.month,
    d.month_name,
    f.monthly_additions,
    f.month_index
FROM fact_monthly_addition f
JOIN dim_date d ON f.date_key = d.date_key
ORDER BY f.month_index ASC;
```

### 6.2. Top 10 Thể loại phổ biến nhất trên Netflix

```sql
SELECT 
    g.genre,
    COUNT(t.show_id) AS total_titles,
    ROUND(COUNT(t.show_id) * 100.0 / (SELECT COUNT(*) FROM dim_title), 2) AS percentage
FROM bridge_genre g
JOIN dim_title t ON g.show_id = t.show_id
GROUP BY g.genre
ORDER BY total_titles DESC
LIMIT 10;
```

### 6.3. Phân bố tác phẩm theo Quốc gia phục vụ Bản đồ thế giới (Choropleth Map)

```sql
SELECT 
    c.country_code,
    c.country,
    COUNT(DISTINCT t.show_id) AS title_count
FROM bridge_country c
JOIN dim_title t ON c.show_id = t.show_id
WHERE c.country_code IS NOT NULL
GROUP BY c.country_code, c.country
ORDER BY title_count DESC;
```

### 6.4. Tỷ lệ cơ cấu Movie vs TV Show theo từng năm thêm

```sql
SELECT 
    d.year,
    SUM(CASE WHEN t.type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN t.type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count,
    COUNT(t.show_id) AS total_count
FROM dim_title t
JOIN dim_date d ON t.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year ASC;
```

---

## 7. Hướng dẫn chạy và tái lập

Thực thi module lưu trữ CSDL từ dòng lệnh:

```powershell
.venv\Scripts\python.exe src/database.py
```

Tệp cơ sở dữ liệu sẽ được tạo mới và cập nhật toàn bộ tại:
- `database/netflix.db`
