# 04. Data Validation

## 1. Mục đích và vị trí trong Data Pipeline

Trong quy trình kỹ thuật dữ liệu, **Data Validation** (Kiểm định dữ liệu) đóng vai trò là một **Chốt chặn chất lượng (Quality Gate)** quan trọng nằm giữa bước Chuẩn hóa dữ liệu (**Data Normalization**) và bước Nạp dữ liệu vào cơ sở dữ liệu (**Database Storage**).

```text
Raw CSV (data/raw/)
  ↓
Ingestion (src/ingestion.py)
  ↓
Data Audit (docs/01_data_audit.md)
  ↓
Data Cleaning (src/cleaning.py)
  ↓
Data Normalization (src/normalization.py -> data/normalized/)
  ↓
Data Validation (src/validation.py -> data/validation_report.json)  ← BƯỚC HIỆN TẠI
  ↓
SQLite Database (src/database.py -> database/netflix.db)
```

### Mục tiêu chính

1. **Ngăn chặn dữ liệu bẩn vào CSDL**: Đảm bảo 100% dữ liệu chuẩn hóa tuân thủ nghiêm ngặt các ràng buộc quan hệ trước khi ghi vào SQLite, tránh các lỗi vi phạm khóa ngoại (`FOREIGN KEY constraint failed`) hoặc khóa chính.
2. **Kiểm chứng các quy tắc nghiệp vụ (Business Rules)**: Đối soát các chỉ số chuỗi thời gian, tính liên tục của các tháng, độ khớp giữa tổng số lượng bổ sung trên bảng Fact và số dòng trên bảng Dimension.
3. **Tự động hóa báo cáo chất lượng**: Xuất kết quả kiểm định chi tiết ra tệp `data/validation_report.json` phục vụ việc giám sát và kiểm tra tự động trong quy trình CI/CD.

---

## 2. Bộ quy tắc kiểm định toàn vẹn (Validation Rule Suite)

