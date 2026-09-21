# Netflix IDV – Phân tích xu hướng phim và TV Show trên Netflix 2011–2020

## 1. Mục tiêu đề tài

Đây là đồ án môn **Tương tác dữ liệu trực quan (Interactive Data Visualization – IDV)** của nhóm 3 người.

> **Phân tích xu hướng nội dung phim và TV Show trên nền tảng Netflix giai đoạn 2011–2020**

Nhóm chọn **đúng 10 năm dương lịch đầy đủ từ đầu 2011 đến hết 2020**. Việc bỏ 2021 giúp timeline tròn 10 năm và tránh phải xử lý năm 2021 bị thiếu dữ liệu.

Mục tiêu:

```text
Dữ liệu thô → Audit → Cleaning → Phân hoạch dữ liệu
→ JOIN/Merge → EDA → Dashboard → Insight
→ Linear Regression + Forecast → Report/Demo
```

Nguyên tắc:

> **Core trước – optional sau.** Làm một hệ thống nhỏ nhưng hoàn chỉnh, dễ học, dễ giải thích và dễ chạy lại.

---

## 2. Phạm vi bài toán

### 2.1 Timeline

- **`date_added` là timeline chính** vì nhóm phân tích sự thay đổi catalog theo thời điểm title được thêm vào Netflix.
- **`release_year` chỉ là biến phụ/ngữ cảnh**.
- Scope: **2011-01-01 → 2020-12-31**.
- Đây là **10 năm dương lịch đầy đủ**.
- Raw CSV vẫn giữ nguyên; dữ liệu processed/analysis mới lọc theo scope.
- **Không dùng actual 2021 làm dữ liệu phân tích core.**
- Forecast 12 tháng được tạo từ mốc cuối 2020 và được xem là **ngoại suy**, không phải số liệu thực tế của 2021.

### 2.2 Câu hỏi nghiên cứu core

1. Số title được thêm vào Netflix theo năm thay đổi như thế nào?
2. Cơ cấu Movie và TV Show thay đổi như thế nào theo thời gian?
3. Những genre nào xuất hiện nhiều và cơ cấu genre thay đổi ra sao?
4. Những quốc gia nào có nhiều title liên quan và phân bố địa lý như thế nào?
5. Rating độ tuổi được phân bố như thế nào và thay đổi ra sao?
6. Số title được thêm mới theo tháng có xu hướng gì?
7. Từ dữ liệu đến hết 2020, Linear Regression có thể ngoại suy số title được thêm mới trong 12 tháng tiếp theo như thế nào?

### 2.3 Ngoài phạm vi

Không phân tích:

- lượt xem;
- doanh thu;
- subscriber;
- hành vi người dùng;
- mức độ yêu thích;
- nguyên nhân kinh doanh nếu dataset không có biến kiểm chứng;
- popularity prediction;
- causal analysis.

---

## 3. Dữ liệu

| File | Quy mô đã kiểm tra | Vai trò |
|---|---:|---|
| `netflix_titles.csv` | 8,807 dòng / 12 cột | **Nguồn core** cho catalog |
| `titles.csv` | 6,137 dòng / 15 cột | Enrichment optional: IMDb/TMDB/title metadata |
| `credits.csv` | 81,355 dòng / 5 cột | Enrichment optional: actor/director |

Sau khi lọc `date_added` trong scope 2011–2020, `netflix_titles.csv` có **7,206 title**.

Các kiểm tra chính:

- `netflix_titles.show_id` là khóa duy nhất cho catalog core.
- `titles.id` là khóa duy nhất trong `titles.csv`.
- `titles.id ↔ credits.id` có thể join trực tiếp.
- Crosswalk Netflix → `titles` bằng `title + release_year + type` chỉ match một phần, nên **không dùng làm dependency cho dashboard core**.

### Quyết định quan trọng

**Không INNER JOIN cả 3 CSV thành một unified table.**

```text
3 CSV RAW
   ↓
Audit / Clean / Transform
   ↓
3 bảng logic CORE
   ├── dim_title
   ├── bridge_genre
   └── bridge_country
   ↓
Analysis / Dashboard

Optional enrichment
   ├── titles.csv
   └── credits.csv
```

Điều này phù hợp với hướng dẫn của giảng viên: dữ liệu thô có thể được tiền xử lý và phân hoạch thành các bảng logic để đáp ứng yêu cầu đồ án.

---

## 4. Mô hình dữ liệu

### `dim_title`

**Grain:** 1 dòng / 1 Netflix title.

Field chính:

```text
show_id
type
title
date_added
release_year
rating
duration
description
added_year
added_month
...
```

