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
| EDA-09 | Trend contribution | Movie là nhóm đóng góp chính cho giai đoạn tăng 2016–2019; mức giảm năm 2020 chủ yếu đến từ Movie. | 2016–2019 tăng 1.587 title: Movie +1.171 (73,8%), TV Show +416 (26,2%). Từ 2019 sang 2020: Movie -140, TV Show +3. | Đây là phân rã đóng góp trong dataset, không chứng minh nguyên nhân kinh doanh hay quan hệ nhân quả. |

## Storytelling tổng hợp

Netflix mở rộng mạnh catalog trong giai đoạn 2016–2019, khi số nội dung được thêm
tăng từ 429 lên 2.016 title. Movie đóng góp 1.171/1.587 title tăng thêm (73,8%),
cho thấy đây là thành phần chính của xu hướng tăng trong dữ liệu. Năm 2020, tổng
additions giảm 6,8% xuống 1.879 title; phần giảm gần như hoàn toàn đến từ Movie
(-140), trong khi TV Show vẫn ổn định (+3).

Không diễn giải sự thay đổi này thành tác động của COVID-19, chiến lược kinh doanh,
nhu cầu người xem hoặc doanh thu vì dataset không chứa các biến để kiểm chứng
những nguyên nhân đó.

## Model / forecast — đã kiểm chứng

| ID | Claim | Evidence | Caveat |
|---|---|---|---|
| MODEL-01 | Linear Regression nhận diện xu hướng tăng dài hạn nhưng chưa mô tả tốt biến động từng tháng của năm 2020. | MAE = 16,7361; RMSE = 23,7119; R² = -0,0828 trên tập test 2020. | R² âm cho thấy mô hình chỉ nên được xem là baseline; target có biến động mà biến thời gian đơn lẻ không giải thích được. |
| MODEL-02 | Đường xu hướng fit trên toàn bộ dữ liệu tăng trung bình khoảng 1,81 title mỗi tháng. | Hệ số `month_index` = 1,8083 khi fit 120 tháng từ 2011–2020. | Đây là xu hướng tuyến tính trung bình, không phải mức tăng đều trong từng tháng. |
| MODEL-03 | Forecast 12 tháng tăng từ khoảng 170 lên 190 title/tháng. | Tháng 01/2021: 170,19; tháng 12/2021: 190,08. | Forecast là ngoại suy từ snapshot đến hết 2020, không phải actual 2021 hay dự báo chính thức của Netflix. |
