# Netflix IDV — Phân tích catalog Netflix giai đoạn 2011–2020

> Dự án phân tích dữ liệu và trực quan hóa nhằm mô tả cách catalog Netflix thay đổi theo thời gian: số lượng nội dung được thêm vào, cơ cấu Movie/TV Show, thể loại, quốc gia liên quan, phân loại độ tuổi và xu hướng bổ sung theo tháng.

Repository này cung cấp một pipeline Python có thể chạy lại, dữ liệu đã được chuẩn hóa trong mô hình quan hệ, cơ sở dữ liệu SQLite, notebook phân tích và dashboard Power BI.

## Tổng quan nhanh

- **Đối tượng phân tích:** các title Netflix có date_added trong khoảng **01/01/2011–31/12/2020**.
- **Mốc thời gian chính:** date_added — thời điểm title được thêm vào catalog; không phải release_year.
- **Quy mô dữ liệu sau chuẩn hóa:** 7.294 title trong 120 tháng liên tiếp.
- **Nguồn chính:** data/raw/netflix_titles.csv.
- **Đầu ra chính:** các bảng CSV chuẩn hóa, database/netflix.db, kết quả mô hình trong data/model_outputs/ và dashboard dashboard/Dashboard_Custom.pbix.

## Dự án trả lời những câu hỏi nào?

1. Số title được thêm vào Netflix thay đổi như thế nào qua từng năm và từng tháng?
2. Movie và TV Show đóng góp như thế nào vào catalog theo thời gian?
3. Những genre nào xuất hiện nhiều nhất?
4. Những quốc gia nào có nhiều title liên quan nhất?
5. Cơ cấu rating/độ tuổi của catalog ra sao?
6. Một mô hình hồi quy tuyến tính đơn giản mô tả và ngoại suy xu hướng bổ sung title như thế nào?

## Phạm vi và cách đọc kết quả

Phân tích sử dụng date_added làm timeline, giới hạn trong 10 năm dương lịch 2011–2020. release_year chỉ được dùng làm thông tin ngữ cảnh về năm phát hành.

Các chỉ số về title luôn được tính bằng COUNT DISTINCT show_id. Một title có thể có nhiều genre, quốc gia, đạo diễn hoặc diễn viên; vì vậy các bảng liên kết là quan hệ nhiều-nhiều và tổng các nhóm genre/quốc gia không nhất thiết bằng tổng số title.

Dataset không chứa lượt xem, doanh thu, số subscriber hay hành vi người dùng. Do đó, kết quả chỉ mô tả **catalog trong dữ liệu**, không thể được diễn giải thành mức độ phổ biến, thị phần, sở thích khán giả hay nguyên nhân kinh doanh.

## Dữ liệu

### Dữ liệu nguồn

| File | Vai trò |
|---|---|
| data/raw/netflix_titles.csv | Dataset chính về title Netflix; dùng cho pipeline core |
| data/raw/titles.csv | Metadata bổ sung từ nguồn khác; không phải dependency của pipeline core |
| data/raw/credits.csv | Thông tin credits bổ sung; không phải dependency của pipeline core |

Dữ liệu trong data/raw/ được giữ nguyên. Các bước làm sạch và biến đổi ghi kết quả sang những thư mục đầu ra khác.

### Mô hình dữ liệu chuẩn hóa

| Bảng | Grain | Nội dung |
|---|---|---|
| dim_date | Một dòng mỗi ngày | Ngày, tháng, quý và năm trong phạm vi phân tích |
| dim_title | Một dòng mỗi title | Thông tin title, loại nội dung, ngày thêm, rating và duration |
| bridge_genre | Một dòng mỗi quan hệ title–genre | Tách các giá trị nhiều genre trong một ô |
| bridge_country | Một dòng mỗi quan hệ title–country | Tách quốc gia và bổ sung mã ISO alpha-3 |
| bridge_director | Một dòng mỗi quan hệ title–director | Danh sách đạo diễn của title |
| bridge_actor | Một dòng mỗi quan hệ title–actor | Danh sách diễn viên của title |
| fact_monthly_addition | Một dòng mỗi tháng | Số title được thêm trong tháng và chỉ số thời gian |

