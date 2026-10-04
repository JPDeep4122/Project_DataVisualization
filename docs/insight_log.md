# Insight Log

## EDA — đã kiểm chứng

| ID | Chủ đề | Claim | Evidence | Caveat |
|---|---|---|---|---|
| EDA-01 | Annual additions | Số title được thêm tăng mạnh sau 2016, đạt đỉnh vào 2019 rồi giảm nhẹ trong 2020. | 2019: 2.016 title; 2020: 1.879 title, giảm 6,8%. | `date_added` không phải `release_year`; snapshot có thể không lưu đầy đủ lịch sử title đã bị gỡ. |
| EDA-02 | Content type | Movie chiếm phần lớn catalog trong phạm vi phân tích. | Movie: 5.134/7.294 (70,4%); TV Show: 2.160/7.294 (29,6%). | Cơ cấu catalog không phản ánh lượt xem hay mức độ yêu thích. |
| EDA-03 | Genre | International Movies là genre xuất hiện trên nhiều title nhất. | 2.343 title, tương đương 32,1% tổng title. | Một title có thể thuộc nhiều genre; tỷ lệ genre không cộng thành 100%. |
| EDA-04 | Genre | Dramas và Comedies cũng là hai nhóm lớn trong catalog. | Dramas: 2.013 title; Comedies: 1.375 title. | Genre có thể chồng lấp và phụ thuộc taxonomy của nguồn. |
| EDA-05 | Country | United States đứng đầu số title có liên quan, cách xa India và United Kingdom. | United States: 3.053; India: 941; United Kingdom: 685. | Country là quan hệ nhiều-nhiều; không diễn giải thành thị phần sản xuất. |
| EDA-06 | Country quality | Phân tích country chưa bao phủ toàn bộ catalog. | 6.822/7.294 title có country; 472 title (6,5%) thiếu country. | Các xếp hạng country có thể bị ảnh hưởng bởi dữ liệu thiếu. |
| EDA-07 | Rating | TV-MA và TV-14 áp đảo cơ cấu rating. | 4.543/7.290 title có rating, tương đương 62,3%. | Hệ thống rating khác nhau theo thị trường; có 4 title thiếu rating. |
| EDA-08 | Monthly additions | Tháng 11/2019 là tháng có nhiều additions nhất. | 255 title được thêm trong 2019-11. | Đây là một điểm cực đại quan sát được, chưa đủ để kết luận nguyên nhân. |

## Model / forecast — chờ thực hiện

Các claim về độ chính xác mô hình và forecast 12 tháng chỉ được bổ sung sau khi
hoàn thành time-based train/test và tính MAE, RMSE, R².