### `bridge_genre`

**Grain:** 1 dòng / 1 quan hệ title–genre.

Một title có thể có nhiều genre.

### `bridge_country`

**Grain:** 1 dòng / 1 quan hệ title–country.

Một title có thể có nhiều country. Có thể thêm `ISO3` để làm map.

### `fact_monthly_additions`

**Grain:** 1 dòng / 1 tháng.

```text
month | monthly_additions
```

Tính bằng:

```text
COUNT DISTINCT show_id
GROUP BY month(date_added)
```

Đây là target/feature phục vụ forecast.

### Enrichment optional

Nếu còn thời gian:

- `titles_enrichment`
- `credits_enrichment`
- IMDb
- actor/director

Các phần này **không được trở thành dependency của MVP**. Nếu thiếu thời gian, cắt IMDb/talent đầu tiên.

---

## 5. Quy tắc dữ liệu

### Không double-count title

KPI title phải dùng:

```text
COUNT DISTINCT show_id
```

Không được lấy số dòng của bridge table rồi gọi đó là số title.

### Many-to-many

Một title có thể có nhiều genre, country hoặc person. Vì vậy phải dùng bridge table và DISTINCT khi tính KPI.

### Raw không được sửa

```text
data/raw/
```

chỉ chứa dữ liệu nguồn.

Mọi xử lý tạo dữ liệu ở:

```text
data/processed/
```

---

## 6. Pipeline

```text
1. Ingest raw
      ↓
2. Audit
      ↓
3. Clean
      ↓
4. Partition thành 3 bảng logic
      ↓
5. JOIN / Merge có kiểm chứng
      ↓
6. Calculated fields
      ↓
7. EDA
      ↓
8. Dashboard
      ↓
9. Linear Regression + Forecast
      ↓
10. Insight + Caveat
      ↓
11. Report + Demo
      ↓
12. Final QA
```

Nguyên tắc:

- Không sửa `data/raw/`.
- Cleaning phải có lý do.
- Có before/after hoặc reconciliation.
- Không dùng absolute path.
- Không commit secret/API key/token.
- Không suy luận causal nếu dataset không có biến kiểm chứng.

---

## 7. Dashboard MVP

### Công cụ

**Power BI** là phương án MVP của nhóm vì phù hợp với:

- Filter;
- Drill-down;
- Tooltip;
- Cross-filtering;
- Map.

Nếu một thành viên đã rất quen Streamlit + Plotly thì có thể thay thế, nhưng phải chốt **một công cụ duy nhất trong Tuần 1**.

### 4 trang

#### Trang 1 – Overview

- KPI cards.
- Line: additions theo năm.
- Stacked Area: Movie vs TV Show.
- Filter Year / Type.
- Drill-down Year → Month.

#### Trang 2 – Content

- Treemap: Genre.
- Heatmap: Rating × Year.
- Donut/Pie: rating mix.
- Filter Year / Type / Genre / Rating.
- Cross-filter.

#### Trang 3 – Geography

- Choropleth Map.
- Horizontal Bar: top country.
- Tooltip.
- Drill-down nếu phù hợp.
- Click country để cross-filter.

#### Trang 4 – Forecast

- Histogram: monthly additions.
- Line: actual vs fitted vs forecast.
- KPI: MAE, RMSE, R².
- Forecast horizon: 12 tháng sau 31/12/2020.

### 8 loại chart core

1. Line
2. Stacked Area
3. Treemap
4. Heatmap
5. Donut/Pie
6. Choropleth Map
7. Horizontal Bar
8. Histogram

IMDb scatter/boxplot là **optional**.

### Interaction bắt buộc

- Filter.
- Drill-down.
- Tooltip.
- Cross-filtering / visual interaction.

---

## 8. EDA

Tối thiểu 5 biểu đồ static:

1. Additions theo năm.
2. Movie vs TV Show.
3. Top genre.
4. Top country.
5. Rating heatmap.

Mỗi chart phải có:

```text
Question → Metric → Chart → Observation → Caveat
```

---

## 9. Forecast / Machine Learning

### Model

Chỉ dùng **Linear Regression** cho MVP.

### Target

```text
monthly_additions
= COUNT DISTINCT show_id theo tháng date_added
```

### Time split

```text
Train: 2011–2019
Test: 2020
```

**Không random split.**

Sau khi đánh giá:

```text
Fit lại trên toàn bộ 2011–2020
        ↓
Forecast 12 tháng sau 31/12/2020
```

Metrics:

- MAE
- RMSE
- R²

Cách diễn đạt:

