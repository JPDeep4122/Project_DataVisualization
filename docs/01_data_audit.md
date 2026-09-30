# 01. Data Audit

## 1. Mục đích

Data Audit được thực hiện trước bước Cleaning và Normalization nhằm đánh giá
chất lượng, cấu trúc và khả năng sử dụng của các bộ dữ liệu đầu vào.

Các mục tiêu chính:

- Kiểm tra cấu trúc của các bảng dữ liệu.
- Kiểm tra duplicate toàn bộ dòng.
- Kiểm tra các khóa chính.
- Kiểm tra quan hệ giữa `titles` và `credits`.
- Phát hiện các cột chứa nhiều giá trị trong cùng một ô.
- Kiểm tra chất lượng dữ liệu ngày tháng.
- Kiểm tra phạm vi dữ liệu phục vụ đề tài.

Các dataset hiện tại:

- `netflix_titles`
- `titles`
- `credits`

---

# 2. Dataset Overview

## 2.1. `netflix_titles`

| Thuộc tính | Giá trị |
|---|---:|
| Rows | 8,807 |
| Columns | 12 |
| Primary Key dự kiến | `show_id` |
| Duplicate rows | 0 |
| Duplicate key | 0 |
| Null `show_id` | 0 |

Các cột:

```text
show_id
type
title
director
cast
country
date_added
release_year
rating
duration
listed_in
description
```

Bảng `netflix_titles` chứa thông tin metadata chính của nội dung
Netflix và là nguồn dữ liệu chính cho phần phân tích xu hướng của đề tài.

---

## 2.2. `titles`

| Thuộc tính | Giá trị |
|---|---:|
| Rows | 6,137 |
| Columns | 15 |
| Primary Key dự kiến | `id` |
| Duplicate rows | 0 |
| Duplicate key | 0 |
| Null `id` | 0 |

Các cột:

```text
id
title
type
description
release_year
age_certification
runtime
genres
production_countries
seasons
imdb_id
imdb_score
imdb_votes
tmdb_popularity
tmdb_score
```

Bảng `titles` cung cấp metadata bổ sung và các thông tin liên quan đến
IMDb/TMDB.

Dataset này được sử dụng như nguồn dữ liệu bổ sung, không thay thế
`netflix_titles` vì hai dataset sử dụng hệ thống ID khác nhau.

---

## 2.3. `credits`

| Thuộc tính | Giá trị |
|---|---:|
| Rows | 81,355 |
| Columns | 5 |
| ID duy nhất | 5,788 |
| `id` | Khóa tham chiếu đến `titles.id` |

Các cột:

```text
person_id
id
name
character
role
```

Bảng `credits` chứa thông tin về những người tham gia vào một title.

Một title có thể có nhiều dòng trong `credits`, do đó `credits.id`
không phải Primary Key.

---

# 3. Structure Audit

## 3.1. Kết quả

| Dataset | Rows | Columns |
|---|---:|---:|
| `netflix_titles` | 8,807 | 12 |
| `titles` | 6,137 | 15 |
| `credits` | 81,355 | 5 |

Không phát hiện bất thường về cấu trúc cơ bản của ba dataset.

Các cột có kiểu dữ liệu phù hợp với dữ liệu hiện tại:

- ID được lưu dưới dạng string.
- Các trường văn bản được lưu dưới dạng string.
- `release_year` được lưu dưới dạng integer.
- Các trường điểm số IMDb/TMDB được lưu dưới dạng float.
- `date_added` hiện đang được đọc dưới dạng string và cần được xử lý
  trong bước Cleaning.

---

# 4. Duplicate Audit

## 4.1. Duplicate toàn bộ dòng

Kết quả:

| Dataset | Duplicate rows |
|---|---:|
| `netflix_titles` | 0 |
| `titles` | 0 |
| `credits` | 0 |

Không phát hiện dòng dữ liệu trùng hoàn toàn trong cả ba dataset.

---

## 4.2. Phân biệt duplicate row và duplicate key

Cần phân biệt:

1. Duplicate toàn bộ dòng.
2. Duplicate giá trị của một cột khóa.

Đối với `credits`, `id` xuất hiện nhiều lần.

