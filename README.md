# Netflix IDV – Phân tích xu hướng phim và TV Show trên Netflix 2011–2021

## 1. Mục tiêu đề tài

Đây là đồ án môn **Tương tác dữ liệu trực quan (Interactive Data Visualization – IDV)** của nhóm 3 người.

Đề tài tập trung vào:

> **Phân tích xu hướng nội dung phim và TV Show trên nền tảng Netflix giai đoạn 2011–2021**

Mục tiêu là xây dựng một pipeline hoàn chỉnh từ dữ liệu thô → tiền xử lý → phân hoạch dữ liệu → EDA → dashboard tương tác → insight → mô hình dự báo → báo cáo/demo.

Nhóm ưu tiên một phương án **đơn giản, dễ học, dễ giải thích, dễ tái lập và hoàn thành được trong 3 tuần**.

---

## 2. Phạm vi bài toán cuối cùng

### 2.1 Timeline chính

- **`date_added` là timeline chính** vì đề tài phân tích sự thay đổi của catalog Netflix theo thời điểm nội dung được thêm vào Netflix.
- **`release_year` chỉ là biến phụ/ngữ cảnh**, dùng để mô tả năm phát hành của nội dung.
- Scope chính: **2011–2021**.
- Snapshot hiện tại có `date_added` đến **25/09/2021**, vì vậy **2021 là năm chưa đầy đủ 12 tháng** và phải ghi rõ caveat trong báo cáo/dashboard.

### 2.2 Các câu hỏi nghiên cứu core

**Q1.** Số title được thêm vào Netflix theo năm thay đổi như thế nào?

**Q2.** Cơ cấu Movie và TV Show thay đổi như thế nào theo thời gian?

**Q3.** Những genre nào xuất hiện nhiều trong catalog Netflix và cơ cấu genre thay đổi ra sao?

**Q4.** Những quốc gia nào có nhiều title liên quan và phân bố địa lý như thế nào?

**Q5.** Rating độ tuổi được phân bố như thế nào và thay đổi ra sao theo thời gian/type?

**Q6.** Số title được thêm mới theo tháng có xu hướng gì?

**Q7.** Có thể dùng **Linear Regression** để ngoại suy số title được thêm mới trong **12 tháng sau snapshot** như thế nào?

### 2.3 Phân tích optional

Các phần sau chỉ làm **sau khi toàn bộ MVP core đã pass**:

- IMDb score trên tập title match được.
- Actor/director/talent.
- Scatter plot hoặc boxplot IMDb.
- Top actor/director.

Nếu thiếu thời gian, **cắt toàn bộ phần IMDb/talent trước**. Không cắt các yêu cầu core của dashboard, map, interaction hoặc forecast.

---

## 3. Dữ liệu

Nhóm hiện có 3 CSV raw:

| File | Quy mô đã kiểm tra | Vai trò |
|---|---:|---|
| `netflix_titles.csv` | 8,807 dòng / 12 cột | **Nguồn core** cho toàn bộ phân tích catalog |
| `titles.csv` | 6,137 dòng / 15 cột | Enrichment optional: IMDb/TMDB/title metadata |
| `credits.csv` | 81,355 dòng / 5 cột | Enrichment optional: actor/director |

Trong scope `date_added` 2011–2021 có khoảng **8,704 title**.

Một số kiểm tra kỹ thuật đã thực hiện:

- `netflix_titles.show_id` có 8,807 giá trị unique.
- `titles.id` có 6,137 giá trị unique.
- `titles.id ↔ credits.id` join được 100% theo tập `credits.id` đã kiểm tra.
- Join Netflix → `titles` bằng `title + release_year + type` sau chuẩn hóa chỉ match khoảng **35.1%** trong scope 2011–2021.

### Quyết định quan trọng

**Không INNER JOIN cả 3 CSV thành một unified table.**

Lý do:

1. `netflix_titles.show_id` không phải cùng hệ ID với `titles.id`/`credits.id`.
2. Netflix → titles chỉ match một phần nếu dựa trên title + year + type.
3. Ép JOIN 3 chiều có thể làm mất nhiều title hoặc tạo sai quan hệ.

Cách làm đúng cho đề tài là:

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

---

## 4. Mô hình dữ liệu cuối cùng

