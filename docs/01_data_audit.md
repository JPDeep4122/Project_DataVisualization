# 01. Data Audit

## 1. Mục đích

Data audit được thực hiện trước bước cleaning và normalization nhằm
kiểm tra cấu trúc, khóa, duplicate và quan hệ giữa các bảng dữ liệu.

Các bảng chính hiện tại:

- `netflix_titles`
- `titles`
- `credits`

---

# 2. Duplicate Audit

## 2.1. Kết quả

Kết quả kiểm tra duplicate toàn bộ dòng:

| Dataset | Duplicate rows |
|---|---:|
| `netflix_titles` | 0 |
| `titles` | 0 |
| `credits` | Chưa xem duplicate key là duplicate row |

Cần phân biệt hai khái niệm:

- Duplicate toàn bộ dòng.
- Duplicate giá trị của một cột khóa.

Trong bảng `credits`, cột `id` xuất hiện lặp nhiều lần.
Điều này không được xem là duplicate dữ liệu vì `credits.id` không phải
Primary Key.

---

## 2.2. Ý nghĩa của `credits.id`

Cấu trúc bảng `credits`:

| Column | Meaning |
|---|---|
| `person_id` | ID của người |
| `id` | ID của title |
| `name` | Tên người |
| `character` | Nhân vật |
| `role` | Vai trò |

Một title có thể có nhiều người tham gia.

Ví dụ cùng một `id = tm82169` có thể xuất hiện ở nhiều dòng:

- Sylvester Stallone
- Talia Shire
- Burt Young
- Carl Weathers
- ...

Vì vậy `credits.id` được phép lặp.

---

# 3. Relationship Audit

## 3.1. Quan hệ `titles` - `credits`

Quan hệ được xác định:

`titles.id` → `credits.id`

Trong đó:

- `titles.id` là Primary Key của `titles`.
- `credits.id` là Foreign Key tham chiếu đến `titles.id`.
- Một title có thể có nhiều credit records.

Mô hình:

```text
titles
   id (PK)
      │
      │ 1
      │
      │ N
      ▼
credits
   id (FK)