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

1. Tách các thuộc tính đa trị `listed_in` và `country` thành bảng cầu nối (1NF).
2. Tạo `dim_date` để phân tích theo ngày, tháng, quý và năm.
3. Tạo `fact_monthly_addition` để phân tích xu hướng và forecasting.
4. Bổ sung mã định danh địa lý chuẩn hóa (`country_code`) phục vụ biểu đồ bản đồ (Choropleth Map).
5. Kiểm tra PK/FK, orphan key và bản ghi trùng.
6. Lưu kết quả thành CSV trong `data/normalized/`.

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
      │              │ │country_code   │
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

**Mục đích:** lưu thông tin mô tả của Movie/TV Show trong phạm vi nghiên cứu 2011–2020.

| Cột | Vai trò | Mô tả |
|---|---|---|
| `show_id` | PK | Mã title duy nhất |
| `title` | — | Tên phim/chương trình |
| `type` | — | `Movie` hoặc `TV Show` |
| `date_added` | — | Ngày Netflix thêm title |
| `date_key` | FK | → `dim_date.date_key` |
| `release_year` | — | Năm phát hành |
| `rating` | — | Phân loại độ tuổi |
| `duration_minutes` | — | Thời lượng Movie (phút) |
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

**Mục đích:** chuẩn hóa thuộc tính đa trị `country` và bổ sung mã định danh địa lý phục vụ trực quan hóa bản đồ (*Choropleth Map*).

Ví dụ:

```text
s1 | United States, Canada
```

thành:

```text
s1 | United States | USA
s1 | Canada        | CAN
```

| Cột | Vai trò | Mô tả |
|---|---|---|
| `show_id` | FK | → `dim_title.show_id` |
| `country` | Thành phần PK | Tên quốc gia nguyên bản |
| `country_code` | Attribute | Mã quốc gia chuẩn ISO 3166-1 alpha-3 (3 ký tự) |

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
| `create_bridge_country()` | Tách `country` thành từng country và gắn `country_code` |
| `get_country_code()` | Chuyển tên quốc gia sang mã ISO-3 theo chiến lược Hybrid |
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
- Loại bỏ khoảng trắng thừa, các giá trị rỗng/NULL và các cặp trùng.
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

Kết quả thực tế:

```text
dim_date
    rows = 3653
    duplicate_date_key = 0
    null_date_key = 0

dim_title
    rows = 7294
    duplicate_show_id = 0
    null_show_id = 0
    orphan_date_key = 0

fact_monthly_addition
    rows = 120
    duplicate_date_key = 0
    null_date_key = 0
    orphan_date_key = 0
    total_additions = 7294

bridge_genre
    rows = 16026
    orphan_show_id = 0
    duplicate_pairs = 0

bridge_country
    rows = 8528
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

### 6.4. Xử lý trường `country_code` trong `bridge_country` cho biểu đồ bản đồ (Choropleth Map)

#### 6.4.1. Bối cảnh và vấn đề phát sinh

Để phục vụ hiển thị biểu đồ nhiệt phân bố nội dung toàn cầu (*Choropleth Map*) trên Streamlit và Plotly, các công cụ đồ họa yêu cầu mã định danh địa lý chuẩn quốc tế **ISO 3166-1 alpha-3** (mã 3 ký tự, ví dụ: `USA`, `VNM`, `GBR`, `DEU`, `FRA`) nhằm khớp với ranh giới hình học trên bản đồ số thế giới (GeoJSON). Việc dùng tên chuỗi thông thường (`country`) dễ gây lỗi vì có nhiều dị bản chính tả hoặc khác biệt ngôn ngữ.

Tuy nhiên, khi tiến hành ánh xạ tự động 122 quốc gia xuất hiện trong danh mục của Netflix bằng thư viện `pycountry.countries.lookup()`, hệ thống gặp **7 trường hợp lỗi tra cứu nghiêm trọng**, làm ảnh hưởng tới hơn 150 bộ phim:

1. **Nhóm quốc gia lịch sử / tiền thân (Historical / Former Countries)**:
   - `West Germany` (Tây Đức - 5 phim), `East Germany` (Đông Đức - 1 phim): Đã thống nhất vào năm 1990. Trong chuẩn ISO, các quốc gia lịch sử được chuyển sang chuẩn ISO 3166-3 với mã 4 ký tự (`DEHY`, `DDRH`).
   - `Soviet Union` (Liên Xô - 3 phim): Đã tan rã năm 1991, có mã lịch sử là `SUHH`.
   - *Hậu quả*: Thư viện bản đồ thế giới ngày nay chỉ hiển thị các vùng lãnh thổ của các quốc gia hiện hành. Nếu gán mã 4 ký tự hoặc để trống (`NaN`), các tác phẩm điện ảnh này sẽ hoàn toàn biến mất trên bản đồ. Để trực quan hóa, cần ánh xạ các thực thể lịch sử này về vùng lãnh thổ quốc gia kế thừa tương ứng trên bản đồ hiện đại (`West Germany`/`East Germany` → `DEU` - Đức; `Soviet Union` → `RUS` - Nga).

2. **Nhóm tên thông dụng không khớp tên chính thức ISO (Official Name Mismatches)**:
   - `Turkey` (Thổ Nhĩ Kỳ - 113 phim): Năm 2022, Thổ Nhĩ Kỳ đã chính thức đổi tên quốc tế tại Liên Hợp Quốc và ISO thành **Türkiye** (`TUR`). Các phiên bản `pycountry` mới dùng tên "Türkiye" nên khi tìm chuỗi cũ `"Turkey"` sẽ bị lỗi.
   - `Russia` (Nga - 27 phim): Tên chính thức trong ISO là **Russian Federation** (`RUS`), tìm kiếm chính xác theo chuỗi `"Russia"` sẽ thất bại.
   - `Palestine` (1 phim): Tên chính thức là **Palestine, State of** (`PSE`).
   - `Vatican City` (1 phim): Tên chính thức là **Holy See (Vatican City State)** (`VAT`).

Nếu không xử lý, riêng **Turkey (113 phim)** và **Russia (27 phim)** sẽ bị thiếu mã quốc gia và bị tô xám/trắng trên bản đồ, gây sai lệch lớn về mặt thị giác đối với hai thị trường sản xuất phim quan trọng của Netflix.

#### 6.4.2. Quyết định kiến trúc: Xử lý ở bước nào trong Data Pipeline?

Nhóm quyết định thực hiện chuẩn hóa `country_code` **tại bước Data Normalization (`src/normalization.py`)** dựa trên các luận cứ kỹ thuật:

1. **Không xử lý ở bước Data Cleaning (`src/cleaning.py`)**:
   - Bước Cleaning có nhiệm vụ bảo toàn tính xác thực và nguồn gốc dữ liệu nguyên bản (*data provenance*). Một tác phẩm điện ảnh phát hành năm 1979 tại "Soviet Union" hay "West Germany" thì thông tin lịch sử của nó là Liên Xô hoặc Tây Đức. Nếu vội vã đổi tên chuỗi thành "Russia" hay "Germany" ngay từ cleaning, ta đã vô tình làm mất thông tin gốc mang giá trị lịch sử.
   - Tại Cleaning, trường `country` vẫn ở dạng chuỗi đa trị gộp (`"United States, West Germany"`), việc chuẩn hóa mã tại đây sẽ làm phức tạp hóa pipeline một cách không cần thiết.

2. **Không xử lý ở tầng Dashboard (`dashboard/app.py`)**:
   - Tầng UI chỉ nên đảm nhận hiển thị. Việc tính toán và mapping mã tại runtime sẽ làm chậm tốc độ tải của Dashboard và không thể tái sử dụng cho các notebook EDA hay mô hình học máy.

3. **Xử lý tại Data Normalization (`src/normalization.py`) là tối ưu nhất**:
   - `country_code` là một **thuộc tính làm giàu dữ liệu (Data Enrichment)** cho mô hình phân tích.
   - Tại Normalization, `country` đã được tách nguyên tử thành từng dòng (1NF), mỗi dòng là một tên quốc gia riêng biệt.
   - **Đạt được mục tiêu kép**: Bảng `bridge_country` vừa **bảo tồn tên gốc `country`** ("West Germany", "Soviet Union", "Turkey") để hiển thị trung thực trên bảng số liệu, tooltip và phân tích lịch sử; vừa **chuẩn hóa `country_code`** (`DEU`, `RUS`, `TUR`) để các công cụ bản đồ nhận diện và tô màu chính xác 100% diện tích các quốc gia.

#### 6.4.3. Giải pháp kỹ thuật: Chiến lược Tra cứu Kết hợp (Hybrid Lookup Strategy)

Giải pháp được triển khai thông qua hàm `get_country_code()` theo cơ chế 3 tầng kết hợp bộ nhớ đệm:

1. **Tầng 1 - Override Dictionary (`src/config.py`)**: Khai báo bảng ánh xạ thủ công `COUNTRY_CODE_OVERRIDE` dành riêng cho các quốc gia lịch sử và tên thông dụng, cho phép tra cứu với độ phức tạp $O(1)$ tuyệt đối nhanh và chuẩn xác.
2. **Tầng 2 - Exact ISO Lookup**: Dùng `pycountry.countries.lookup(country)` cho các quốc gia chuẩn.
3. **Tầng 3 - Fuzzy Search Fallback**: Dùng `pycountry.countries.search_fuzzy()` để bắt các biến thể tên gọi nhỏ.
4. **Bộ nhớ đệm (`@lru_cache`)**: Lưu cache kết quả của 122 quốc gia, giúp hàm xử lý hàng chục nghìn lượt tra cứu trong vòng chưa đầy $1$ miligiây.

```python
# Cấu hình tại src/config.py
COUNTRY_CODE_OVERRIDE: dict[str, str] = {
    # 1. Quốc gia lịch sử -> quy về vùng lãnh thổ hiện tại để vẽ bản đồ
    "West Germany": "DEU",   # Đức
    "East Germany": "DEU",   # Đức
    "Soviet Union": "RUS",   # Nga

    # 2. Tên thông dụng khác với tên chuẩn ISO 3166-1
    "Turkey": "TUR",         # ISO: Türkiye
    "Russia": "RUS",         # ISO: Russian Federation
    "Palestine": "PSE",      # ISO: Palestine, State of
    "Vatican City": "VAT",   # ISO: Holy See (Vatican City State)
}
```

```python
# Triển khai tại src/normalization.py
@lru_cache(maxsize=256)
def get_country_code(country: str | None) -> str | Any:
    """Chuyển tên quốc gia sang mã ISO 3166-1 alpha-3 phục vụ biểu đồ bản đồ."""
    if pd.isna(country) or not str(country).strip():
        return pd.NA

    country_str = str(country).strip()

    # 1. Kiểm tra bảng ghi đè thủ công
    if country_str in COUNTRY_CODE_OVERRIDE:
        return COUNTRY_CODE_OVERRIDE[country_str]

    # 2. Tra cứu chuẩn ISO chính thức
    try:
        return pycountry.countries.lookup(country_str).alpha_3
    except LookupError:
        pass

    # 3. Tra cứu tìm kiếm mờ (Fuzzy search)
    try:
        return pycountry.countries.search_fuzzy(country_str)[0].alpha_3
    except Exception:
        return pd.NA