Điều này không phải duplicate dữ liệu vì `credits.id` không phải Primary Key.

Ví dụ một title có thể có nhiều credit:

```text
titles
tm82169
   │
   ├── Sylvester Stallone
   ├── Talia Shire
   ├── Burt Young
   ├── Carl Weathers
   └── ...
```

Do đó cùng một `credits.id` có thể xuất hiện trên nhiều dòng.

---

## 4.3. Kết luận Duplicate Audit

Kết quả audit cho phép xác định:

- Không có duplicate toàn bộ dòng trong ba dataset.
- `netflix_titles.show_id` không bị duplicate.
- `titles.id` không bị duplicate.
- `credits.id` được phép lặp vì đóng vai trò khóa tham chiếu đến `titles.id`.

Không nên xóa các dòng `credits` chỉ vì `credits.id` xuất hiện nhiều lần.

---

# 5. Key Audit

## 5.1. `netflix_titles.show_id`

Kết quả:

```text
Rows:          8,807
Unique IDs:    8,807
Null IDs:      0
Duplicate IDs: 0
```

Do đó `netflix_titles.show_id` đủ điều kiện làm Primary Key cho bảng
dữ liệu được chuẩn hóa từ `netflix_titles`.

---

## 5.2. `titles.id`

Kết quả:

```text
Rows:          6,137
Unique IDs:    6,137
Null IDs:      0
Duplicate IDs: 0
```

Do đó `titles.id` đủ điều kiện làm Primary Key của bảng `titles`.

---

# 6. Relationship Audit

## 6.1. Quan hệ `titles` - `credits`

Quan hệ được xác định:

```text
titles.id
    │
    │ 1
    │
    │ N
    ▼
credits.id
```

Trong đó:

- `titles.id` là khóa chính của `titles`.
- `credits.id` là khóa tham chiếu đến `titles.id`.
- Một title có thể có nhiều credit records.

---

## 6.2. Kết quả

| Thuộc tính | Giá trị |
|---|---:|
| `titles` rows | 6,137 |
| `credits` rows | 81,355 |
| Unique `titles.id` | 6,137 |
| Unique `credits.id` | 5,788 |
| Orphan `credits.id` | 0 |
| Title không có credit | 349 |
| Referential integrity | `True` |

---

## 6.3. Referential Integrity

Nhóm kiểm tra:

```python
credits_ids.issubset(titles_ids)
```

Kết quả:

```text
True
```

Điều này cho thấy toàn bộ các giá trị `credits.id` đều tồn tại trong
tập khóa `titles.id`.

Do đó không phát hiện orphan key ở phía `credits`.

---

## 6.4. Title không có Credit

Có:

```text
6,137 titles
5,788 titles xuất hiện trong credits
```

Do đó:

```text
6,137 - 5,788 = 349
```

Có 349 title trong `titles` không xuất hiện trong `credits`.

Đây được ghi nhận là vấn đề về độ bao phủ của dataset `credits`,
không mặc định xem là lỗi dữ liệu.

Các title này vẫn có thể sử dụng cho những phân tích dựa trên metadata
của bảng `titles`.

---

# 7. Multivalue Audit

Audit phát hiện hai cột trong `netflix_titles` chứa nhiều giá trị trong
cùng một cell:

- `country`
- `listed_in`

## 7.1. `country`

| Thuộc tính | Giá trị |
|---|---:|
| Non-null rows | 7,976 |
| Single-value rows | 6,656 |
| Multivalue rows | 1,320 |
| Average values/row | ~1.256 |
| Maximum values/row | 12 |

Có 1,320 dòng chứa nhiều quốc gia trong cùng một cell.

---

## 7.2. `listed_in`

| Thuộc tính | Giá trị |
|---|---:|
| Non-null rows | 8,807 |
| Single-value rows | 2,020 |
| Multivalue rows | 6,787 |
| Average values/row | ~2.194 |
| Maximum values/row | 3 |

Có 6,787 dòng chứa nhiều thể loại trong cùng một cell.

Điều này cho thấy `listed_in` là một thuộc tính multi-valued rõ ràng.

---

## 7.3. Quyết định thiết kế dữ liệu