### 4.1 Ba bảng core

#### `dim_title`

**Grain:** 1 dòng / 1 Netflix title

Các field chính:

- `show_id`
- `type`
- `title`
- `date_added`
- `release_year`
- `rating`
- `duration`
- `description`
- calculated fields như `added_year`, `added_month`, `release_decade`, `title_age_when_added`, ...

Đây là bảng trung tâm cho KPI catalog.

#### `bridge_genre`

**Grain:** 1 dòng / 1 quan hệ title–genre

Ví dụ:

```text
show_id | genre
1       | Drama
1       | International
1       | TV Shows
```

Một title có thể có nhiều genre, vì vậy **không được dùng bridge này để đếm title mà không xử lý DISTINCT**.

#### `bridge_country`

**Grain:** 1 dòng / 1 quan hệ title–country

Có thể bổ sung `country_key` / `ISO3` để làm bản đồ.

Một title có thể có nhiều country, do đó country analysis cũng phải chú ý double-count.

### 4.2 Enrichment optional

Nếu còn thời gian có thể tạo:

- `titles_enrichment`
- `credits_enrichment`
- `map_netflix_to_title`
- `dim_person`

Nhưng các bảng này **không được trở thành dependency của dashboard MVP**.

### 4.3 Quy tắc đếm

KPI title phải dùng:

```text
COUNT DISTINCT show_id
```

Country/genre/person là quan hệ nhiều-nhiều nên phải dùng bridge và/hoặc DISTINCT để tránh nhân bản title.

---

## 5. Quy trình thực hiện đề tài

Pipeline chuẩn của nhóm:

```text
1. Ingest raw
      ↓
2. Audit
      ↓
3. Clean
      ↓
4. Partition thành 3 bảng logic
      ↓
5. Join / Merge có kiểm chứng
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
12. Final QA / Reproducibility
```

### Quy tắc

- Không sửa dữ liệu trong `data/raw/`.
- Mọi cleaning phải có lý do.
- Có before/after hoặc row reconciliation khi biến đổi dữ liệu.
- Không sử dụng path tuyệt đối phụ thuộc máy cá nhân.
- Không commit password, API key, token, cache hoặc file rác.
- Không suy luận nhân quả khi dataset không cung cấp biến để kiểm chứng.

---

## 6. Dashboard MVP

### Công cụ

**Power BI là phương án khuyến nghị cho MVP** vì phù hợp với mục tiêu hoàn thành nhanh các yêu cầu filter, drill-down, tooltip, cross-filter và map.

Nếu một thành viên đã rất quen **Streamlit + Plotly**, nhóm có thể dùng công cụ đó thay thế, nhưng nên chốt **một công cụ trước khi hết Tuần 1** và không đổi tool sau khi dashboard đã được xây dựng sâu.

### 4 trang dashboard

#### Trang 1 – Overview

Mục tiêu: trả lời Q1–Q2.

- KPI cards.
- Line: additions theo năm.
- Stacked Area: Movie vs TV Show.
- Filter: Year, Type.
- Drill-down: Year → Month.

#### Trang 2 – Content

Mục tiêu: trả lời Q3–Q5.

- Treemap: Genre.
- Heatmap: Rating × Year.
- Donut/Pie: rating mix.
- Filter: Year, Type, Genre, Rating.
- Cross-filter giữa Genre/Rating/Year.

#### Trang 3 – Geography

Mục tiêu: trả lời Q4.

- Choropleth Map.
- Horizontal Bar: top country.
- Tooltip.
- Drill-down: Country → Genre → Title.
- Click country để cross-filter.

#### Trang 4 – Forecast

Mục tiêu: trả lời Q6–Q7.

- Histogram: monthly additions.
- Line: actual vs fitted vs forecast.
- KPI model: MAE, RMSE, R².
- Forecast horizon: 12 tháng sau snapshot.

### 8 loại biểu đồ core

Dashboard MVP phải có ít nhất 8 loại khác nhau:

1. Line
2. Stacked Area
3. Treemap
4. Heatmap
5. Donut/Pie
6. Choropleth Map
7. Horizontal Bar
8. Histogram

IMDb scatter/boxplot là **optional**, không dùng để quyết định việc pass dashboard core.

