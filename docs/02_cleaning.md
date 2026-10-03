# 02. Data Cleaning

## 1. Mục đích và vị trí trong Data Pipeline

Sau khi giai đoạn **Data Audit** ([`docs/01_data_audit.md`](file:///D:/UTE/IDVI/Project_DataVisualization/docs/01_data_audit.md)) phát hiện các vấn đề về chất lượng dữ liệu thô (chuỗi rỗng, khoảng trắng thừa, định dạng ngày tháng chưa chuẩn, trường thời lượng lẫn lộn giữa phút và số mùa), giai đoạn **Data Cleaning** có nhiệm vụ chuẩn hóa và xử lý các lỗi kỹ thuật này.

```text
Raw CSV (data/raw/)
  ↓
Ingestion (src/ingestion.py)
  ↓
Data Audit (docs/01_data_audit.md)
  ↓
Data Cleaning (src/cleaning.py -> data/processed/)  ← BƯỚC HIỆN TẠI
  ↓
Data Normalization (src/normalization.py -> data/normalized/)
  ↓
Validation (src/validation.py)
  ↓
SQLite Database (src/database.py -> database/netflix.db)
```

### Mục tiêu chính

1. **Chuẩn hóa chuỗi văn bản**: Loại bỏ khoảng trắng đầu/cuối và quy chuẩn chuỗi rỗng `""` về giá trị khuyết thiếu chuẩn của Pandas (`pd.NA`).
2. **Chuẩn hóa ngày tháng (`date_added`)**: Chuyển đổi chuỗi văn bản ngày tháng tự do sang định dạng chuẩn `datetime`, chuyển các giá trị không hợp lệ về `NaT`, không tự tiện suy đoán dữ liệu thiếu.
3. **Phân rã trường thời lượng (`duration`)**: Tách số và đơn vị trong cột `duration`, phân tách rõ ràng thành hai cột số nguyên độc lập: `duration_minutes` (phim lẻ) và `duration_seasons` (phim bộ).
4. **Chuẩn hóa năm phát hành (`release_year`)**: Chuyển đổi về kiểu số nguyên có thể chứa giá trị rỗng (`Int64`).
5. **Bảo toàn dữ liệu nguồn**: Áp dụng nguyên tắc không xóa dòng ở bước cleaning, lưu trữ các bảng sạch độc lập vào thư mục `data/processed/`.

---

## 2. Các vấn đề dữ liệu được giải quyết

Dựa trên kết quả kiểm toán dữ liệu từ bước Audit, module cleaning giải quyết các vấn đề cụ thể sau:

| Thuộc tính | Hiện trạng dữ liệu thô | Giải pháp xử lý | Kết quả sau Cleaning |
|---|---|---|---|
| **Text columns** | Tồn tại khoảng trắng đầu/cuối; ô trống lưu dưới dạng chuỗi rỗng `""`. | `.str.strip()` và thay thế `""` bằng `pd.NA`. | Chuỗi sạch, phân biệt rõ giữa chuỗi hợp lệ và giá trị thiếu. |
| **`date_added`** | Kiểu chuỗi văn bản tự do (ví dụ: `"September 25, 2021"`), có 10 dòng bị thiếu và 88 dòng lỗi định dạng. | Chuyển đổi bằng `pd.to_datetime(errors="coerce")`. | Kiểu `datetime64[ns]`, giá trị lỗi trở thành `NaT`. |
| **`duration`** | Lưu chung cả phút và số mùa (ví dụ: `"90 min"`, `"2 Seasons"`). | Dùng Regex trích xuất phần số, dựa vào cột `type` để phân bổ vào `duration_minutes` hoặc `duration_seasons`. | Hai cột số nguyên `Int64` độc lập, thuận tiện cho tính toán thống kê. |
| **`release_year`** | Được đọc dưới dạng số nguyên thường hoặc chuỗi. | Ép kiểu an toàn bằng `pd.to_numeric(errors="coerce").astype("Int64")`. | Kiểu `Int64` nullable. |

---

## 3. Đặc tả chi tiết các hàm trong `src/cleaning.py`

Module [`src/cleaning.py`](file:///D:/UTE/IDVI/Project_DataVisualization/src/cleaning.py) được xây dựng theo kiến trúc hàm mô-đun hóa, mỗi hàm đảm nhận một nhiệm vụ làm sạch chuyên biệt:

### 3.1. `clean_text_columns(df: pd.DataFrame) -> pd.DataFrame`

- **Mục đích**: Chuẩn hóa toàn bộ các cột kiểu văn bản trong DataFrame.
- **Cách thức hoạt động**:
  - Tự động phát hiện các cột kiểu chuỗi ký tự bằng `df.select_dtypes(include='str').columns`.
  - Cắt bỏ khoảng trắng thừa ở hai đầu bằng `.str.strip()`.
  - Thay thế toàn bộ chuỗi rỗng `""` thành `pd.NA` nhằm thống nhất định dạng giá trị khuyết thiếu.
- **Đầu ra**: Bản sao DataFrame với các cột text đã được làm sạch.

### 3.2. `clean_date_added(df: pd.DataFrame) -> pd.DataFrame`

- **Mục đích**: Chuyển đổi cột `date_added` từ văn bản sang đối tượng thời gian chuẩn.
- **Cách thức hoạt động**:
  - Kiểm tra sự tồn tại của cột `date_added`.
  - Dùng `pd.to_datetime(df['date_added'], errors='coerce')` để tự động nhận dạng định dạng ngày tháng tiếng Anh chuẩn.
  - Các ô có định dạng không hợp lệ hoặc chuỗi rỗng sẽ tự động chuyển thành `NaT` (Not a Time), không tự ý suy đoán ngày tháng.

### 3.3. `clean_duration(df: pd.DataFrame) -> pd.DataFrame`

- **Mục đích**: Xử lý hiện tượng "một cột chứa hai thang đo khác nhau" của trường `duration`.
- **Cách thức hoạt động**:
  - Dùng biểu thức chính quy `r"(\d+)"` để bóc tách giá trị số nguyên từ chuỗi (ví dụ: `"90 min"` $\rightarrow$ `90`, `"2 Seasons"` $\rightarrow$ `2`).
  - Khởi tạo hai cột mới `duration_minutes` và `duration_seasons` với giá trị mặc định là `pd.NA`.
  - Dựa trên giá trị của cột `type`:
    - Nếu `type == "Movie"`: Gán giá trị số vào cột `duration_minutes`.
    - Nếu `type == "TV Show"`: Gán giá trị số vào cột `duration_seasons`.
  - Chuyển đổi cả hai cột về kiểu `Int64` (kiểu số nguyên hỗ trợ `NA` của Pandas).

### 3.4. `clean_release_year(df: pd.DataFrame) -> pd.DataFrame`

- **Mục đích**: Đảm bảo năm phát hành là số nguyên hợp lệ.
- **Cách thức hoạt động**: Ép kiểu số an toàn thông qua `pd.to_numeric(..., errors='coerce').astype('Int64')`.

### 3.5. `clean_netflix_titles(df: pd.DataFrame) -> pd.DataFrame`

- **Mục đích**: Áp dụng toàn bộ quy trình làm sạch cho tập dữ liệu nòng cốt `netflix_titles`.
- **Thứ tự thực hiện**:
  1. `clean_text_columns`
  2. `clean_date_added`
  3. `clean_duration`
  4. `clean_release_year`

### 3.6. `clean_titles(df: pd.DataFrame) -> pd.DataFrame` & `clean_credits(df: pd.DataFrame) -> pd.DataFrame`

- **Mục đích**: Làm sạch các cột text và chuẩn hóa giá trị rỗng cho hai tập dữ liệu bổ trợ `titles` và `credits`.

### 3.7. `clean_all_data(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]`

- **Mục đích**: Hàm điều phối chính (Orchestrator), nhận vào từ điển dữ liệu thô và trả về từ điển chứa cả 3 DataFrame đã được làm sạch.

### 3.8. `cleaning_summary(before: dict[str, pd.DataFrame], after: dict[str, pd.DataFrame]) -> pd.DataFrame`

- **Mục đích**: Tạo bảng đối soát định lượng trước và sau khi làm sạch để kiểm tra tính toàn vẹn (số dòng, số cột, số dòng bị xóa).

### 3.9. `save_cleaned_data(cleaned_data: dict[str, pd.DataFrame], output_dir: str | Path = "data/processed") -> None`

- **Mục đích**: Ghi các DataFrame sạch ra thư mục `data/processed/` dưới định dạng CSV, sử dụng mã hóa `utf-8-sig` để tương thích tốt với tiếng Việt và các ký tự quốc tế.

---

## 4. Kết quả thực thi (Cleaning Results)

Khi chạy pipeline làm sạch dữ liệu, kết quả đối soát thu được như sau:

```text
=== CLEANING SUMMARY ===
         table  rows_before  rows_after  columns_before  columns_after  rows_removed
netflix_titles         8807        8807              12             14             0
        titles         6137        6137              15             15             0
       credits        81355       81355               5              5             0
```

### Đánh giá kết quả

1. **Bảo toàn số dòng (100%)**: Không có bất kỳ bản ghi nào bị loại bỏ ở giai đoạn này (`rows_removed = 0`). Việc lọc dữ liệu theo phạm vi nghiên cứu (2011–2020) được chuyển giao cho bước Normalization xử lý có chủ đích.
2. **Mở rộng thuộc tính hữu ích**:
   - `netflix_titles` tăng từ 12 cột lên 14 cột nhờ bổ sung 2 trường định lượng chuẩn hóa: `duration_minutes` và `duration_seasons`.
   - Cột `duration` gốc vẫn được giữ nguyên để đối chiếu khi cần thiết.
3. **Các tệp kết quả được tạo trong `data/processed/`**:
   - `netflix_titles.csv` (8,807 dòng $\times$ 14 cột)
   - `titles.csv` (6,137 dòng $\times$ 15 cột)
   - `credits.csv` (81,355 dòng $\times$ 5 cột)

---

## 5. Các quyết định thiết kế quan trọng

1. **Vì sao không xóa các dòng thiếu `date_added` ở bước Cleaning?**
   - 10 dòng bị thiếu ngày và 88 dòng lỗi ngày vẫn chứa đầy đủ các thông tin quan trọng khác (`title`, `cast`, `country`, `listed_in`, `release_year`).
   - Việc xóa ngay ở Cleaning sẽ làm mất dữ liệu có thể sử dụng cho phân tích khác (ví dụ: thống kê phân bố thể loại hay quốc gia không phụ thuộc vào ngày thêm).
   - Quyết định lọc phạm vi theo thời gian được đặt tại bước **Normalization** nhằm đảm bảo tính phân tầng trách nhiệm (*Separation of Concerns*).

2. **Vì sao tách `duration` thành hai cột thay vì giữ nguyên chuỗi?**
   - Giữ nguyên chuỗi dạng `"90 min"` hay `"2 Seasons"` không thể thực hiện các phép toán thống kê cơ bản như tính trung bình, trung vị, vẽ histogram hay so sánh thời lượng.
   - Việc tách thành `duration_minutes` (dành riêng cho Movie) và `duration_seasons` (dành riêng cho TV Show) giúp việc trực quan hóa trên Dashboard rõ ràng, không bị nhầm lẫn giữa đơn vị "phút" và "mùa".

---

## 6. Hướng dẫn chạy và tái lập

Thực thi module làm sạch độc lập từ terminal:

```powershell
# Chạy trực tiếp từ thư mục gốc
.venv\Scripts\python.exe src/cleaning.py
```

Dữ liệu sạch sẽ được cập nhật đồng bộ vào thư mục `data/processed/`, sẵn sàng làm đầu vào cho bước **Data Normalization**.
