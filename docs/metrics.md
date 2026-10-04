# Metric Dictionary — EDA và Forecast

## 1. Phạm vi và nguồn dữ liệu

- Phạm vi phân tích: `date_added` từ `2011-01-01` đến `2020-12-31`.
- Dataset phân tích chính: `data/normalized/dim_title.csv`.
- Grain của `dim_title`: một dòng cho một Netflix title (`show_id`).
- Số title đã validation: **7.294**.
- Dữ liệu thể loại và quốc gia lấy từ hai bảng bridge nhiều-nhiều.
- Dữ liệu chuỗi thời gian lấy từ `fact_monthly_addition.csv`, gồm 120 tháng liên tục.

> Số 7.294 là số liệu authoritative sau cleaning/normalization và khớp với
> `data/validation_report.json`. Mọi metric EDA sử dụng dữ liệu normalized, không
> dùng trực tiếp kết quả audit thô.

## 2. Metric definitions

| Metric | Định nghĩa | Grain / nhóm | Lưu ý |
|---|---|---|---|
| Total titles | `COUNT DISTINCT dim_title.show_id` | Toàn scope | Baseline denominator; hiện bằng 7.294 |
| Annual additions | `COUNT DISTINCT show_id` theo năm của `date_added` | Năm thêm | Không phải năm phát hành |
| Monthly additions | `COUNT DISTINCT show_id` theo tháng của `date_added` | Tháng thêm | Có đủ tháng 0; là target forecast |
| Content type count | `COUNT DISTINCT show_id` theo `type` | Movie / TV Show | Tổng hai nhóm bằng Total titles |
| Content type share | Content type count / Total titles | Movie / TV Show | Tỷ lệ toàn giai đoạn |
| Content type share by year | Type count trong năm / Annual additions của năm | Năm × type | Dùng cho 100% stacked chart |
| Content type count by year | `COUNT DISTINCT show_id` theo năm và `type` | Năm × type | Dùng để phân rã nhóm đóng góp vào xu hướng tăng/giảm |
| Genre title count | `COUNT DISTINCT show_id` theo `bridge_genre.genre` | Genre | Một title có nhiều genre |
| Genre penetration | Genre title count / Total titles | Genre | Các tỷ lệ không cộng thành 100% |
| Country title count | `COUNT DISTINCT show_id` theo `bridge_country.country` | Country | Một title có nhiều country |
| Country penetration | Country title count / Total titles | Country | Không diễn giải là market share |
| Country coverage | Số title xuất hiện trong `bridge_country` / Total titles | Toàn scope | Hiện 93,5%; 472 title thiếu country |
| Rating title count | `COUNT DISTINCT show_id` theo `rating` | Rating | Null được báo cáo riêng |
| Rating share | Rating title count / số title có rating | Rating | Hiện có 7.290 title có rating |
| Rating share by year | Rating count / số title có rating trong năm | Năm × rating | Dùng cho heatmap |

## 3. Quy tắc chống double-count

1. Metric title luôn dùng `COUNT DISTINCT show_id`.
2. Không cộng số lượng giữa các genre hoặc country để suy ra tổng title.
3. Khi join bảng bridge với `dim_title`, phải aggregate về `show_id` hoặc nhóm
   phân tích trước khi tính tổng.
4. `SUM(fact_monthly_addition.monthly_additions)` phải bằng Total titles.
5. Tỷ lệ rating loại null khỏi denominator và phải công bố số null.

## 4. Thiết kế và kết quả model

- Target: `monthly_additions`.
- Feature MVP: `month_index` từ 0 đến 119.
- Train: tháng thuộc 2011–2019.
- Test: tháng thuộc 2020.
- Evaluation: MAE, RMSE và R² trên tập test.
- Forecast horizon: 12 tháng sau 31/12/2020; đây là ngoại suy, không phải actual 2021.

### Kết quả trên tập test năm 2020

| Metric | Giá trị | Diễn giải |
|---|---:|---|
| MAE | 16,7361 | Sai số tuyệt đối trung bình khoảng 17 title/tháng |
| RMSE | 23,7119 | Một số tháng có sai số lớn hơn mức trung bình |
| R² | -0,0828 | Mô hình chưa mô tả tốt biến động theo tháng trong năm 2020 |

Mô hình train trên 2011–2019 có phương trình:

`monthly_additions = -47,4062 + 1,8233 × month_index`

Sau khi đánh giá, mô hình được fit lại trên toàn bộ 120 tháng để tạo forecast:

`monthly_additions = -46,8105 + 1,8083 × month_index`

Forecast tăng từ khoảng **170 title trong tháng 01/2021** lên khoảng **190 title
trong tháng 12/2021**. Đây là đường ngoại suy xu hướng, không phải số liệu thực tế
của năm 2021 hay dự báo chính thức của Netflix.