Các bảng này có sẵn tại data/normalized/ và đã được nạp vào database/netflix.db.

## Pipeline xử lý

~~~text
data/raw/netflix_titles.csv
        │
        ▼
Đọc dữ liệu → Làm sạch text, ngày tháng, duration và release_year
        │
        ▼
Lọc date_added trong 2011–2020
        │
        ▼
Chuẩn hóa thành dim/bridge/fact tables
        │
        ├── Kiểm tra khóa, bản ghi mồ côi, bản ghi trùng và số dòng
        ├── Ghi data/validation_report.json
        └── Nạp vào database/netflix.db
~~~

Entry point của pipeline là src/pipeline.py. Pipeline sử dụng đường dẫn tương đối tính từ thư mục dự án, không sửa dữ liệu raw và dừng nếu bước validation hoặc kiểm tra khóa ngoại thất bại.

## Kết quả phân tích nổi bật

Các insight đã được ghi lại trong [docs/insight_log.md](docs/insight_log.md). Một số kết quả chính:

- Số title được thêm tăng mạnh sau năm 2016, đạt 2.016 title vào năm 2019 và giảm nhẹ còn 1.879 title vào năm 2020.
- Movie chiếm 5.134/7.294 title (70,4%); TV Show chiếm 2.160/7.294 title (29,6%).
- International Movies là genre xuất hiện trên nhiều title nhất với 2.343 title.
- United States là quốc gia liên quan đến nhiều title nhất trong dữ liệu, tiếp theo là India và United Kingdom.
- Country chưa bao phủ toàn bộ catalog: 6.822/7.294 title có thông tin quốc gia.
- TV-MA và TV-14 chiếm tỷ trọng lớn trong các title có rating.

### Mô hình và forecast

Mô hình MVP dùng **Linear Regression** với:

- target: monthly_additions;
- feature: month_index từ 0 đến 119;
- train: các tháng năm 2011–2019;
- test: các tháng năm 2020;
- metrics: MAE, RMSE và R²;
- forecast: 9 tháng đầu năm 2021 trong các file output hiện có.

Kết quả chi tiết được lưu tại [docs/metrics.md](docs/metrics.md) và [data/model_outputs/](data/model_outputs/). Forecast là ngoại suy từ snapshot dữ liệu đến hết năm 2020, không phải số liệu thực tế hoặc dự báo chính thức của Netflix. Do R² trên tập test thấp/âm, mô hình nên được xem là baseline mô tả xu hướng dài hạn, không phải mô hình dự báo chính xác theo tháng.

## Dashboard

Dashboard Power BI nằm tại dashboard/Dashboard_Custom.pbix. Dashboard gồm **5 trang**, được thiết kế để khám phá:

- **Overview:** KPI và xu hướng số title được thêm theo năm/tháng.
- **Content Trend:** xu hướng bổ sung nội dung theo thời gian, Movie/TV Show và genre.
- **Geography:** phân bố theo quốc gia, dùng country_code cho bản đồ.
- **Content Characteristics:** đặc điểm nội dung theo genre, rating, duration và số mùa.
- **Forecast Evaluation:** monthly additions, đường xu hướng, forecast và sai số dự báo.

Các tương tác chính gồm bộ lọc, drill-down, tooltip và cross-filtering. Power BI có thể yêu cầu cập nhật lại đường dẫn nguồn khi mở repository trên máy khác; hãy trỏ nguồn về các file trong data/normalized/ hoặc database tương ứng.

## Cấu trúc repository