Module [`src/validation.py`](file:///D:/UTE/IDVI/Project_DataVisualization/src/validation.py) thiết lập 4 tầng kiểm tra độc lập và toàn diện:

### 2.1. Tầng 1: Kiểm định cấu trúc bảng và cột bắt buộc (`validate_structure`)

Kiểm tra sự hiện diện đầy đủ của cả 5 bảng chuẩn hóa và các trường dữ liệu thiết yếu:

| Bảng dữ liệu | Danh sách cột bắt buộc |
|---|---|
| `dim_date` | `date_key`, `date`, `year`, `month`, `month_name`, `quarter`, `quarter_name` |
| `dim_title` | `show_id`, `title`, `type`, `date_added`, `date_key`, `release_year`, `rating`, `duration_minutes`, `duration_seasons` |
| `bridge_genre` | `show_id`, `genre` |
| `bridge_country` | `show_id`, `country` |
| `fact_monthly_addition` | `date_key`, `monthly_additions`, `month_index` |

Nếu phát hiện thiếu bất kỳ bảng nào hoặc thiếu cột, hệ thống lập tức ghi nhận lỗi cấu trúc và dừng việc kiểm tra sâu để tránh ngoại lệ runtime.

### 2.2. Tầng 2: Kiểm định Khóa chính (`validate_primary_keys`)

Khóa chính của các bảng thực thể phải đảm bảo hai thuộc tính cốt lõi trong lý thuyết CSDL quan hệ:
- **Tính không rỗng (Non-null constraint)**: Cột khóa chính tuyệt đối không chứa giá trị `NULL`/`NaN`.
- **Tính duy nhất (Uniqueness constraint)**: Không được xuất hiện bất kỳ giá trị khóa nào bị trùng lặp.

Các khóa chính được kiểm tra:
1. `dim_date.date_key`
2. `dim_title.show_id`
3. `fact_monthly_addition.date_key`

### 2.3. Tầng 3: Kiểm định Khóa ngoại và Toàn vẹn tham chiếu (`validate_foreign_keys`)

Phát hiện và ngăn chặn hiện tượng **Khóa mồ côi (Orphan Keys)** – tức các giá trị khóa ngoại ở bảng con trỏ tới một giá trị không tồn tại ở bảng cha:

```text
dim_date.date_key (Cha)       ◄─── dim_title.date_key (Con)
dim_date.date_key (Cha)       ◄─── fact_monthly_addition.date_key (Con)
dim_title.show_id (Cha)       ◄─── bridge_genre.show_id (Con)
dim_title.show_id (Cha)       ◄─── bridge_country.show_id (Con)
```

Quy tắc:
$$\text{Orphan Keys} = \text{Set}(\text{Child Key}) \setminus \text{Set}(\text{Parent Key}) = \emptyset$$

### 2.4. Tầng 4: Kiểm định Quy tắc nghiệp vụ phân tích (`validate_business_rules`)

1. **Tính đầy đủ của chiều thời gian (`dim_date`)**:
   - Khoảng thời gian phân tích: `2011-01-01` đến `2020-12-31`.
   - Tổng số ngày yêu cầu: Đúng **3,653 ngày** (10 năm, trong đó có các năm nhuận 2012, 2016, 2020).
2. **Tính liên tục của chuỗi thời gian (`fact_monthly_addition`)**:
   - Tổng số tháng yêu cầu: Đúng **120 tháng** ($10 \times 12$).
   - Số lượng bổ sung không âm: $\text{monthly\_additions} \ge 0$.
   - Chỉ số `month_index` phải là một chuỗi số nguyên tăng dần liên tục không ngắt quãng từ $0$ đến $119$.
3. **Cân đối số lượng tác phẩm**:
   - Tổng metric trên bảng Fact phải bằng đúng số lượng bản ghi trên bảng Title:
   $$\sum \text{monthly\_additions} = \text{Count}(\text{dim\_title.show\_id}) = 7,294$$
4. **Phạm vi nghiên cứu (Scope Consistency)**:
   - Toàn bộ các bộ phim trong `dim_title` phải có năm thêm (`year(date_added)`) nằm trọn vẹn trong khoảng $[2011, 2020]$. Số dòng ngoài phạm vi phải bằng $0$.

---

## 3. Đặc tả chi tiết các hàm trong `src/validation.py`

### 3.1. `load_normalized_data(input_dir: str | Path) -> dict[str, pd.DataFrame]`
- Đọc đồng thời 5 tệp CSV từ thư mục `data/normalized/` vào một dictionary.

### 3.2. `validate_structure(data: dict[str, pd.DataFrame]) -> list[str]`
- So sánh tập hợp cột của từng DataFrame với từ điển `TABLES`. Trả về danh sách thông báo lỗi nếu phát hiện thiếu cột hoặc thiếu bảng.

### 3.3. `validate_primary_keys(data: dict[str, pd.DataFrame]) -> list[str]`
- Dùng phương thức `.isna().any()` và `.duplicated().any()` để kiểm tra vi phạm ràng buộc PK.

### 3.4. `validate_foreign_keys(data: dict[str, pd.DataFrame]) -> list[str]`
- Chuyển đổi các cột khóa thành `set` và thực hiện phép trừ tập hợp (`actual_keys - valid_keys`). Báo lỗi nếu số lượng orphan keys $> 0$.

### 3.5. `validate_business_rules(data: dict[str, pd.DataFrame]) -> list[str]`
- Kiểm tra các biểu thức logic nghiệp vụ: độ dài dải ngày, độ dài chuỗi tháng, tổng metric tích lũy và kiểm tra dải năm bằng `.dt.year.between(START_YEAR, END_YEAR)`.

### 3.6. `build_report(data: dict[str, pd.DataFrame]) -> dict[str, Any]`
- Tổng hợp toàn bộ các lỗi từ các tầng kiểm định. Nếu không có lỗi, gán `status = "PASS"`, ngược lại `status = "FAIL"`. Đồng thời tổng hợp thống kê số dòng và số cột của từng bảng.

### 3.7. `save_report(report: dict[str, Any], output_dir: str | Path) -> Path`
- Ghi đối tượng từ điển báo cáo ra tệp JSON chuẩn `validation_report.json` với định dạng dễ đọc (`indent=2`, `ensure_ascii=False`).

---

## 4. Báo cáo kết quả kiểm định thực tế

Khi chạy kiểm định trên tập dữ liệu chuẩn hóa, kết quả trên terminal:

```text
============================================================
VALIDATION - DỮ LIỆU CHUẨN HÓA
============================================================
dim_date                    3653 dòng |  7 cột
dim_title                   7294 dòng |  9 cột
bridge_genre               16026 dòng |  2 cột
bridge_country              8528 dòng |  3 cột
fact_monthly_addition        120 dòng |  3 cột

Kết quả: PASS
Tất cả kiểm tra đều đạt.

Đã lưu báo cáo: D:\UTE\IDVI\Project_DataVisualization\data\validation_report.json
```

### Nội dung tệp `data/validation_report.json`

```json
{
  "status": "PASS",
  "errors": [],
  "tables": {
    "dim_date": {
      "rows": 3653,
      "columns": 7
    },
    "dim_title": {
      "rows": 7294,
      "columns": 9
    },
    "bridge_genre": {
      "rows": 16026,
      "columns": 2
    },
    "bridge_country": {
      "rows": 8528,
      "columns": 3
    },
    "fact_monthly_addition": {
      "rows": 120,
      "columns": 3
    }
  }
}
```

---

## 5. Cơ chế Quality Gate và Xử lý Lỗi

Module được thiết kế với cơ chế phòng vệ nghiêm ngặt:
- Khi phát hiện bất kỳ lỗi nào (`status == "FAIL"`), hàm `main()` sẽ in danh sách lỗi chi tiết ra console và thực thi lệnh:
  ```python
  if report["status"] == "FAIL":
      raise SystemExit(1)
  ```
- Việc trả về mã thoát `1` (Exit code 1) đảm bảo rằng nếu chạy trong Pipeline hoặc kịch bản tự động (Bash / PowerShell / CI-CD), pipeline sẽ lập tức dừng lại, **không cho phép dữ liệu lỗi tiếp tục được nạp vào cơ sở dữ liệu SQLite**.

---

## 6. Hướng dẫn chạy và kiểm tra

Chạy module kiểm định độc lập từ dòng lệnh:

```powershell
.venv\Scripts\python.exe src/validation.py
```

Sau khi chạy, kiểm tra tệp báo cáo vừa được tạo tại:
- `data/validation_report.json`