Không nên giữ nguyên toàn bộ danh sách thể loại hoặc quốc gia trong một
cell khi xây dựng mô hình dữ liệu phục vụ phân tích.

Dữ liệu sẽ được chuẩn hóa thành các bảng bridge:

```text
dim_title
    │
    ├─────────── bridge_genre
    │
    └─────────── bridge_country
```

### `bridge_genre`

```text
show_id | genre
```

### `bridge_country`

```text
show_id | country
```

Cách tổ chức này giúp:

- Lọc theo genre.
- Lọc theo country.
- JOIN dữ liệu.
- Phân tích số lượng title theo genre/country.
- Hạn chế việc lưu nhiều giá trị trong một cell.

---

# 8. Date Audit

Cột ngày chính của project:

```text
netflix_titles.date_added
```

Hiện tại cột này có kiểu `str` và sẽ được chuyển đổi sang kiểu datetime
trong bước Cleaning.

## 8.1. Kết quả

| Thuộc tính | Giá trị |
|---|---:|
| Original dtype | `str` |
| Null values | 10 |
| Invalid/unparseable values | 88 |
| Total rows without valid date | 98 |
| Minimum valid date | 2008-01-01 |
| Maximum valid date | 2021-09-25 |

Trong quá trình audit:

- 10 dòng có giá trị `date_added` bị thiếu.
- 88 dòng không chuyển đổi được thành ngày hợp lệ theo quy tắc parse hiện tại.
- Tổng cộng có 98 dòng không có ngày hợp lệ.

Các giá trị ngày hợp lệ nằm trong khoảng:

```text
2008-01-01 → 2021-09-25
```

## 8.2. Xử lý ở bước Cleaning

Audit không tự động sửa dữ liệu.

Trong bước Cleaning cần:

1. Chuyển `date_added` sang datetime.
2. Xác định nguyên nhân của 88 giá trị không parse được.
3. Xử lý 10 giá trị missing.
4. Không tự ý suy đoán ngày nếu dataset không cung cấp đủ thông tin.

Các dòng không có ngày hợp lệ sẽ được xem xét riêng khi xác định phạm vi
phân tích.

---

# 9. Scope Audit

## 9.1. Phạm vi nghiên cứu

Đề tài sử dụng `date_added` làm mốc thời gian chính.

Phạm vi nghiên cứu:

```text
2011 <= year(date_added) <= 2020
```

Lý do sử dụng `date_added` thay vì `release_year`:

- `release_year` biểu thị năm phát hành nội dung.
- `date_added` biểu thị thời điểm nội dung được thêm vào Netflix.
- Đề tài tập trung vào xu hướng nội dung được Netflix thêm vào trong
  giai đoạn nghiên cứu.

## 9.2. Kết quả Scope Audit

| Phân loại | Số dòng |
|---|---:|
| Tổng số dòng | 8,807 |
| Trong phạm vi 2011–2020 | 7,206 |
| Ngoài phạm vi | 1,503 |
| Thiếu ngày | 98 |

Tỷ lệ các dòng nằm trong phạm vi 2011–2020 trên tổng dataset:

```text
81.82%
```

## 9.3. Các năm ngoài phạm vi

Các năm xuất hiện ngoài phạm vi nghiên cứu:

```text
2008
2009
2010
2021
```

Các dòng thuộc các năm này sẽ không được đưa vào tập dữ liệu chính của
phần phân tích xu hướng 2011–2020.

## 9.4. Lưu ý về missing/invalid date

Có 98 dòng không có ngày hợp lệ.

Các dòng này được phân loại riêng là:

```text
missing/invalid date
```

Missing/invalid date không đồng nghĩa với out-of-scope.

---

# 10. Tổng hợp kết quả Audit

| Audit | Kết quả chính | Quyết định |
|---|---|---|
| Structure | 3 dataset có cấu trúc hợp lệ | Tiếp tục Cleaning |
| Duplicate | 0 duplicate toàn bộ dòng | Không cần loại duplicate toàn dòng |
| Key | `show_id` và `titles.id` unique, non-null | Có thể sử dụng làm PK |
| Relationship | `titles.id → credits.id` hợp lệ | Có thể sử dụng quan hệ 1-N |
| Multivalue | `country`, `listed_in` chứa nhiều giá trị | Tách thành bridge tables |
| Date | 98 dòng thiếu/không parse được ngày | Xử lý trong Cleaning |
| Scope | 7,206 dòng thuộc 2011–2020 | Sử dụng làm scope chính |