```

#### 6.4.4. Bảng đối soát kết quả chuẩn hóa mã quốc gia

| Tên gốc trong dataset (`country`) | Phân loại vấn đề | Lý do kỹ thuật | Mã gán (`country_code`) | Lãnh thổ hiển thị trên bản đồ | Số tác phẩm bảo toàn |
|---|---|---|:---:|---|---:|
| **Turkey** | Name Mismatch | Đổi tên quốc tế thành *Türkiye* | `TUR` | Thổ Nhĩ Kỳ | 113 |
| **Russia** | Name Mismatch | Tên ISO là *Russian Federation* | `RUS` | Nga | 27 |
| **West Germany** | Historical Country | Mã ISO-3 hiện hành của Đức | `DEU` | Đức | 5 |
| **Soviet Union** | Historical Country | Thực thể kế thừa chính | `RUS` | Nga | 3 |
| **Palestine** | Name Mismatch | Tên ISO là *Palestine, State of* | `PSE` | Palestine | 1 |
| **East Germany** | Historical Country | Mã ISO-3 hiện hành của Đức | `DEU` | Đức | 1 |
| **Vatican City** | Name Mismatch | Tên ISO là *Holy See (Vatican...)* | `VAT` | Vatican | 1 |

Nhờ chiến lược này, **122 / 122 quốc gia (100%)** trong danh mục của Netflix đều được gán mã ISO-3 chuẩn xác, không có bất kỳ quốc gia hay tác phẩm nào bị bỏ sót khi trực quan hóa trên bản đồ.

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