### Interaction bắt buộc

- Filter.
- Drill-down.
- Tooltip.
- Cross-filtering / visual interaction.

Không chỉ đặt filter cho có; phải test rằng khi người dùng chọn một giá trị thì các visual liên quan thực sự cập nhật.

---

## 7. EDA

EDA được làm trước dashboard để kiểm tra dữ liệu và tìm insight.

Tối thiểu 5 biểu đồ static:

1. Additions theo năm.
2. Movie vs TV Show.
3. Top genre.
4. Top country.
5. Rating heatmap.

Mỗi biểu đồ phải trả lời một câu hỏi và có nhận xét ngắn.

EDA dùng để phát hiện xu hướng, lỗi dữ liệu và candidate insight; **không được dùng để khẳng định quan hệ nhân quả**.

---

## 8. Forecast / Machine Learning

### Model core

Dùng **Linear Regression** vì phù hợp với yêu cầu môn và đủ đơn giản để giải thích.

### Target

```text
monthly_additions = COUNT DISTINCT show_id theo tháng date_added
```

### Train/Test

Để bảo đảm đúng thứ tự thời gian:

- Train: 2016–2020.
- Test: 01–09/2021.
- Không random split.

### Metrics

- MAE
- RMSE
- R²

### Forecast

Ngoại suy **12 tháng tiếp theo** tính từ snapshot dữ liệu.

Phải ghi rõ:

> Đây là một phép ngoại suy từ dữ liệu catalog lịch sử bằng mô hình tuyến tính đơn giản, **không phải dự báo chính thức của Netflix**.

Khoảng tin cậy/band forecast là phần cộng thêm nếu còn thời gian; không để nó làm trễ MVP.

---

## 9. Sáu insight core phải có

Sau khi EDA và dashboard ổn định, nhóm cần chốt ít nhất 6 insight có bằng chứng:

1. **Additions theo năm** – số title được thêm vào Netflix thay đổi thế nào.
2. **Movie vs TV Show** – cơ cấu catalog thay đổi ra sao.
3. **Genre** – genre nào xuất hiện nhiều và thay đổi thế nào.
4. **Country** – phân bố title theo quốc gia.
5. **Rating** – cơ cấu rating và biến động theo thời gian.
6. **Monthly additions + forecast** – xu hướng thêm mới theo tháng và kết quả ngoại suy.

Mỗi insight phải có:

```text
Claim
  ↓
Evidence / số liệu
  ↓
Cách đọc
  ↓
Caveat / giới hạn
```

Không được viết:

- “Genre X được xem nhiều nhất” nếu dataset không có view count.
- “Khán giả thích Movie hơn TV Show” nếu chỉ có catalog count.
- “Netflix ưu tiên country X” nếu dataset không có biến chiến lược.
- “Năm 2021 giảm vì COVID/chiến lược Netflix” nếu không có dữ liệu để kiểm chứng.

---

## 10. Cấu trúc GitHub repo

Khuyến nghị dùng:

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

Nếu nhóm dùng Streamlit thay Power BI thì có thể đổi `dashboard/` thành:

```text
dashboard/
├── app.py
├── pages/
├── assets/
└── requirements.txt
```

---

## 11. Ba vai trò để tự ứng cử

### A – Data / Pipeline / Reproducibility

**Phù hợp với người thích:** Python, pandas, xử lý dữ liệu, kiểm tra lỗi, cấu trúc dữ liệu.

**Nhiệm vụ chính:**

- Audit 3 CSV.
- Kiểm tra null/duplicate/key/range.
- Cleaning.
- Tách `listed_in` thành `bridge_genre`.
- Tách `country` thành `bridge_country`.
- Tạo `dim_title`.
- Tạo calculated fields.
- Tạo monthly additions.
- Kiểm tra duplicate/double-count.
- Viết data dictionary + join report.
- Giữ pipeline có thể chạy lại.
- Hỗ trợ dữ liệu cho dashboard và report.

**Deliverable chính:**

`01_audit.py`, `02_clean.py`, `03_transform_join.py`, processed tables, data dictionary, DQ/join report.

**Nên chọn A nếu:** bạn muốn làm phần dữ liệu gốc và thích debug hơn là thiết kế giao diện.