> Đây là ngoại suy 12 tháng tiếp theo từ snapshot dữ liệu đến hết 2020 bằng mô hình tuyến tính đơn giản, không phải dự báo chính thức của Netflix.

---

## 10. Sáu insight core

1. **Additions theo năm** – số title được thêm vào thay đổi thế nào trong 2011–2020?
2. **Movie vs TV Show** – cơ cấu catalog thay đổi ra sao?
3. **Genre** – genre nào xuất hiện nhiều và thay đổi thế nào?
4. **Country** – title phân bố theo quốc gia ra sao?
5. **Rating** – cơ cấu rating thay đổi thế nào?
6. **Monthly additions + forecast** – xu hướng thêm mới theo tháng và kết quả ngoại suy.

Mỗi insight:

```text
Claim
↓
Evidence / số liệu
↓
Cách đọc
↓
Caveat
```

Không được biến catalog count thành view count, popularity, audience preference, revenue hoặc business strategy.

---

## 11. Cấu trúc GitHub repo

```text
netflix-idv/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── netflix_titles.csv
│   │   ├── titles.csv
│   │   └── credits.csv
│   │
│   └── processed/
│       ├── dim_title.csv
│       ├── bridge_genre.csv
│       ├── bridge_country.csv
│       └── fact_monthly_additions.csv
│
├── src/
│   ├── 01_audit.py
│   ├── 02_clean.py
│   └── 03_transform_join.py
│
├── notebooks/
│   ├── 04_eda.ipynb
│   └── 05_model.ipynb
│
├── dashboard/
│   ├── netflix_idv.pbix
│   └── assets/
│
└── docs/
    ├── scope.md
    ├── data_dictionary.md
    ├── metrics.md
    ├── data_model.md
    ├── join_report.md
    ├── insight_log.md
    ├── source_log.md
    ├── interaction_map.md
    └── report.pdf
```

Nếu dùng Streamlit:

```text
dashboard/
├── app.py
├── pages/
├── assets/
└── requirements.txt
```

---

## 12. Ba vai trò để tự ứng cử

### A – Data / Pipeline / Reproducibility

Phù hợp với người thích Python, pandas, xử lý dữ liệu và debug.

Nhiệm vụ:

- Audit 3 CSV.
- Kiểm tra null/duplicate/key/range.
- Cleaning.
- Tách genre.
- Tách country.
- Tạo `dim_title`.
- Tạo calculated fields.
- Tạo monthly additions.
- Kiểm tra double-count.
- Viết data dictionary.
- Viết join/data-quality report.
- Đảm bảo pipeline chạy lại được.

Deliverable:

```text
01_audit.py
02_clean.py
03_transform_join.py
data/processed/
data_dictionary.md
join_report.md
```

**Nên ứng cử A nếu:** bạn thích làm phần dữ liệu và debug.

---

### B – EDA / Model / Insight

Phù hợp với người thích phân tích, thống kê cơ bản, biểu đồ và giải thích kết quả.

Nhiệm vụ:

- Làm 5 EDA static.
- Định nghĩa metric.
- Tìm và kiểm chứng insight.
- Linear Regression.
- Time-based train/test.
- MAE/RMSE/R².
- Forecast 12 tháng.
- Viết 6+ insight.
- Viết caveat.
- Phụ trách EDA/Model/Insight trong report.

Deliverable:

```text
04_eda.ipynb
05_model.ipynb
model_metrics.csv
insight_log.md
```

**Nên ứng cử B nếu:** bạn thích trả lời “dữ liệu đang cho thấy điều gì?”.

---

### C – Dashboard / UI-UX / Demo

Phù hợp với người thích Power BI, trực quan hóa, giao diện và trình bày.

Nhiệm vụ:

- Wireframe.
- 4 dashboard pages.
- 8 chart types.
- Map.
- Filters.
- Drill-down.
- Tooltip.
- Cross-filtering.
- Dashboard QA.
- Demo/video.
- README setup.
- Dashboard/Demo trong report.

Deliverable:

```text
dashboard/
interaction_map.md
demo script/video
```

**Nên ứng cử C nếu:** bạn thích làm phần trực quan và demo.

---

## 13. Review chéo

```text
A ↔ B : data / metric / model input
A ↔ C : data binding / dashboard data
B ↔ C : insight / chart meaning / forecast
```

Trong tuần 3, mỗi người phải kiểm tra phần của người khác.

Mục tiêu: nếu một thành viên vắng mặt, hai người còn lại vẫn hiểu đủ pipeline để giải thích và chạy lại dự án.

---

## 14. Kế hoạch 3 tuần

### Tuần 1 – Data + EDA + Prototype
**21–27/09/2026**