~~~text
.
├── data/
│   ├── raw/             # Dữ liệu nguồn, không chỉnh sửa
│   ├── processed/       # Dữ liệu sau làm sạch
│   ├── normalized/      # Các bảng dim/bridge/fact
│   └── model_outputs/   # Metrics, forecast và biểu đồ mô hình
├── database/
│   └── netflix.db       # SQLite database đã nạp dữ liệu chuẩn hóa
├── src/
│   ├── config.py        # Đường dẫn, phạm vi năm và ánh xạ quốc gia
│   ├── ingestion.py     # Đọc dữ liệu nguồn
│   ├── audit.py         # Kiểm tra cấu trúc, khóa, ngày và phạm vi
│   ├── cleaning.py      # Làm sạch dữ liệu
│   ├── normalization.py # Tạo mô hình dữ liệu chuẩn hóa
│   ├── validation.py    # Kiểm tra tính toàn vẹn và ghi báo cáo
│   ├── database.py      # Tạo/nạp/kiểm tra SQLite
│   └── pipeline.py      # Chạy toàn bộ luồng xử lý
├── notebook/            # Notebook audit, EDA và model
├── dashboard/           # Power BI dashboard
├── docs/                # Báo cáo, metric dictionary, insight và demo
├── requirements.txt
└── README.md
~~~

## Cài đặt và chạy lại

Yêu cầu Python 3.10 trở lên và Power BI Desktop nếu muốn mở dashboard.

### 1. Tạo môi trường và cài thư viện

Windows PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
~~~

### 2. Chạy toàn bộ pipeline

Từ thư mục gốc của repository:

~~~powershell
python src/pipeline.py
~~~

Sau khi chạy thành công, các đầu ra chính là:

- data/processed/netflix_titles.csv
- các file CSV trong data/normalized/
- data/validation_report.json
- database/netflix.db

### 3. Chạy notebook

~~~powershell
jupyter lab
~~~

Mở notebook theo thứ tự:

1. notebook/01_data_audit.ipynb
2. notebook/02_eda.ipynb
3. notebook/03_model.ipynb

### 4. Mở dashboard và tài liệu

- Mở dashboard/Dashboard_Custom.pbix bằng Power BI Desktop.
- Báo cáo tổng hợp: [docs/report.pdf](docs/report.pdf).
- Video demo: [docs/demo.mp4](docs/demo.mp4).
- Từ điển metric: [docs/metrics.md](docs/metrics.md).
- Nhật ký insight: [docs/insight_log.md](docs/insight_log.md).

## Giới hạn và khả năng mở rộng

- date_added phản ánh thời điểm dữ liệu ghi nhận title được thêm vào catalog, không nhất thiết phản ánh toàn bộ lịch sử phát hành của Netflix.
- Một số trường như country hoặc rating có thể bị thiếu; các tỷ lệ cần ghi rõ mẫu số và mức độ bao phủ.
- Dữ liệu nhiều-nhiều có thể gây double-count nếu không dùng COUNT DISTINCT show_id.
- Linear Regression hiện chỉ dùng một biến thời gian, chưa mô hình hóa seasonality hay các yếu tố bên ngoài.
- Có thể mở rộng bằng việc bổ sung kiểm định thống kê, mô hình chuỗi thời gian, metadata chất lượng cao hơn hoặc phân tích credits; các phần này không cần thiết cho pipeline core hiện tại.

## Tài liệu tham khảo trong repository

- [docs/report.pdf](docs/report.pdf): báo cáo dự án.
- [docs/metrics.md](docs/metrics.md): định nghĩa metric và kết quả model.
- [docs/insight_log.md](docs/insight_log.md): các insight kèm evidence và caveat.
- [docs/26_AnhAnhHoc_IDV_REPORT.docx](docs/26_AnhAnhHoc_IDV_REPORT.docx): bản báo cáo dạng Word.

## License và nguồn dữ liệu

Repository này được xây dựng cho mục đích học tập và trình bày đồ án.