**Kỹ năng cần ôn:** pandas merge/explode/groupby, datetime, DISTINCT logic, file path tương đối, Git cơ bản.

---

### B – EDA / Model / Insight

**Phù hợp với người thích:** phân tích, biểu đồ, thống kê cơ bản, giải thích kết quả.

**Nhiệm vụ chính:**

- Xây 5 EDA static.
- Định nghĩa metric/denominator.
- Chọn và kiểm chứng insight.
- Tạo monthly additions cho model.
- Huấn luyện Linear Regression.
- Time-based train/test.
- Tính MAE/RMSE/R².
- Forecast 12 tháng.
- Viết 6+ insight kèm caveat.
- Viết phần EDA/Model/Insight trong report.

**Deliverable chính:**

`04_eda.ipynb`, `05_model.ipynb`, `model_metrics.csv`, `insight_log.md`, phần EDA/Model/Insight của report.

**Nên chọn B nếu:** bạn thích đặt câu hỏi từ dữ liệu và giải thích “con số này có ý nghĩa gì”.

**Kỹ năng cần ôn:** pandas, matplotlib/seaborn, scikit-learn LinearRegression, regression metrics, storytelling.

---

### C – Dashboard / UI-UX / Deploy / Demo

**Phù hợp với người thích:** trực quan hóa, giao diện, thao tác dashboard, trình bày.

**Nhiệm vụ chính:**

- Chốt wireframe.
- Xây 4 trang Power BI.
- Đảm bảo 8 loại biểu đồ core.
- Làm map.
- Thiết lập filters.
- Thiết lập drill-down.
- Thiết lập tooltip.
- Thiết lập cross-filtering.
- Kiểm tra UX và số liệu hiển thị.
- Publish/đóng gói dashboard.
- Viết README phần chạy và chuẩn bị demo/video.

**Deliverable chính:**

Dashboard PBIX/app, wireframe, interaction map, demo script/video, phần Dashboard/UX/Demo của report.

**Nên chọn C nếu:** bạn thích làm phần mà giảng viên/người xem trực tiếp thao tác và nhìn thấy kết quả.

**Kỹ năng cần ôn:** Power BI, filter, drill-down, interactions, map, layout, Git/relative paths.

---

## 12. Review chéo và vấn đáp

Không ai chỉ biết đúng phần mình.

Quy tắc review:

```text
A ↔ B : data / metric / model input
A ↔ C : data binding / dashboard data
B ↔ C : insight / chart meaning / forecast display
```

Trong tuần 3:

- A tự chạy lại EDA/model/dashboard ở mức kiểm tra.
- B tự kiểm tra data model và dashboard interactions.
- C tự kiểm tra cleaning, join logic và forecast.

Mục tiêu là nếu một thành viên vắng mặt, hai người còn lại vẫn hiểu cách hệ thống hoạt động ở mức đủ để giải thích và chạy lại.

---

## 13. Kế hoạch 3 tuần

### Tuần 1 – Dữ liệu + EDA + Prototype

**21–27/09/2026**

- Khóa scope và tool.
- Audit 3 CSV.
- Cleaning.
- Tạo 3 bảng core.
- Tạo calculated fields.
- Tạo monthly additions.
- EDA 5 biểu đồ.
- Prototype dashboard.
- Cuối tuần: M1 sign-off.

### Tuần 2 – Dashboard + Forecast

**28/09–04/10/2026**

- Wireframe 4 trang.
- Chuẩn hóa country/ISO3.
- Hoàn thành Overview + Content + Geography.
- Linear Regression.
- Forecast 12 tháng.
- Hoàn thành Forecast page.
- Test filter/drill-down/tooltip/cross-filter.
- Khóa dashboard MVP.
- Cuối tuần: M2 sign-off.

### Tuần 3 – Insight + Report + Demo + QA

**05–11/10/2026**

- Chốt 6+ insights.
- Hoàn thiện report.
- README + requirements + docs.
- Test clean clone/re-run.
- Video demo backup.
- Luyện vấn đáp.
- Đóng gói final submission.
- **10–11/10 là buffer cho bug và chỉnh sửa cuối.**

---

## 14. Sản phẩm cuối cùng

Bộ nộp phải có tối thiểu:

1. **GitHub repository** có cấu trúc rõ ràng.
2. **3 bảng dữ liệu logic core:** `dim_title`, `bridge_genre`, `bridge_country`.
3. **EDA notebook** với ít nhất 5 biểu đồ static.
4. **Dashboard MVP 4 trang**.
5. **≥8 loại biểu đồ**, bao gồm map.
6. **Filter + drill-down + tooltip + cross-filtering**.
7. **Linear Regression** + MAE/RMSE/R².
8. **Forecast 12 tháng**.
9. **≥6 insight có evidence + caveat**.
10. **Báo cáo cuối kỳ** theo yêu cầu môn.
11. **README.md**.
12. **requirements.txt**.
13. **Video demo backup**.

---

## 15. Cách chạy phần Python

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Chạy pipeline

```powershell
python src/01_audit.py
python src/02_clean.py
python src/03_transform_join.py
```

### Chạy notebook

```powershell
jupyter lab
```

Sau đó chạy theo thứ tự:

```text
04_eda.ipynb
05_model.ipynb
```

### Dashboard Power BI

Mở:

```text
dashboard/netflix_idv.pbix
```

Sau khi clone repo trên máy khác, kiểm tra lại source path của Power BI và trỏ về `data/processed/` nếu cần.

---

## 16. Git workflow đơn giản

Dùng `main` làm nhánh ổn định.

Mỗi người có thể làm trên branch riêng:

```text
feature/data
feature/eda-model
feature/dashboard
```

Sau khi xong một task:

```bash
git add .
git commit -m "feat: audit netflix raw data"
git push
```

Không commit:

- `.venv/`
- `__pycache__/`
- `.ipynb_checkpoints/`
- secrets/API keys
- file tạm
- dữ liệu phát sinh không kiểm soát

---

## 17. Những việc KHÔNG làm trong MVP

Để kịp 3 tuần, không mở rộng sang:

- Dự đoán số lượt xem.
- Dự đoán doanh thu.
- Dự đoán subscriber.
- Phân tích hành vi người dùng.
- Causal analysis.
- Clustering/classification chỉ để “có thêm ML”.
- Prophet như mô hình chính thay cho Linear Regression.
- IMDb/talent trước khi dashboard core hoàn chỉnh.
- Ép JOIN 3 CSV thành một bảng.
- Thêm nhiều chart trùng ý nghĩa chỉ để tăng số lượng.

---

## 18. Definition of Done

Dự án được xem là hoàn thành khi tất cả câu trả lời dưới đây là **Có**:

- [ ] Scope 2011–2021 đã khóa.
- [ ] `date_added` là timeline chính.
- [ ] Raw data được giữ nguyên.
- [ ] Có audit và cleaning log.
- [ ] Có ít nhất 3 bảng logic core.
- [ ] Có JOIN/Merge được giải thích bằng key + cardinality.
- [ ] Không double-count title.
- [ ] Có 5 EDA static.
- [ ] Dashboard có 4 trang core.
- [ ] Có 8 loại biểu đồ core.
- [ ] Có map.
- [ ] Có filter.
- [ ] Có drill-down.
- [ ] Có tooltip.
- [ ] Có cross-filtering.
- [ ] Có Linear Regression.
- [ ] Có MAE/RMSE/R².
- [ ] Có forecast 12 tháng.
- [ ] Có ít nhất 6 insights.
- [ ] Insight có caveat.
- [ ] README có hướng dẫn chạy.
- [ ] Repo clone được trên máy khác.
- [ ] Báo cáo hoàn chỉnh.
- [ ] Video demo backup có sẵn.
- [ ] Cả 3 thành viên đều giải thích được pipeline.

---

## 19. Nguyên tắc cuối cùng của nhóm

> **Core trước – optional sau.**
>
> Không cố làm thật nhiều thứ; hãy làm một pipeline nhỏ nhưng hoàn chỉnh và giải thích được từ đầu đến cuối.

Khi thiếu thời gian, thứ tự ưu tiên là:

```text
Data quality
→ 3 bảng core
→ EDA
→ Dashboard + 8 chart types + Map + Interaction
→ Linear Regression + Forecast
→ 6 Insights
→ Report / Demo / Reproducibility
→ IMDb / Talent (chỉ nếu còn thời gian)
```