- Khóa scope 2011–2020.
- Audit.
- Cleaning.
- 3 bảng core.
- Calculated fields.
- Monthly additions.
- EDA 5 chart.
- Dashboard prototype.
- M1 sign-off.

### Tuần 2 – Dashboard + Forecast
**28/09–04/10/2026**

- Wireframe.
- Country/ISO3.
- Overview.
- Content.
- Geography.
- Linear Regression.
- Forecast.
- Interaction test.
- Khóa dashboard MVP.
- M2 sign-off.

### Tuần 3 – Insight + Report + Demo + QA
**05–11/10/2026**

- Chốt 6+ insights.
- Hoàn thiện report.
- README/docs.
- Clean clone/re-run test.
- Video backup.
- Luyện vấn đáp.
- Final package.
- 10–11/10 là buffer.

---

## 15. Sản phẩm cuối cùng

Tối thiểu:

1. GitHub repository.
2. `dim_title`.
3. `bridge_genre`.
4. `bridge_country`.
5. EDA notebook với ≥5 static charts.
6. Dashboard 4 trang.
7. ≥8 loại chart + map.
8. Filter + drill-down + tooltip + cross-filtering.
9. Linear Regression.
10. MAE/RMSE/R².
11. Forecast 12 tháng sau 31/12/2020.
12. ≥6 insights.
13. PDF report.
14. README.
15. `requirements.txt`.
16. Video demo backup.

---

## 16. Cách chạy Python

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Pipeline

```powershell
python src/01_audit.py
python src/02_clean.py
python src/03_transform_join.py
```

### Notebook

```powershell
jupyter lab
```

Chạy theo thứ tự:

```text
04_eda.ipynb
05_model.ipynb
```

### Power BI

Mở:

```text
dashboard/netflix_idv.pbix
```

Sau khi clone trên máy khác, kiểm tra lại source path của Power BI và trỏ về `data/processed/` nếu cần.

---

## 17. Git workflow

Dùng `main` làm branch ổn định.

Branches:

```text
feature/data
feature/eda-model
feature/dashboard
```

Ví dụ:

```bash
git add .
git commit -m "feat: audit netflix raw data"
git push
```

Không commit:

```text
.venv/
__pycache__/
.ipynb_checkpoints/
secrets
API keys
cache
file tạm
```

---

## 18. Những việc không làm trong MVP

Để kịp 3 tuần, không mở rộng sang:

- Dự đoán lượt xem.
- Dự đoán doanh thu.
- Dự đoán subscriber.
- User behavior.
- Causal analysis.
- Clustering/classification chỉ để có thêm ML.
- Prophet như mô hình chính.
- IMDb/talent trước khi dashboard core hoàn chỉnh.
- Ép JOIN 3 CSV thành một bảng.
- Thêm chart trùng ý nghĩa chỉ để tăng số lượng.

---

## 19. Definition of Done

- [ ] Scope = 2011–2020.
- [ ] Đúng 10 năm dương lịch đầy đủ.
- [ ] `date_added` là timeline chính.
- [ ] Raw data được giữ nguyên.
- [ ] Có audit + cleaning log.
- [ ] Có ≥3 bảng logic core.
- [ ] Có JOIN/Merge được giải thích bằng key/cardinality.
- [ ] Không double-count title.
- [ ] Có ≥5 EDA static charts.
- [ ] Dashboard có 4 trang core.
- [ ] Có ≥8 loại chart.
- [ ] Có map.
- [ ] Có filter.
- [ ] Có drill-down.
- [ ] Có tooltip.
- [ ] Có cross-filtering.
- [ ] Có Linear Regression.
- [ ] Có MAE/RMSE/R².
- [ ] Có forecast 12 tháng sau 31/12/2020.
- [ ] Có ≥6 insights.
- [ ] Insight có evidence + caveat.
- [ ] README có hướng dẫn chạy.
- [ ] Repo clone được trên máy khác.
- [ ] Report hoàn chỉnh.
- [ ] Video demo backup.
- [ ] Cả 3 thành viên hiểu được toàn pipeline.

---

## 20. Nguyên tắc cuối cùng

> **Đừng cố làm thật nhiều. Hãy làm một pipeline nhỏ nhưng hoàn chỉnh và giải thích được từ đầu đến cuối.**

Khi thiếu thời gian:

```text
Data quality
→ 3 bảng core
→ EDA
→ Dashboard + 8 chart types + Map + Interaction
→ Linear Regression + Forecast
→ 6 Insights
→ Report / Demo / Reproducibility
→ IMDb / Talent nếu còn thời gian
```
