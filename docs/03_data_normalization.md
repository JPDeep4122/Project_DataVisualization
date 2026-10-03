# 03. Data Normalization

## 1. Mục đích và vị trí trong Data Pipeline

Sau **Data Audit** và **Data Cleaning**, bước **Data Normalization** chuyển
`netflix_titles.csv` đã làm sạch thành mô hình dữ liệu phục vụ phân tích,
dashboard và forecasting.

```text
Raw CSV
  ↓
Ingestion
  ↓
Data Audit
  ↓
Data Cleaning
  ↓
Data Normalization  ← bước hiện tại
  ↓
Validation / SQLite
  ├── EDA
  ├── Dashboard
  └── Forecasting
```

### Mục tiêu

1. Tách các thuộc tính đa trị `listed_in` và `country` thành bảng cầu nối.
2. Tạo `dim_date` để phân tích theo ngày, tháng, quý và năm.
3. Tạo `fact_monthly_addition` để phân tích xu hướng và forecasting.
4. Kiểm tra PK/FK, orphan key và bản ghi trùng.
5. Lưu kết quả thành CSV trong `data/normalized/`.

---

## 2. Mô hình dữ liệu

Mô hình sử dụng **Extended Star / Snowflake Schema** kết hợp các bảng cầu nối
cho quan hệ nhiều-nhiều.

```text
                         ┌─────────────────┐
                         │    dim_date     │
                         ├─────────────────┤
                         │ PK date_key     │
                         │ date            │
                         │ year            │
                         │ month           │
                         │ month_name      │
                         │ quarter         │
                         │ quarter_name    │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ┌─────────────────┐       ┌────────────────────────┐
          │    dim_title    │       │ fact_monthly_addition  │
          ├─────────────────┤       ├────────────────────────┤
          │ PK show_id      │       │ PK/FK date_key         │
          │ title           │       │ monthly_additions      │
          │ type            │       │ month_index            │
          │ date_added      │       └────────────────────────┘
          │ FK date_key     │
          │ release_year    │
          │ rating          │
          │ duration_*      │
          └────────┬────────┘
                   │
             ┌─────┴─────┐
             ▼           ▼
      ┌──────────────┐ ┌───────────────┐
      │bridge_genre  │ │bridge_country │
      ├──────────────┤ ├───────────────┤
      │FK show_id    │ │FK show_id     │
      │genre         │ │country        │
      └──────────────┘ └───────────────┘
```

### Quan hệ

| Quan hệ | Ý nghĩa |
|---|---|
| `dim_date.date_key` → `dim_title.date_key` | Một ngày có thể có nhiều title được thêm |
| `dim_date.date_key` → `fact_monthly_addition.date_key` | Mỗi tháng dùng ngày đầu tháng làm khóa |
| `dim_title.show_id` → `bridge_genre.show_id` | Một title có thể có nhiều genre |
| `dim_title.show_id` → `bridge_country.show_id` | Một title có thể có nhiều country |

---

## 3. Đặc tả các bảng

### 3.1. `dim_date`

**Mục đích:** cung cấp chiều thời gian cho phân tích.

**Phạm vi:** `2011-01-01` đến `2020-12-31`.

| Cột | Vai trò | Mô tả |
|---|---|---|
| `date_key` | PK | Khóa ngày dạng `YYYYMMDD` |
| `date` | — | Ngày dạng `YYYY-MM-DD` |
| `year` | — | Năm |
| `month` | — | Tháng 1–12 |
| `month_name` | — | Tên tháng |
| `quarter` | — | Quý 1–4 |
| `quarter_name` | — | Q1–Q4 |

---

### 3.2. `dim_title`

**Mục đích:** lưu thông tin mô tả của Movie/TV Show trong phạm vi nghiên cứu
2011–2020.

| Cột | Vai trò | Mô tả |
|---|---|---|
| `show_id` | PK | Mã title duy nhất |
| `title` | — | Tên phim/chương trình |
| `type` | — | `Movie` hoặc `TV Show` |
| `date_added` | — | Ngày Netflix thêm title |
| `date_key` | FK | → `dim_date.date_key` |
| `release_year` | — | Năm phát hành |
| `rating` | — | Phân loại độ tuổi |
| `duration_minutes` | — | Thời lượng Movie |
| `duration_seasons` | — | Số mùa của TV Show |

> `release_year` là năm tác phẩm phát hành; `date_added` là ngày Netflix đưa
tác phẩm vào danh mục. Hai trường này được giữ riêng để tránh nhầm lẫn.

---

### 3.3. `fact_monthly_addition`

**Mục đích:** lưu số title được Netflix thêm trong từng tháng.

| Cột | Vai trò | Mô tả |
|---|---|---|
| `date_key` | PK/FK | Ngày đầu tháng, dạng `YYYYMM01` |
| `monthly_additions` | Measure | Số title được thêm trong tháng |
| `month_index` | — | Chỉ số tháng liên tục từ 0 |

Bảng có **120 dòng**, tương ứng 120 tháng từ `01/2011` đến `12/2020`.
Các tháng không có title mới vẫn được giữ với `monthly_additions = 0`.

`month_index` được sử dụng làm biến thời gian cho mô hình Linear Regression.

---

### 3.4. `bridge_genre`