---

# 11. Các quyết định thiết kế sau Audit

## 11.1. Primary Key

Sử dụng `netflix_titles.show_id` làm khóa chính cho `dim_title`.

Đối với dataset `titles`, `titles.id` được sử dụng làm khóa chính.

## 11.2. Relationship

Giữ quan hệ:

```text
titles.id
    1
    │
    N
credits.id
```

Không xem các giá trị lặp của `credits.id` là duplicate cần xóa.

## 11.3. Genre

Tách `netflix_titles.listed_in` thành `bridge_genre`:

```text
show_id | genre
```

## 11.4. Country

Tách `netflix_titles.country` thành `bridge_country`:

```text
show_id | country
```

## 11.5. Date

Chuyển `date_added` từ string sang datetime trong bước Cleaning.

Các giá trị missing/invalid cần được xử lý trước khi tạo:

```text
added_year
added_month
added_quarter
```

## 11.6. Scope

Tập dữ liệu chính của đề tài được xác định bằng:

```text
2011–2020
```

theo `year(date_added)`.

Tập phân tích chính hiện có:

```text
7,206 titles
```

---

# 12. Data Pipeline sau Audit

```text
Raw CSV
   │
   ▼
Ingestion
   │
   ▼
Data Audit
   │
   ├── Structure
   ├── Duplicate
   ├── Key
   ├── Relationship
   ├── Multivalue
   ├── Date
   └── Scope
   │
   ▼
Cleaning
   │
   ├── Xử lý missing/invalid date
   ├── Chuẩn hóa date
   └── Chuẩn hóa dữ liệu text
   │
   ▼
Normalization
   │
   ├── dim_title
   ├── bridge_genre
   └── bridge_country
   │
   ▼
Validation
   │
   ▼
SQLite
   │
   ├── EDA
   ├── Dashboard
   └── Forecast
```

---

# 13. Những nội dung chưa kết luận từ Audit hiện tại

Data Audit hiện tại chưa đưa ra kết luận cuối cùng về:

- Cách xử lý missing values ở từng cột.
- Phân phối `rating`.
- Phân phối `type`.
- Phân phối `release_year`.
- Giá trị bất thường của các trường số.
- Chất lượng `director` và `cast`.
- Giá trị và phân phối của IMDb/TMDB.
- Chi tiết dữ liệu sau khi normalize.
- Chất lượng dữ liệu sau Cleaning.

Các nội dung trên sẽ được thực hiện ở các bước Cleaning, EDA và
Validation tiếp theo.

---

# 14. Kết luận

Data Audit cho thấy dữ liệu có thể tiếp tục được sử dụng cho các bước
Cleaning và Normalization.

Các kết quả quan trọng nhất:

1. `netflix_titles` có 8,807 dòng và không có duplicate toàn bộ dòng.
2. `titles` có 6,137 dòng và không có duplicate toàn bộ dòng.
3. `credits` có 81,355 dòng và không có duplicate toàn bộ dòng.
4. `netflix_titles.show_id` và `titles.id` đều unique và non-null.
5. `credits.id` là khóa tham chiếu đến `titles.id`, không phải Primary Key.
6. Quan hệ `titles` - `credits` có dạng one-to-many.
7. Không phát hiện orphan key trong `credits`.
8. Có 349 title trong `titles` không có credit tương ứng.
9. `listed_in` và `country` là các trường multi-valued cần được normalize.
10. `date_added` có 10 giá trị missing và 88 giá trị không parse được.
11. Có 7,206 dòng thuộc phạm vi nghiên cứu 2011–2020.
12. Các dòng có `date_added` ngoài phạm vi gồm các năm 2008, 2009, 2010 và 2021.
13. Các giá trị missing/invalid date được phân loại riêng và không được
    đánh đồng với dữ liệu out-of-scope.

Kết quả này là cơ sở để chuyển sang bước:

```text
Cleaning → Normalization → Validation
```