**Mục đích:** chuẩn hóa thuộc tính đa trị `listed_in`.

Ví dụ:

```text
s1 | Drama, Comedy
```

thành:

```text
s1 | Drama
s1 | Comedy
```

| Cột | Vai trò | Mô tả |
|---|---|---|
| `show_id` | FK | → `dim_title.show_id` |
| `genre` | Thành phần PK | Thể loại |

Khóa chính logic: **(`show_id`, `genre`)**.

---

### 3.5. `bridge_country`

**Mục đích:** chuẩn hóa thuộc tính đa trị `country`.

Ví dụ:

```text
s1 | United States, Canada
```

thành:

```text
s1 | United States
s1 | Canada
```

| Cột | Vai trò | Mô tả |
|---|---|---|
| `show_id` | FK | → `dim_title.show_id` |
| `country` | Thành phần PK | Quốc gia |

Khóa chính logic: **(`show_id`, `country`)**.

---

## 4. Quy trình triển khai

Module xử lý nằm tại:

```text
src/normalization.py
```

Input:

```text
data/processed/netflix_titles.csv
```

Output:

```text
data/normalized/
├── dim_date.csv
├── dim_title.csv
├── bridge_genre.csv
├── bridge_country.csv
└── fact_monthly_addition.csv
```

### Các hàm chính

| Hàm | Nhiệm vụ |
|---|---|
| `create_dim_date()` | Tạo chiều thời gian 2011–2020 |
| `create_dim_title()` | Tạo chiều title và áp dụng phạm vi nghiên cứu |
| `create_bridge_genre()` | Tách `listed_in` thành từng genre |
| `create_bridge_country()` | Tách `country` thành từng country |
| `create_fact_monthly_addition()` | Tổng hợp số title theo tháng |
| `normalize_data()` | Điều phối việc tạo 5 bảng |
| `validate_normalized_data()` | Kiểm tra tính toàn vẹn |
| `save_normalized_data()` | Lưu các bảng thành CSV |

### Quy tắc xử lý

- Chỉ đưa title có `date_added` từ **2011–2020** vào mô hình phân tích.
- `dim_date` chứa toàn bộ ngày từ `2011-01-01` đến `2020-12-31`.
- `fact_monthly_addition` luôn có đủ **120 tháng**.
- Tháng không có title mới được gán `0`.
- `listed_in` và `country` được tách bằng `split` + `explode`.
- Loại bỏ khoảng trắng thừa và các cặp trùng.
- Các bảng bridge chỉ chứa `show_id` tồn tại trong `dim_title`.
- `titles.csv` và `credits.csv` không được ép vào mô hình này vì sử dụng
  hệ thống ID khác với `netflix_titles.csv`.

---

## 5. Kiểm tra tính toàn vẹn

`validate_normalized_data()` kiểm tra:

- Trùng khóa chính.
- Khóa chính bị NULL.
- Orphan `date_key`.
- Orphan `show_id`.
- Trùng cặp `(show_id, genre)`.
- Trùng cặp `(show_id, country)`.
- Tổng số title trong bảng fact.

Kết quả mong đợi:

```text
dim_date
    duplicate_date_key = 0
    null_date_key = 0

dim_title
    duplicate_show_id = 0
    null_show_id = 0
    orphan_date_key = 0

fact_monthly_addition
    rows = 120
    duplicate_date_key = 0
    null_date_key = 0
    orphan_date_key = 0

bridge_genre
    orphan_show_id = 0
    duplicate_pairs = 0

bridge_country
    orphan_show_id = 0
    duplicate_pairs = 0
```

---

## 6. Các quyết định thiết kế

### 6.1. Vì sao không chuẩn hóa toàn bộ thành 3NF?

Project tập trung vào **phân tích và trực quan hóa dữ liệu**, không phải xây dựng
hệ thống OLTP. Nhóm chuẩn hóa ở mức phù hợp với mục tiêu: xử lý thuộc tính đa trị,
tách chiều thời gian, tách dữ liệu mô tả và dữ liệu đo lường, đồng thời giữ các
bảng thuận tiện cho JOIN, EDA, dashboard và forecasting.

Không áp dụng 3NF một cách máy móc cho toàn bộ dataset.

### 6.2. Vì sao `fact_monthly_addition` là bảng riêng?

Đây là bảng dữ liệu dẫn xuất từ `dim_title`, chứa metric `monthly_additions`.
Nó giúp xây dựng biểu đồ xu hướng, tạo chuỗi thời gian liên tục và cung cấp trực
tiếp biến đầu vào cho Linear Regression.

### 6.3. Vì sao `duration` được tách thành hai cột?

```text
duration_minutes   → Movie
 duration_seasons   → TV Show
```

Hai cột giữ riêng hai đơn vị đo khác nhau, giúp phân tích rõ ràng hơn.

---

## 7. Hướng dẫn chạy

Từ thư mục gốc project:

```powershell
.venv\Scripts\python.exe src/normalization.py
```

Sau khi chạy, kiểm tra:

```text
data/normalized/
├── dim_date.csv
├── dim_title.csv
├── bridge_genre.csv
├── bridge_country.csv
└── fact_monthly_addition.csv
```

Dữ liệu chuẩn hóa được dùng cho EDA, Interactive Dashboard, Linear Regression /
Forecasting và SQLite Database.
