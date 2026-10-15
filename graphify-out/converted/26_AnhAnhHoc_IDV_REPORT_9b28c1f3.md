<!-- converted from 26_AnhAnhHoc_IDV_REPORT.docx -->

TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT TP.HCM
KHOA CÔNG NGHỆ THÔNG TIN
BỘ MÔN HỆ THỐNG THÔNG TIN



BÁO CÁO CUỐI KỲ
HỌC PHẦN: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN

Đề tài:
PHÂN TÍCH XU HƯỚNG MOVIE VÀ TV SHOW TRÊN NETFLIX TRONG GIAI ĐOẠN 2011-2020


NHÓM SINH VIÊN THỰC HIỆN
LÊ ĐẶNG HOÀNG ANH – 24162006
NGUYỄN ĐỨC HỌC – 24162039
NGUYỄN VĂN HOÀNG ANH – 24133004



GIÁO VIÊN HƯỚNG DẪN
THS. ĐOÀN MINH TRÍ
KHÓA 2024-2028
NHẬN XÉT CỦA GIẢNG VIÊN
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
.....................................................................................................................................
TP. Hồ Chí Minh, ngày 9 tháng 10 năm 2026
Giảng viên ký tên


LỜI CẢM ƠN
Lời đầu tiên, nhóm chúng em xin gửi lời cảm ơn chân thành đến Ban Giám hiệu Trường Đại học Công nghệ Kỹ thuật TP.HCM, quý Thầy, Cô Khoa Công nghệ Thông tin và Bộ môn Hệ thống Thông tin đã tạo điều kiện học tập, cung cấp những kiến thức nền tảng và môi trường thuận lợi để chúng em có thể hoàn thành học phần Tương tác dữ liệu trực quan.
Đặc biệt, nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc đến ThS. Đoàn Minh Trí, giảng viên hướng dẫn học phần, đã tận tình hướng dẫn, định hướng và đóng góp nhiều ý kiến quý báu trong quá trình thực hiện đề tài. Những kiến thức và phương pháp được truyền đạt trong quá trình học đã giúp nhóm có cơ sở để tiếp cận bài toán một cách có hệ thống, từ thu thập và tiền xử lý dữ liệu, kiểm tra và chuẩn hóa dữ liệu, đến phân tích, khai phá insight, xây dựng mô hình dự báo và trực quan hóa kết quả.
Trong quá trình thực hiện đề tài “Phân tích xu hướng Movie và TV Show trên Netflix trong giai đoạn 2011–2020”, nhóm đã có cơ hội vận dụng các kiến thức đã học vào một bài toán dữ liệu thực tế. Thông qua quá trình này, nhóm từng bước rèn luyện kỹ năng xử lý dữ liệu bằng Python, thiết kế dữ liệu phục vụ phân tích, xây dựng các biểu đồ trực quan, rút trích insight từ dữ liệu và thử nghiệm mô hình Linear Regression để mô tả và dự báo xu hướng số lượng nội dung được bổ sung theo thời gian.
Mặc dù nhóm đã cố gắng hoàn thành báo cáo với tinh thần nghiêm túc và trách nhiệm, do thời gian thực hiện, kiến thức và kinh nghiệm thực tế còn hạn chế, báo cáo khó tránh khỏi những thiếu sót. Nhóm chúng em rất mong nhận được những nhận xét và góp ý từ Thầy để có thể tiếp tục hoàn thiện kiến thức, kỹ năng cũng như phương pháp thực hiện các đề tài dữ liệu trong tương lai.
Nhóm chúng em xin kính chúc Thầy cùng quý Thầy, Cô luôn mạnh khỏe, hạnh phúc và thành công trong công tác giảng dạy và nghiên cứu.
TP. Hồ Chí Minh, ngày 9 tháng 10 năm 2026
Nhóm sinh viên thực hiện


MỤC LỤC
NHẬN XÉT CỦA GIẢNG VIÊN	I
LỜI CẢM ƠN	II
MỤC LỤC	III
DANH SÁCH HÌNH ẢNH	VI
DANH SÁCH BẢNG	VII
CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI	1
1.1. Lý do chọn đề tài	1
1.2. Mục tiêu đề tài	1
1.3. Đối tượng và phạm vi nghiên cứu	2
1.3.1. Đối tượng nghiên cứu	2
1.3.2. Phạm vi dữ liệu	2
1.3.3. Phạm vi phân tích và giới hạn	2
1.4. Câu hỏi nghiên cứu	3
CHƯƠNG 2. THU THẬP VÀ TIỀN XỬ LÝ DỮ LIỆU	4
2.1. THU THẬP DỮ LIỆU	4
2.1.1. Tổng quan dữ liệu	4
2.1.2. Xác định phạm vi nghiên cứu	5
2.2. KIỂM TRA VÀ ĐÁNH GIÁ DỮ LIỆU BAN ĐẦU	6
2.2.1. Đọc và kiểm tra cấu trúc dữ liệu	6
2.2.2. Kiểm tra khóa chính	7
2.2.3. Kiểm tra bản ghi trùng lặp	7
2.2.4. Kiểm tra thuộc tính đa trị	8
2.2.5. Kiểm tra dữ liệu ngày tháng	10
2.2.6. Kiểm tra phạm vi dữ liệu	12
2.3. LÀM SẠCH DỮ LIỆU	13
2.3.1. Chuẩn hóa dữ liệu dạng chuỗi	13
2.3.2. Chuẩn hóa date_added	14
2.3.3. Chuẩn hóa release_year	14
2.3.4. Chuẩn hóa duration	14
2.3.5. Xử lý dữ liệu thiếu	15
2.4. CHUẨN HÓA DỮ LIỆU	15
2.4.1. Mục đích chuẩn hóa	15
2.4.2. Mô hình dữ liệu sau chuẩn hóa	16
2.5. VALIDATION SAU CHUẨN HÓA	19
2.5.1. Kiểm tra cấu trúc các bảng	20
2.5.2. Kiểm tra khóa chính	21
2.5.3. Kiểm tra khóa ngoại	21
2.5.4. Kiểm tra số lượng ngày và tháng	22
2.5.5. Kiểm tra giá trị monthly_additions và month_index	22
2.5.6. Kiểm tra tổng số lượng title	23
2.5.7. Kiểm tra lại phạm vi thời gian của dim_title	23
2.5.8. Kết quả validation	24
2.6. KẾT QUẢ SAU TIỀN XỬ LÝ	25
2.7. KẾT LUẬN CHƯƠNG	27
CHƯƠNG 3. PHÂN TÍCH DỮ LIỆU	28
3.1. Tổng quan phân tích	28
3.2. Phân tích xu hướng nội dung được thêm mới theo năm	28
3.3. Phân tích cơ cấu Movie và TV Show	29
3.4. Phân tích độ phủ của thể loại (genre) và quốc gia (country)	31
3.5. Phân tích cơ cấu phân loại độ tuổi	34
3.6. Kết luận chương	36
CHƯƠNG 4. KHAI PHÁ DỮ LIỆU	37
4.1. Tổng hợp các insight	37
4.2. Diễn biến và phân tích biến động trong dữ liệu	37
4.3. Giới hạn dữ liệu	37
CHƯƠNG 5. XÂY DỰNG MÔ HÌNH DỰ BÁO	38
5.1. Mục tiêu xây dựng mô hình	38
5.2. Import thư viện	38
5.3. Đọc dữ liệu	38
5.4. Xác định biến đầu vào và biến cần dự báo	39
5.5. Huấn luyện mô hình	39
5.6. Dự báo 9 tháng tiếp theo	40
5.7. Thu thập dữ liệu thực tế năm 2021	41
5.8. Tính phần sai khác và các chỉ số đánh giá	42
5.9. Biểu đồ xu hướng, đường hồi quy và dự báo	42
5.10. Residual Plot	44
5.11. Nhận xét	45
5.12. Kết luận	45
CHƯƠNG 6. XÂY DỰNG DASHBOARD	46
6.1. Mục tiêu và phạm vi xây dựng dashboard	46
6.2. Kiến trúc thông tin và bố cục dashboard	46
6.3. Trang Tổng quan	47
6.4. Trang Xu hướng nội dung	47
6.5. Trang Phân bố nội dung theo quốc gia	48
6.6. Trang Đặc điểm nội dung	49
6.7. Trang Đánh giá mô hình dự báo	50
6.8. Kết luận chương	51
KẾT LUẬN	53
TÀI LIỆU THAM KHẢO	55


DANH SÁCH HÌNH ẢNH
Hình 2.1 Một phần dữ liệu gốc trong tệp netflix_titles.csv	6
Hình 2.2 Kết quả kiểm tra cấu trúc dữ liệu	6
Hình 2.3 Kết quả kiểm tra khóa chính	7
Hình 2.4 Kết quả kiểm tra trùng lặp	7
Hình 2.5 Kết quả kiểm tra thuộc tính đa trị	8
Hình 2.6 Kết quả kiểm tra các thuộc tính đa trị	9
Hình 2.7 Kết quả kiểm tra thủ công các thuộc tính đa trị	10
Hình 2.8 Kết quả kiểm tra dữ liệu ngày tháng khi không có format=”mixed”	11
Hình 2.9 Kết quả kiểm tra dữ liệu ngày tháng với format="mixed"	12
Hình 2.10 Kết quả kiểm tra phạm vi dữ liệu	13
Hình 2.11 Mô hình dữ liệu gồm bảy bảng sau chuẩn hóa	16
Hình 2.12 Lược đồ dim_title	16
Hình 2.13 Lược đồ dim_date	17
Hình 2.14 Lược đồ bridge_genre	17
Hình 2.15 Lược đồ bridge_country	18
Hình 2.16 Lược đồ bridge_director	18
Hình 2.17 Lược đồ bridge_actor	19
Hình 2.18 Lược đồ fact_monthly_addition	19
Hình 2.19 Pipeline xử lý dữ liệu của đề tài	26
Hình 3.1. Số title được thêm vào Netflix từ năm 2011-2020	29
Hình 3.2. Tỷ trọng Movie và TV Show giai đoạn 2011-2020	31
Hình 3.3. Top 10 thể loại có số nội dung nhiều nhất	32
Hình 3.4. Top 10 quốc gia có số nội dung nhiều nhất	33
Hình 3.5. Tỷ trọng rating giao đoạn 2011-2020	35
Hình 5.1. Biểu đồ Xu hướng, đường hồi quy và dự báo	43
Hình 5.2. Biểu đồ Residual trên tập train 2011-2020	44
Hình 6.1. Cấu trúc điều hướng và bố cục chung của dashboard	46
Hình 6.2. Trang Tổng quan của dashboard	47
Hình 6.3. Trang Xu hướng nội dung và hierarchy drill-down	48
Hình 6.4. Trang Phân bố nội dung theo quốc gia	49
Hình 6.5. Trang Đặc điểm nội dung	50
Hình 6.6. Trang Đánh giá mô hình dự báo	51


# DANH SÁCH BẢNG
Bảng 2.1 Mô tả các trường dữ liệu trong bộ dữ liệu Netflix	4
Bảng 2.2 Bảng ví dụ minh họa về dữ liệu chứa thuộc tính đa trị	15
Bảng 2.3 Bảng danh sách khóa chính của các bảng dữ liệu sau chuẩn hóa	21
Bảng 2.4 Bảng tổng hợp kết quả kiểm tra toàn vẹn dữ liệu sau chuẩn hóa	24
Bảng 2.5 Bảng thống kê kết quả sau quá trình tiền xử lý dữ liệu	26
Bảng 5.1 Kết quả dự báo số Title thêm vào từ 01/2021 - 09/2021	41




# TỔNG QUAN ĐỀ TÀI
## Lý do chọn đề tài
Trong bối cảnh dữ liệu ngày càng được sử dụng rộng rãi để hỗ trợ phân tích và ra quyết định, việc chuyển đổi dữ liệu thô thành thông tin trực quan và dễ hiểu trở thành một nội dung quan trọng trong quá trình khai thác dữ liệu. Đối với lĩnh vực phim ảnh và chương trình truyền hình, một tập dữ liệu có thể chứa nhiều thông tin khác nhau như loại nội dung, thể loại, quốc gia sản xuất, đạo diễn, diễn viên, phân loại độ tuổi, năm phát hành và thời điểm nội dung được bổ sung vào nền tảng.
Netflix là một nền tảng có danh mục nội dung đa dạng, do đó dữ liệu về các Movie và TV Show trên Netflix là một nguồn dữ liệu phù hợp để áp dụng các phương pháp xử lý, phân tích và trực quan hóa dữ liệu. Bộ dữ liệu được nhóm sử dụng là Netflix Movies and TV Shows, trong đó tệp netflix_titles.csv chứa 8.807 bản ghi và 12 trường dữ liệu liên quan đến nội dung trên Netflix.
Một vấn đề đáng chú ý trong quá trình nghiên cứu là date_added và release_year thể hiện hai khía cạnh thời gian khác nhau. release_year là năm phát hành của nội dung, trong khi date_added là thời điểm nội dung được thêm vào Netflix. Do đề tài tập trung nghiên cứu xu hướng bổ sung nội dung lên nền tảng, nhóm lựa chọn date_added làm cơ sở để xác định phạm vi thời gian thay vì release_year.
Bên cạnh đó, dữ liệu ban đầu còn tồn tại những đặc điểm cần được xử lý trước khi phân tích, chẳng hạn như các thuộc tính đa trị trong cast, country, director và listed_in, dữ liệu ngày tháng chưa được chuẩn hóa và trường duration có cách biểu diễn khác nhau giữa Movie và TV Show. Vì vậy, đề tài không chỉ tập trung vào việc tạo biểu đồ mà còn bao gồm toàn bộ quá trình từ kiểm tra, làm sạch, chuẩn hóa, kiểm tra tính toàn vẹn của dữ liệu đến phân tích và trực quan hóa.
Từ những lý do trên, nhóm lựa chọn đề tài “Phân tích xu hướng Movie và TV Show trên Netflix trong giai đoạn 2011–2020” nhằm vận dụng các kiến thức của học phần vào một bài toán dữ liệu cụ thể, đồng thời xây dựng một quy trình phân tích có tính hệ thống từ dữ liệu nguồn đến kết quả trực quan.
## Mục tiêu đề tài
Đề tài hướng đến việc phân tích và trực quan hóa dữ liệu Movie và TV Show được bổ sung trên Netflix trong giai đoạn 2011–2020, từ đó nhận diện các xu hướng và đặc điểm nổi bật của danh mục nội dung dựa trên những thuộc tính có trong bộ dữ liệu.
Để đạt được mục tiêu này, nhóm thực hiện một quy trình gồm các bước chính: thu thập và kiểm tra dữ liệu, làm sạch và chuẩn hóa dữ liệu, xây dựng dữ liệu phục vụ phân tích, khám phá dữ liệu, rút trích insight, xây dựng mô hình dự báo và trình bày kết quả bằng dashboard.

## Đối tượng và phạm vi nghiên cứu
### Đối tượng nghiên cứu
Đối tượng nghiên cứu của đề tài là dữ liệu về các Movie và TV Show được bổ sung trên nền tảng Netflix, tập trung vào các đặc trưng có trong bộ dữ liệu như loại nội dung, tên nội dung, đạo diễn, diễn viên, quốc gia, thời điểm được thêm vào Netflix, năm phát hành, phân loại độ tuổi, thời lượng và thể loại.
Trong quá trình phân tích, nhóm tập trung vào số lượng nội dung được bổ sung và mối liên hệ của số lượng này với một số thuộc tính mô tả của nội dung. Đề tài không sử dụng dữ liệu về lượt xem, doanh thu hay hành vi người dùng để đánh giá mức độ phổ biến của nội dung.
### Phạm vi dữ liệu
Nguồn dữ liệu chính được sử dụng trong đề tài là tệp netflix_titles.csv, thuộc bộ dữ liệu Netflix Movies and TV Shows. Dữ liệu ban đầu gồm 8.807 bản ghi và 12 trường dữ liệu.
Phạm vi thời gian nghiên cứu được xác định từ ngày 01/01/2011 đến ngày 31/12/2020, dựa trên trường date_added. Việc sử dụng date_added nhằm đảm bảo phạm vi nghiên cứu phản ánh thời điểm nội dung được bổ sung lên Netflix thay vì năm phát hành của nội dung.
Các bản ghi có thời điểm nằm ngoài giai đoạn nghiên cứu không được xem là dữ liệu sai mà chỉ nằm ngoài phạm vi của đề tài. Những bản ghi không xác định được date_added hợp lệ cũng không được tự ý suy diễn để đưa vào chuỗi thời gian.
### Phạm vi phân tích và giới hạn
Đề tài tập trung phân tích các nội dung sau:
Xu hướng số lượng nội dung được thêm vào Netflix theo thời gian.
Cơ cấu và sự thay đổi giữa Movie và TV Show.
Phân bố nội dung theo thể loại và quốc gia.
Cơ cấu phân loại độ tuổi.
Một số insight liên quan đến sự thay đổi của danh mục nội dung.
Dự báo số lượng nội dung được bổ sung theo tháng bằng mô hình Linear Regression.
Do dữ liệu chủ yếu mô tả thông tin về danh mục nội dung, đề tài không đưa ra kết luận về lượt xem, doanh thu, mức độ yêu thích hoặc nguyên nhân kinh doanh thực tế của các biến động. Chẳng hạn, dữ liệu cho thấy số lượng nội dung giảm trong năm 2020 và phần giảm này chủ yếu đến từ Movie, nhưng dữ liệu hiện có không đủ để khẳng định nguyên nhân sâu xa của biến động đó.
## Câu hỏi nghiên cứu
Dựa trên mục tiêu và phạm vi của đề tài, nhóm đặt ra các câu hỏi nghiên cứu sau:
Số lượng nội dung được thêm vào Netflix thay đổi như thế nào trong giai đoạn 2011–2020?
Movie và TV Show có tỷ trọng như thế nào trong danh mục nội dung, và sự thay đổi của hai loại nội dung này ảnh hưởng như thế nào đến xu hướng chung?
Những thể loại nào xuất hiện nhiều nhất trong danh mục nội dung Netflix trong giai đoạn nghiên cứu?
Những quốc gia nào có số lượng nội dung được bổ sung nhiều nhất?
Cơ cấu phân loại độ tuổi của các nội dung thay đổi như thế nào theo thời gian?
Các đạo diễn và diễn viên xuất hiện như thế nào trong danh mục nội dung, và dữ liệu có thể cung cấp những insight nào về sự phân bố của họ?
Có thể sử dụng xu hướng số lượng nội dung được bổ sung theo tháng để xây dựng mô hình Linear Regression và dự báo số lượng nội dung trong các tháng tiếp theo hay không?
Các câu hỏi trên được sử dụng làm định hướng xuyên suốt quá trình thực hiện đề tài, từ việc xác định phạm vi dữ liệu, lựa chọn phương pháp tiền xử lý, thiết kế dữ liệu phục vụ phân tích cho đến xây dựng insight, mô hình dự báo và dashboard.


# THU THẬP VÀ TIỀN XỬ LÝ DỮ LIỆU
## THU THẬP DỮ LIỆU
### Tổng quan dữ liệu
Bộ dữ liệu chính được sử dụng trong đề tài có tên “Netflix Movies and TV Shows”, được lưu dưới dạng tệp CSV và chứa thông tin về các bộ phim và chương trình truyền hình trên nền tảng Netflix.
Bộ dữ liệu được nhóm lựa chọn vì có các thuộc tính phù hợp với mục tiêu của đề tài “Phân tích xu hướng Movie và TV Show trên Netflix trong giai đoạn 2011–2020”. Dữ liệu cung cấp các thông tin liên quan đến loại nội dung, tên nội dung, đạo diễn, diễn viên, quốc gia sản xuất, ngày được thêm vào Netflix, năm phát hành, nhãn phân loại độ tuổi, thời lượng và thể loại.
Trong báo cáo, nhóm sử dụng netflix_titles.csv làm nguồn dữ liệu chính. Dataset ban đầu gồm 8.807 bản ghi và 12 trường dữ liệu.
Bảng 2.1 Mô tả các trường dữ liệu trong bộ dữ liệu Netflix
| Trường | Ý nghĩa | Kiểu dữ liệu |
| --- | --- | --- |
| show_id | Mã định danh của nội dung | String |
| type | Loại nội dung: Movie hoặc TV Show | String |
| title | Tên phim/chương trình | String |
| director | Đạo diễn | String |
| cast | Danh sách diễn viên | String |
| country | Quốc gia sản xuất | String |
| date_added | Ngày nội dung được thêm vào Netflix | Date/String |
| release_year | Năm phát hành nội dung | Integer |
| rating | Nhãn phân loại độ tuổi | String |
| duration | Thời lượng phim hoặc số mùa | String |
| listed_in | Danh sách thể loại | String |
| description | Mô tả nội dung | String |

Một điểm cần phân biệt trong quá trình xử lý dữ liệu là release_year và date_added có ý nghĩa khác nhau. release_year thể hiện năm phát hành của nội dung, trong khi date_added thể hiện thời điểm nội dung được thêm vào Netflix. Do đề tài nghiên cứu xu hướng nội dung được bổ sung vào nền tảng trong giai đoạn 2011–2020, nhóm sử dụng date_added làm cơ sở chính để xác định phạm vi thời gian nghiên cứu.
### Xác định phạm vi nghiên cứu
Dataset ban đầu chứa các nội dung được thêm vào Netflix trong nhiều năm khác nhau. Trong khi đó, đề tài chỉ tập trung nghiên cứu giai đoạn 2011–2020. Nhóm không sử dụng release_year để lọc phạm vi vì trường này thể hiện năm nội dung được phát hành, không phải năm nội dung được thêm vào Netflix.
Cuối cùng, nhóm xác định phạm vi nghiên cứu là các nội dung có date_added nằm trong khoảng từ ngày 01/01/2011 đến ngày 31/12/2020. Quy tắc này được sử dụng thống nhất trong các bước tiền xử lý, phân tích, khai phá dữ liệu và xây dựng mô hình dự báo ở các chương tiếp theo.
## KIỂM TRA VÀ ĐÁNH GIÁ DỮ LIỆU BAN ĐẦU
### Đọc và kiểm tra cấu trúc dữ liệu
Nhóm sử dụng Python với thư viện Pandas để xây dựng đọc và kiểm tra sơ bộ dữ liệu. Quá trình kiểm tra bao gồm: số lượng dòng và cột, tên các trường, kiểu dữ liệu, bản ghi trùng lặp, khóa định danh, thuộc tính đa trị, trường ngày tháng, phạm vi thời gian.
Kết quả kiểm tra như sau:

Hình 2.1 Một phần dữ liệu gốc trong tệp netflix_titles.csv
Có thể thấy dữ liệu chưa bị sai lệch so với các mô tả ban đầu, kiểm tra sâu hơn về cấu trúc của dữ liệu ta được kết quả như sau:

Hình 2.2 Kết quả kiểm tra cấu trúc dữ liệu
Toàn bộ các trường dữ liệu đa phần được lưu dưới dạng chuỗi, duy nhất chỉ có release_year là thuộc loại số nguyên. Dựa trên ý nghĩa của các trường dữ liệu thì mọi thứ đều hợp lý. Nhưng hiện tại vẫn chưa thể kết luận rõ cấu trúc thực tế của các trường dữ liệu khi sử dụng chuỗi. Nó có thể là một đoạn văn bản, một loại chuỗi ký tự, chuỗi ngày tháng hay một danh sách các gồm các thành phần ngăn cách nhau bởi các dấu phẩy. Vì vậy nhóm sẽ đào sâu hơn về cấu trúc ở phần phân tích dữ liệu cụ thể phía sau.
### Kiểm tra khóa chính
def audit_key(df: pd.DataFrame, key_column: str | None = None) -> dict[str, dict]:
"""Kiểm tra tính chính xác của trường key_column"""
if not key_column:
key_column = df.columns[df.columns.str.contains(r"id$", case=False, regex=True)].tolist()
if not key_column:
print("Dữ liệu đã cho không có trường định danh")
return
if len(key_column) > 1:
print("Dữ liệu đã cho có hơn 1 cột định danh, lấy cột định danh đầu tiên.")
key_column = key_column[0]

return {
"key": key_column,
"null_count": int(df[key_column].isna().sum()),
"duplicate_count": int(df[key_column].duplicated().sum()),
"unique_count": int(df[key_column].nunique())
}
Nhóm đã xây dựng hàm audit_key() này để kiểm tra trường dữ liệu key_column xem nó có thật sự là khóa chính của dữ liệu này hay không. Bằng cách đếm số giá trị lặp và số giá trị null, ta có thể kết luận một trường có thật sự là khóa chính cho bảng đó hay không. Với số giá trị lặp, số giá trị null đều bằng 0 thì các giá trị này có thể dùng làm định danh cho các dòng trong bộ dữ liệu tương ứng và đây là kết quả:

Hình 2.3 Kết quả kiểm tra khóa chính
Có thể thấy là show_id chính là khóa chính của bộ dữ liệu này như đã dự đoán. Do đó sẽ giữ nguyên và không cần xử lý gì thêm.
### Kiểm tra bản ghi trùng lặp
def audit_duplicate(df: pd.DataFrame) -> int:
"""Kiểm tra số dòng bị trùng hoàn toàn trong DataFrame."""

return int(df.duplicated().sum())
Nhóm sử dụng hàm audit_duplicate() để kiểm tra số dòng bị trùng trong bộ dữ liệu và nhận được kết quả sau:

Hình 2.4 Kết quả kiểm tra trùng lặp
Cho thấy các dòng đều hoàn toàn khác nhau và đây là một tính hiệu đáng mừng cho thấy bộ dữ liệu đã được thu thập một cách đúng đắn và không bị lặp.
### Kiểm tra thuộc tính đa trị
def audit_multivalue(df: pd.DataFrame) -> dict[str, Any]:
"""Kiểm tra các cột chứa nhiều giá trị trong cùng một cell."""
result = {}
for column in list(df.columns):
series = df[column].dropna().astype(str)
multi_count = int(series.str.contains(",", regex=False).sum())
value_counts = series.str.split(",").str.len()
avg_values_per_row = float(value_counts.mean())
if avg_values_per_row != 1:
result[column] = {
"non_null_count": int(series.count()),
"multivalue_rows": multi_count,
"single_value_rows": int((value_counts == 1).sum()),
"max_values_per_row": int(value_counts.max()),
"average_values_per_row": avg_values_per_row
}
return result
Nhóm đã xây dựng hàm audit_multivalue() như này để kiểm tra các trường dữ liệu kiểu chuỗi trong bộ dữ liệu có nhiều giá trị được phân cách bằng dấu phẩy như nghi vấn đặt ra ban đầu hay không và sau đây là kết quả nhận được:

Hình 2.5 Kết quả kiểm tra thuộc tính đa trị
Sau khi kiểm tra, nhóm xác định bốn trường cast, country, director và listed_in là các thuộc tính đa trị thực sự. Các trường này có thể chứa nhiều giá trị trong cùng một bản ghi và các giá trị được phân cách bằng dấu phẩy.
Đối với date_added, description và title, mặc dù một số giá trị cũng chứa dấu phẩy nhưng dấu phẩy không mang ý nghĩa phân tách nhiều giá trị. Ví dụ, date_added có thể có dạng “November 25, 2020”, trong khi description và title có thể chứa dấu phẩy như một phần nội dung văn bản. Vì vậy, nhóm không xem các trường này là thuộc tính đa trị và không thực hiện tách chúng thành các bảng trung gian.
Các trường dữ liệu khác như cast, country, director và listed_in thì đều có thể mang giá trị đa trị theo đặc điểm của các bộ phim. Một bộ phim có thể có nhiều diễn viên đóng, sản xuất đa quốc gia, nhiều người đồng đạo diễn và thuộc nhiều thể loại khác nhau.
Để chắc chắn thì ta sẽ lần lượt kiểm tra 5 dòng đầu tiên của từng trường dữ liệu trong danh sách nghi vấn trên để xem nó có đúng thật là đa trị hay không và đây là kết quả:

Hình 2.6 Kết quả kiểm tra các thuộc tính đa trị
Kết quả cho thấy những dự đoán của nhóm là tương đối chính xác, chỉ có phần title, director, country sẽ cần phải xác minh thủ công và nhóm đã mở dataset lên và dễ dàng nhìn thấy các bản ghi sau:

Hình 2.7 Kết quả kiểm tra thủ công các thuộc tính đa trị
Đây là các bản ghi khác nhau nhưng cùng chứng minh một quan điểm về vấn đề thuộc tính đa trị mà nhóm đã nhắc đến. Để xử lý các thuộc tính đa trị này thì ta cần phải thiết kế chuẩn hóa thành các bảng trung gian và nhóm đã quyết định chuẩn hóa thành các bảng như sau bridge_genre, bridge_country, bridge_director, bridge_actor.
Trong đó:
bridge_genre phục vụ phân tích thể loại
bridge_country phục vụ phân tích quốc gia và bản đồ
bridge_director phục vụ phân tích đạo diễn
bridge_actor phục vụ phân tích diễn viên.
Việc bổ sung bridge_director và bridge_actor giúp nhóm có thể khai thác thêm các insight về mức độ xuất hiện của đạo diễn và diễn viên trong các nội dung thuộc phạm vi nghiên cứu.
### Kiểm tra dữ liệu ngày tháng
Trường date_added là trường quan trọng vì được sử dụng để xác định phạm vi nghiên cứu và xây dựng chuỗi thời gian. Nhóm cũng xây dựng một hàm để kiểm tra các trường dữ liệu có chữ date ở đầu nhưng rõ ràng thì trong bộ dữ liệu đang xét thì chỉ có date_added là có dạng ngày tháng nên ta sẽ chuẩn hóa nó về dạng pd.datetime thông qua hàm pd.to_datetime():

def audit_date(df: pd.DataFrame) -> dict[str, dict[str, Any]] | None:
"""Kiểm tra các cột ngày quan trọng."""
date_columns = df.columns[df.columns.str.contains(r"^date", case=False, regex=True)].tolist()
if not date_columns:
print("Dữ liệu đã cho không có trường ngày tháng")
return

result = {}
for date_cols in date_columns:
parsed = pd.to_datetime(df[date_cols], errors="coerce", format="mixed")
result[date_cols] = {
"original_dtype": str(df[date_cols].dtype),
"null_count": int(df[date_cols].isna().sum()),
"invalid_count": int(parsed.isna().sum() - df[date_cols].isna().sum()),
"min_date": (parsed.min().strftime("%Y-%m-%d") if parsed.notna().any() else None),
"max_date": (parsed.max().strftime("%Y-%m-%d") if parsed.notna().any() else None)
}

return result
Sau đây là kết quả:

Hình 2.8 Kết quả kiểm tra dữ liệu ngày tháng khi không có format=”mixed”
Kết quả kiểm tra cho thấy trường date_added có 8.797 giá trị có ngày hợp lệ và 10 giá trị NULL. Không có giá trị ngày tháng không hợp lệ sau khi sử dụng format="mixed" để cho phép Pandas xử lý các chuỗi ngày tháng có định dạng phù hợp nhưng có cách biểu diễn khác nhau.
Ở lần kiểm tra ban đầu, nhóm sử dụng pd.to_datetime() mà không chỉ định format="mixed", dẫn đến 88 giá trị ngày tháng hợp lệ bị chuyển thành NaT do cơ chế suy luận định dạng của bộ phân tích ngày tháng. Sau khi kiểm tra lại dữ liệu gốc, các giá trị này thực tế có dạng ngày hợp lệ, chẳng hạn “September 25, 2021”. Vì vậy, 88 giá trị này không được xem là dữ liệu lỗi và không bị loại bỏ.
Sau khi thay đổi phương pháp chuyển đổi sang format="mixed", kết quả audit xác nhận rằng dataset chỉ có 10 bản ghi thực sự thiếu date_added và không có bản ghi có ngày tháng không hợp lệ.

Hình 2.9 Kết quả kiểm tra dữ liệu ngày tháng với format="mixed"
Trong quá trình kiểm tra dữ liệu, nhóm phát hiện kết quả parse ban đầu cho thấy 88 giá trị date_added không chuyển đổi được sang datetime. Nhóm tiến hành kiểm tra trực tiếp các giá trị tương ứng trong dữ liệu nguồn và nhận thấy đây là các chuỗi ngày tháng hợp lệ, chủ yếu có dạng “Month Day, Year”. Nguyên nhân nằm ở phương pháp suy luận định dạng ngày tháng của hàm pd.to_datetime() khi không chỉ định format.
Nhóm thay đổi phương pháp chuyển đổi sang pd.to_datetime(..., format="mixed", errors="coerce") và thực hiện audit lại toàn bộ dữ liệu. Kết quả mới cho thấy 8.797 giá trị date_added hợp lệ, 10 giá trị NULL và không có giá trị ngày tháng không hợp lệ. Do đó, 88 giá trị trước đây bị đánh dấu là không parse được được xác định là dữ liệu hợp lệ và được giữ lại.
### Kiểm tra phạm vi dữ liệu
Dữ liệu thu thập các chương trình được thêm vào nền tảng Netflix từ 2008-2021 và đã được kiểm chứng trên nền tảng Kaggle, vấn đề duy nhất ở đây là trong phạm vi của đề tài là trong 10 năm từ 2011-2020 thì số lượng dữ liệu có đủ lớn hay không nên sẽ cần kiểm tra lại thông qua hàm sau:
def audit_scope(
df: pd.DataFrame,
start_year: int = 2011,
end_year: int = 2020
) -> dict[str, Any]:
"""
Kiểm tra phạm vi dữ liệu theo date_added.
Project hiện tại: 2011 <= year(date_added) <= 2020
"""
dates = pd.to_datetime(df["date_added"], errors="coerce", format="mixed")
years = dates.dt.year
in_scope = years.between(start_year, end_year)

return {
"scope_column": "date_added",
"start_year": start_year,
"end_year": end_year,
"total_rows": len(df),
"in_scope_rows": int(in_scope.sum()),
"out_of_scope_rows": int((~in_scope & years.notna()).sum()),
"missing_date_rows": int(years.isna().sum()),
"in_scope_percentage": float(in_scope.mean() * 100),
"out_of_scope_years": sorted(years[~in_scope & years.notna()].unique().tolist())
}
Kết quả của hàm trên như sau:

Hình 2.10 Kết quả kiểm tra phạm vi dữ liệu
Kết quả kiểm tra cho thấy dataset có 8.807 bản ghi, trong đó 7.294 bản ghi có date_added thuộc phạm vi nghiên cứu 2011–2020, chiếm 82,82% tổng số dữ liệu. Có 1.503 bản ghi có ngày hợp lệ nhưng nằm ngoài phạm vi nghiên cứu, thuộc các năm 2008, 2009, 2010 và 2021. Ngoài ra, có 10 bản ghi không có giá trị date_added.
Các bản ghi ngoài phạm vi không được xem là dữ liệu sai mà chỉ không thuộc câu hỏi nghiên cứu hiện tại. Do đó, các bản ghi này vẫn được giữ trong dữ liệu nguồn và dữ liệu sau cleaning, nhưng không được đưa vào các bảng phân tích thuộc phạm vi 2011–2020. Đối với 10 bản ghi không có date_added, nhóm không tự suy diễn thời điểm bổ sung mà loại chúng khỏi tập phân tích theo thời gian.
## LÀM SẠCH DỮ LIỆU
### Chuẩn hóa dữ liệu dạng chuỗi
Thực hiện lần lượt loại bỏ khoảng trắng đầu cuối và chuyển các chuỗi rỗng thành giá trị NaN. Nhóm chỉ chuẩn hóa cách biểu diễn dữ liệu, không thay đổi nội dung thực tế của tên phim, tên đạo diễn, diễn viên, quốc gia hoặc thể loại.
def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
"""
Chuẩn hóa các cột dạng text:
- Loại bỏ khoảng trắng đầu/cuối
- Chuyển chuỗi rỗng thành NaN
"""
df = df.copy()
text_columns = df.select_dtypes(include='str').columns

for column in text_columns:
df[column] = df[column].str.strip()
df[column] = df[column].replace('', pd.NA)

return df
### Chuẩn hóa date_added
def clean_date_added(df: pd.DataFrame) -> pd.DataFrame:
"""
Chuyển date_added sang kiểu datetime.

Các giá trị không hợp lệ sẽ trở thành NaT.
Không tự suy đoán ngày bị thiếu.
"""
df = df.copy()
if ('date_added' not in df.keys()):
return "data doesn't contain date_added column"

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce', format='mixed')

return df
Các giá trị ngày tháng được chuyển từ dạng chuỗi sang kiểu datetime bằng pd.to_datetime() với format="mixed". Việc sử dụng format="mixed" giúp xử lý đúng các chuỗi ngày tháng hợp lệ trong dataset mà không làm mất các giá trị chỉ vì khác biệt về cách biểu diễn chuỗi. Các giá trị thực sự thiếu ngày được giữ dưới dạng NaT; nhóm không tự suy diễn hoặc tạo ngày thay thế.
### Chuẩn hóa release_year
Giá trị release_year được chuyển sang kiểu số nguyên có hỗ trợ giá trị thiếu:
def clean_release_year(df: pd.DataFrame) -> pd.DataFrame:
"""
Chuẩn hóa release_year về kiểu số nguyên nullable.
"""
df = df.copy()
if ('release_year' not in df.keys()):
return "data doesn't contain release_year column"

df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').astype('Int64')

return df
Nhóm không loại bỏ bản ghi chỉ vì thiếu release_year, bởi trường này không được sử dụng để xác định phạm vi 2011–2020.
### Chuẩn hóa duration
Trường duration có hai ý nghĩa tùy theo type, nếu type là Movie thì nó sẽ có dạng số kèm hậu tố min biểu trưng cho độ dài về mặt số phút của Movie đó. Ngược lại, nếu type là TV Shows thì nó là dạng số kèm hậu tố season biểu trưng cho số mùa của một chương trình truyền hình. Về mặt ý nghĩa thì nó rất hợp lý nhưng về mặt thống kê thì cách viết này khá khó khăn cho việc phân tích dữ liệu vì một trường không nên có 2 cách biểu diễn dữ liệu khác nhau vì nó có bản chất khác nhau.
Do đó nhóm quyết định chuẩn hóa và tách thành 2 trường khác nhau tên duration_minutes và duration_seasons theo quy tắc sau:
Movie: duration_minutes  = số phút, duration_seasons   = NULL
TV Show: duration_minutes  = NULL, duration_seasons   = số mùa
Cách làm này giúp các chương sau có thể phân tích riêng các phân phối thời lượng Movie, phân phối số mùa TV Show.
### Xử lý dữ liệu thiếu
Nhóm không sử dụng dropna() trên toàn bộ dataset. Lý do là việc thiếu một thuộc tính không có nghĩa toàn bộ bản ghi không còn giá trị. Ví dụ, một nội dung thiếu director vẫn có thể được sử dụng để phân tích: thời gian, loại nội dung, quốc gia, thể loại, rating. Do đó, nhóm chỉ loại một bản ghi khỏi phạm vi phân tích thời gian khi không thể xác định date_added hợp lệ. Các trường thông tin khác tiếp tục được giữ nguyên giá trị thiếu để tránh làm mất dữ liệu hợp lệ.
## CHUẨN HÓA DỮ LIỆU
### Mục đích chuẩn hóa
Sau khi làm sạch, dữ liệu vẫn còn các thuộc tính đa trị. Nếu tiếp tục lưu nhiều giá trị trong một ô, việc truy vấn và trực quan hóa sẽ gặp khó khăn. Ví dụ như:
Bảng 2.2 Bảng ví dụ minh họa về dữ liệu chứa thuộc tính đa trị
| show_id | listed_in |
| --- | --- |
| s001 | Drama, Comedy, International Movies |
Nếu cần đếm số nội dung thuộc Drama, nhóm phải tách chuỗi trước khi thực hiện thống kê. Do đó, nhóm chuẩn hóa dữ liệu thành các bảng riêng. Khác với việc chuẩn hóa toàn bộ dữ liệu theo mô hình OLTP 3NF, nhóm xây dựng mô hình dữ liệu chuẩn hóa phục vụ phân tích và trực quan hóa theo mô hình OLAP bởi vì dataset không cần cập nhật gì nhiều.
### Mô hình dữ liệu sau chuẩn hóa

Hình 2.11 Mô hình dữ liệu gồm bảy bảng sau chuẩn hóa
Đây là mô hình dữ liệu sau khi chuẩn hóa của nhóm, chia thành 3 nhóm khác nhau:
Nhóm Dimension
Nhóm này chứa thông tin mô tả và các trường được tính toán sẵn nhằm phục vụ các phân tích và trực quan hóa ở sau. Gồm có bảng dim_title chứa các thông tin về các chương trình như trong bảng cũ, chỉ có phần duration là được chuẩn hóa theo như đã phân tích ở phần làm sạch dữ liệu.

Hình 2.12 Lược đồ dim_title
Ngoài ra còn có bảng dim_date gồm các kiểu biểu diễn khác tổng quát hóa khác nhau của ngày như year, month, quarter để phục vụ phân tích theo các giai đoạn và các trường dữ liệu như month_name, quarter_name để làm nhãn phục vụ trực quan hóa theo các giai đoạn.

Hình 2.13 Lược đồ dim_date
Vì thế nên trong dim_title cần thêm một trường date_key để liên kết với bảng dim_date nhưng vẫn giữ date_added để đảm bảo tính đầy đủ và phục vụ các phân tích khác nếu sử dụng đơn vị thời gian “ngày” mà không cần kết với dim_date.
Nhóm Bridge
Nhóm này chứa các thông tin bổ sung và các thuộc tính đa trị nhằm bổ sung vào bảng chính dim_title.
Bảng bridge_genre
Bảng này được tách ra từ cột listed_in để tránh các thuộc tính đa trị và phục vụ các phân tích như:
Top thể loại
thể loại theo Movie/TV Show
thể loại theo thời gian
thể loại phổ biến theo quốc gia

Hình 2.14 Lược đồ bridge_genre
Bảng bridge_country
Bảng này được tách ra từ cột country vì các lý do tương tự với country_code được bổ sung nhằm phục vụ trực tiếp cho biểu đồ bản đồ và các phân tích địa lý. Thay vì dùng country_code để thay thế country thì nhóm vẫn giữ country để hiển thị tên quốc gia trên dashboard.

Hình 2.15 Lược đồ bridge_country
Bảng bridge_director
Cùng với các lý do tương tự và để mở rộng khả năng phân tích insight, nhóm tách trường director thành bảng bridge_director. Mỗi dòng thể hiện một quan hệ giữa một nội dung và một đạo diễn. Một đạo diễn có thể xuất hiện ở nhiều nội dung. Nhờ bảng này, nhóm có thể phân tích:
Top đạo diễn có nhiều nội dung nhất;
đạo diễn theo loại nội dung;
đạo diễn theo thể loại;
đạo diễn theo quốc gia;
sự xuất hiện của đạo diễn theo thời gian.
Việc bổ sung bảng này giúp phần insight ở chương sau có thêm một chiều phân tích mà không cần sử dụng nguồn dữ liệu bên ngoài.

Hình 2.16 Lược đồ bridge_director
Bảng bridge_actor
Tương tự trường cast, nhóm tách danh sách diễn viên thành bridge_actor. Một diễn viên có thể xuất hiện trong nhiều nội dung. Bảng bridge_actor cho phép nhóm thực hiện các phân tích:
Top diễn viên xuất hiện nhiều nhất
diễn viên theo Movie/TV Show
diễn viên theo thể loại
diễn viên theo quốc gia
sự xuất hiện của diễn viên theo thời gian
Từ đó, nhóm có thể rút ra thêm insight về sự phân bố diễn viên trong danh mục nội dung Netflix.

Hình 2.17 Lược đồ bridge_actor
Nhóm Fact
Nhóm này xuất hiện nhằm phục vụ phân tích xu hướng và mô hình dự báo, nó chứa các trường dữ liệu cụ thể về một mục cố định và có các các trường tính toán sẵn theo các con số có thể tính toán thay vì chứa các dữ liệu chung chung và không phục vụ dự đoán như của nhóm Dimension. Nhóm đã tạo ra fact_monthly_addition nhằm dự báo số lượng title được thêm vào Netflix theo từng tháng.

Hình 2.18 Lược đồ fact_monthly_addition
Trong bảng gồm các trường date_key để nhận được định danh ngày từ bảng dim_date, monthly_additions được tính toán bằng cách đếm số title có date_added nằm trong tháng đó, month_index đây là chỉ mục riêng bắt đầu từ số 0 được tạo ra nhằm phục vụ tính toán và xây dựng mô hình dự báo.
## VALIDATION SAU CHUẨN HÓA
Sau khi tạo bảy bảng, nhóm tiến hành kiểm tra tính toàn vẹn của dữ liệu. Mục đích của bước này là đảm bảo dữ liệu sau khi chuẩn hóa vẫn đúng với mô hình đã thiết kế, không xuất hiện các lỗi về cấu trúc bảng, khóa chính, khóa ngoại và các quy tắc dữ liệu cần thiết trước khi lưu trữ vào SQLite.
Nhóm xây dựng file validation.py để thực hiện các bước kiểm tra tự động thay vì kiểm tra thủ công từng bảng. Các nội dung được kiểm tra gồm:
Kiểm tra cấu trúc và các cột bắt buộc
Kiểm tra khóa chính
Kiểm tra khóa ngoại
Kiểm tra số lượng ngày trong dim_date
Kiểm tra số lượng tháng trong fact_monthly_addition
Kiểm tra giá trị của monthly_additions
Kiểm tra month_index
Kiểm tra tổng số lượng title
Kiểm tra phạm vi thời gian của dim_title
### Kiểm tra cấu trúc các bảng
Đầu tiên, nhóm kiểm tra xem bảy bảng sau khi chuẩn hóa có tồn tại đầy đủ và có đúng các trường dữ liệu cần thiết hay không:
dim_date
dim_title
bridge_genre
bridge_country
bridge_director
bridge_actor
fact_monthly_addition
Nhóm xây dựng danh sách các trường bắt buộc cho từng bảng trong validation.py:
TABLES: dict[str, list[str]] = {
"dim_date": [
"date_key", "date", "year", "month",
"month_name", "quarter", "quarter_name"
],
"dim_title": [
"show_id", "title", "type", "date_added", "date_key",
"release_year", "rating", "duration_minutes", "duration_seasons"
],
"bridge_genre": ["show_id", "genre"],
"bridge_country": ["show_id", "country"],
"bridge_director": ["show_id", "director"],
"bridge_actor": ["show_id", "actor"],
"fact_monthly_addition": [
"date_key", "monthly_additions", "month_index"
],
}

Sau đó nhóm kiểm tra lần lượt từng bảng và từng trường. Nếu một bảng không tồn tại hoặc thiếu trường bắt buộc thì chương trình sẽ ghi nhận lỗi. Việc kiểm tra này nhằm đảm bảo dữ liệu đầu vào của các bước validation tiếp theo đúng với mô hình đã được thiết kế ở phần 2.4. Nếu tất cả các bảng đều tồn tại và không thiếu trường bắt buộc thì nhóm tiếp tục thực hiện các bước kiểm tra sâu hơn.
### Kiểm tra khóa chính
Sau khi kiểm tra cấu trúc, nhóm tiếp tục kiểm tra các trường được sử dụng làm khóa chính. Các khóa chính được xác định như sau:
Bảng 2.3 Bảng danh sách khóa chính của các bảng dữ liệu sau chuẩn hóa
| Bảng | Khóa chính |
| --- | --- |
| dim_date | date_key |
| dim_title | show_id |
| bridge_genre | show_id + genre |
| bridge_country | show_id + country |
| bridge_director | show_id + director |
| bridge_actor | show_id + actor |
| fact_monthly_addition | date_key |
Nhóm kiểm tra hai vấn đề là khóa chính có giá trị NULL hay không và có xuất hiện giá trị trùng lặp hay không.
if df[key].isna().any():
errors.append(f"{table_name}.{key}: có giá trị NULL")

if df[key].duplicated().any():
errors.append(f"{table_name}.{key}: có khóa trùng")
Nếu khóa chính có giá trị NULL thì không thể xác định chính xác bản ghi tương ứng. Nếu khóa chính bị trùng thì mỗi bản ghi không còn được định danh duy nhất. Do đó, nhóm yêu cầu các khóa chính phải đảm bảo không có null và không có lặp.
### Kiểm tra khóa ngoại
Tiếp theo, nhóm kiểm tra các mối quan hệ giữa các bảng sau khi chuẩn hóa. Đối với date_key, các giá trị trong dim_title.date_key và fact_monthly_addition.date_key phải tồn tại trong dim_title.date_key. Đối với show_id, các giá trị trong: bridge_genre.show_id, bridge_country.show_id, bridge_director.show_id và bridge_actor.show_id phải nằm trong title.show_id.
Nhóm thực hiện kiểm tra bằng cách lấy tập các khóa hợp lệ từ bảng được tham chiếu rồi so sánh với các khóa xuất hiện ở bảng liên quan. Nếu orphan_keys khác rỗng thì có nghĩa là bảng đang chứa một show_id không tồn tại trong dim_title.
actual_keys = set(data[table_name][column].dropna())
orphan_keys = actual_keys - valid_keys

if orphan_keys:
errors.append(
f"{table_name}.{column}: "
f"{len(orphan_keys)} khóa ngoại không tồn tại"
)
Nhóm thực hiện kiểm tra này đối với toàn bộ bốn bảng bridge nhằm đảm bảo việc tách các thuộc tính đa trị ở phần 2.4 không làm mất liên kết với bảng dim_title.
### Kiểm tra số lượng ngày và tháng
Do dim_date được thiết kế để chứa toàn bộ ngày trong phạm vi nghiên cứu từ 2011 đến 2020, nhóm tiếp tục kiểm tra số lượng ngày thực tế trong bảng. Khoảng thời gian được xác định là: 01/01/2011 → 31/12/2020 Tương ứng với toàn bộ số ngày trong 10 năm này. Sau đó so sánh số lượng ngày thực tế trong dim_date với số ngày kỳ vọng. Nếu số lượng không bằng nhau, chương trình sẽ báo lỗi để nhóm kiểm tra lại quá trình tạo bảng dim_date.
Tương tự như dim_date, bảng fact_monthly_addition cũng có một số lượng bản ghi được xác định trước. Do đó bảng fact_monthly_addition phải có đủ 120 dòng, tương ứng với 120 tháng từ tháng 01/2011 đến tháng 12/2020. Một điểm nhóm đặc biệt lưu ý là tháng không có nội dung được thêm vào vẫn phải tồn tại trong bảng và có monthly_additions = 0. Thay vì loại bỏ tháng đó, nhóm giữ lại để đảm bảo chuỗi thời gian liên tục. Điều này sẽ cần thiết cho quá trình xây dựng mô hình dự báo ở chương 5.
Việc kiểm tra này giúp đảm bảo bảng ngày không bị thiếu ngày, từ đó tránh ảnh hưởng đến các phân tích theo thời gian ở những chương sau.
expected_dates = (
pd.date_range(
f"{START_YEAR}-01-01",
f"{END_YEAR}-12-31",
freq="D"
)
)

expected_months = (END_YEAR - START_YEAR + 1) * 12

if len(dim_date) != len(expected_dates):
errors.append(
f"dim_date: {len(dim_date)} dòng, "
f"mong đợi {len(expected_dates)}"
)

if len(fact) != expected_months:
errors.append(
f"fact_monthly_addition: {len(fact)} dòng, "
f"mong đợi {expected_months}"
)
### Kiểm tra giá trị monthly_additions và month_index
Trường monthly_additions trong fact_monthly_addition thể hiện số lượng title được thêm vào Netflix trong từng tháng. Vì đây là một đại lượng đếm nên giá trị không thể nhỏ hơn 0. Do đó, điều kiện hợp lệ của trường này là: monthly_additions >= 0. Nếu một tháng không có title mới thì giá trị được biểu diễn bằng 0.
Trong phần chuẩn hóa bảng fact_monthly_addition, nhóm đã tạo thêm trường month_index nhằm phục vụ cho việc xây dựng mô hình dự báo. Trường này được thiết kế bắt đầu từ 0 và tăng liên tục theo từng tháng. Do đó, nhóm kiểm tra danh sách month_index có đúng với dãy từ 0 đến 119 hay không, nếu chỉ số bị thiếu một giá trị hoặc bị thay đổi thứ tự thì chương trình sẽ báo lỗi.
if fact["monthly_additions"].lt(0).any():
errors.append(
"fact_monthly_addition.monthly_additions: "
"có giá trị âm"
)

if fact["month_index"].tolist() != list(range(expected_months)):
errors.append(
"fact_monthly_addition.month_index: "
"không liên tục từ 0 đến 119"
)
Kiểm tra này giúp phát hiện những lỗi bất thường có thể xảy ra trong quá trình tổng hợp số lượng title theo tháng và nó cũng rất quan trọng vì month_index sẽ được sử dụng làm biến thời gian trong mô hình Linear Regression ở chương xây dựng mô hình dự báo.
### Kiểm tra tổng số lượng title
Sau khi kiểm tra bảng fact, nhóm tiếp tục đối chiếu tổng số title được tính toán trong fact_monthly_addition với số lượng bản ghi trong dim_title. Tất cả phải bằng nhau, nếu không bằng nhau thì đã có lỗi xẩy ra trong quá trình xử lý dữ liệu.
total_fact = int(fact["monthly_additions"].sum())

if total_fact != len(dim_title):
errors.append(
"Tổng monthly_additions không bằng số dòng dim_title: "
f"{total_fact} != {len(dim_title)}"
)
Kiểm tra này giúp nhóm phát hiện những trường hợp có thể xảy ra trong quá trình chuẩn hóa và tổng hợp dữ liệu như: bỏ sót title, đếm trùng title, lọc sai phạm vi thời gian hoặc tính sai số lượng title theo tháng,..
Đây là một trong những kiểm tra quan trọng nhất đối với bảng fact_monthly_addition vì bảng này được tạo trực tiếp từ dim_title.
### Kiểm tra lại phạm vi thời gian của dim_title
Cuối cùng, nhóm kiểm tra lại phạm vi thời gian của bảng dim_title sau khi chuẩn hóa. Mặc dù phạm vi 2011–2020 đã được kiểm tra ở phần 2.2, nhóm vẫn thực hiện lại bước này để đảm bảo rằng quá trình chuẩn hóa không đưa các bản ghi ngoài phạm vi vào bảng phân tích. Nếu xuất hiện bản ghi nằm ngoài khoảng 2011–2020, chương trình sẽ ghi nhận lỗi. Nhóm chuyển date_added về dạng datetime và kiểm tra năm:
dates = pd.to_datetime(
dim_title["date_added"],
errors="coerce"
)

invalid_scope = ~dates.dt.year.between(START_YEAR, END_YEAR)

if invalid_scope.any():
errors.append(
f"dim_title: {int(invalid_scope.sum())} "
f"title nằm ngoài phạm vi {START_YEAR}-{END_YEAR}"
)
Như vậy, dim_title sau chuẩn hóa chỉ chứa những nội dung thuộc đúng phạm vi nghiên cứu của đề tài.
### Kết quả validation
Sau khi thực hiện các bước trên, nhóm tổng hợp kết quả validation thành hai trạng thái: PASS, FAIL. Nếu tất cả các bước kiểm tra đều không phát hiện lỗi, kết quả sẽ là: PASS. Ngược lại, nếu tồn tại ít nhất một lỗi thì kết quả sẽ là: FAIL. Nhóm cũng lưu kết quả validation thành file: validation_report.json.
File này được sử dụng để lưu lại trạng thái validation, các lỗi phát hiện được và thông tin cơ bản của từng bảng. Nhờ đó, nhóm có thể kiểm tra lại kết quả của quá trình chuẩn hóa mà không cần thực hiện thủ công.

Bảng 2.4 Bảng tổng hợp kết quả kiểm tra toàn vẹn dữ liệu sau chuẩn hóa
| Nội dung kiểm tra | Yêu cầu | Kết quả |
| --- | --- | --- |
| Cấu trúc | Đủ 7 bảng và các trường bắt buộc | Đạt |
| Khóa chính | Không NULL, không trùng | Đạt |
| Khóa ngoại | Không có khóa không tồn tại | Đạt |
| dim_date | Đủ toàn bộ ngày 2011–2020 | Đạt |
| fact_monthly_addition | Đủ 120 tháng | Đạt |
| monthly_additions | Không có giá trị âm | Đạt |
| month_index | Liên tục từ 0 đến 119 | Đạt |
| Tổng số title | Bằng số dòng dim_title | Đạt |
| Phạm vi dim_title | Chỉ thuộc 2011–2020 | Đạt |
Vậy là sau khi kiểm tra thì mọi thứ đã đạt, dữ liệu sau khi chuẩn hóa không chỉ có cấu trúc đúng mà còn duy trì được các mối quan hệ giữa các bảng và các quy tắc cần thiết cho quá trình phân tích sau này.
## KẾT QUẢ SAU TIỀN XỬ LÝ
Sau khi hoàn thành cleaning, normalization và validation, nhóm lưu dữ liệu dưới dạng các file CSV trong thư mục data/processed và lưu tất cả vào cơ sở dữ liệu SQLite lưu trong database/netflix.db để đảm bảo tương thích với nhiều công cụ phân tích và trực quan hóa dữ liệu nhất. Mặc dù dữ liệu nguồn được cung cấp dưới dạng một tệp CSV, nhóm đã chuẩn hóa và phân tách dữ liệu thành các bảng có quan hệ với nhau để giải quyết các vấn đề đã nêu. Các bảng này sẽ được kết nối thông qua show_id và date_key trong quá trình phân tích và xây dựng dashboard.
Sau quá trình audit, cleaning, normalization và validation, nhóm xây dựng được pipeline:

Hình 2.19 Pipeline xử lý dữ liệu của đề tài
Và nhận được các kết quả quan trọng:
Bảng 2.5 Bảng thống kê kết quả sau quá trình tiền xử lý dữ liệu
| Nội dung | Kết quả |
| --- | --- |
| Dataset ban đầu | 8.807 bản ghi |
| Số cột ban đầu | 12 |
| show_id duy nhất | 8.807 |
| Bản ghi trùng hoàn toàn | 0 |
| NULL date_added | 10 |
| date_added không parse được | 0 |
| Ngày thêm vào NULL | 10 |
| Ngày thêm vào HỢP LỆ | 8797 |
| Trong phạm vi 2011–2020 | 7.294 |
| Ngoài phạm vi, có ngày hợp lệ | 1.503 |
| Tỷ lệ trong phạm vi | 82,82% |
| Số tháng phân tích | 120 |
| Số bảng chuẩn hóa | 7 |
## KẾT LUẬN CHƯƠNG
Trong chương này, nhóm đã thực hiện quá trình từ thu thập, kiểm tra, làm sạch, chuẩn hóa, validation đến lưu trữ dữ liệu nhằm tạo ra nguồn dữ liệu thống nhất cho các bước phân tích tiếp theo.
Đầu tiên, nhóm sử dụng netflix_titles.csv với 8.807 bản ghi và 12 trường dữ liệu làm nguồn dữ liệu chính. Qua quá trình kiểm tra, show_id được xác định có thể sử dụng làm khóa chính vì không chứa giá trị NULL hoặc trùng lặp.
Nhóm cũng phát hiện các thuộc tính đa trị trong country, listed_in, director và cast. Thay vì giữ nhiều giá trị trong một ô, nhóm quyết định chuẩn hóa thành bốn bảng liên kết gồm bridge_country, bridge_genre, bridge_director và bridge_actor. Trong đó, hai bảng bridge_director và bridge_actor được bổ sung nhằm mở rộng khả năng phân tích và rút trích insight về đạo diễn và diễn viên trong các chương sau.
Đối với trường date_added, nhóm xác định đây là trường dùng để xác định phạm vi nghiên cứu. Sau khi kiểm tra lại bằng phương pháp parse ngày tháng với format="mixed", có 7.294 bản ghi thuộc giai đoạn 2011–2020, chiếm 82,82% tổng số bản ghi. Dataset có 10 bản ghi thiếu date_added và không có giá trị ngày tháng không hợp lệ. Các bản ghi ngoài phạm vi không bị xem là dữ liệu lỗi mà chỉ được loại khỏi tập dữ liệu phân tích của đề tài.
Trong quá trình làm sạch, nhóm chuẩn hóa dữ liệu dạng chuỗi, ngày tháng và năm phát hành; đồng thời tách duration thành duration_minutes và duration_seasons. Các giá trị thiếu không bị loại bỏ hàng loạt nhằm hạn chế mất dữ liệu có giá trị cho các phân tích khác nhau.
Sau cùng, nhóm xây dựng mô hình dữ liệu gồm 7 bảng: dim_title, dim_date, bridge_genre, bridge_country, bridge_director, bridge_actor và fact_monthly_addition. Mô hình này vừa giải quyết các thuộc tính đa trị, vừa cung cấp các chiều dữ liệu cần thiết cho phân tích theo thời gian, loại nội dung, thể loại, quốc gia, đạo diễn và diễn viên.
Dữ liệu sau khi hoàn thành tiền xử lý được lưu dưới dạng CSV và SQLite, tạo thành nguồn dữ liệu đầu vào thống nhất cho phân tích khám phá, rút trích insight, xây dựng mô hình dự báo và dashboard ở các chương tiếp theo.
# PHÂN TÍCH DỮ LIỆU
## Tổng quan phân tích
Mục tiêu của chương này là khám phá và mô trả cấu trúc của tập dữ liệu sau quá trình tiền xử lý, bao gồm 7.294 nội dung (title) duy nhất được thêm vào Netflix trong giai đoạn 2011-2020. Quá trình khám quá dữ liệu (Exploratory Data Analysis - EDA) tập trung vào việc quan sát sự thay đổi số lượng nội dung theo thời gian, so sánh tỷ trọng giữa Movie và TV Show, đồng thời nhận diện các quốc gia, thể loại và phân loại độ tuổi phổ biến nhất trên nền tảng.
## Phân tích xu hướng nội dung được thêm mới theo năm
Để quan sát sự thay đổi của số lượng nội dung theo thời gian, biểu đồ đường được lựa chọn sử dụng vì trục thời gian (năm) có thứ tự liên tục, giúp thể hiện trực quan nhất xu hướng tăng giảm qua các năm.
# Bước 1: Đếm title duy nhất theo năm.
annual = titles.groupby("added_year")["show_id"].nunique()

# Bước 2: Xem bảng kết quả.
print(annual)

# Bước 3: Vẽ biểu đồ đường bằng Matplotlib.
plt.figure(figsize=(10, 5))
plt.plot(annual.index, annual.values, marker="o", color="red")

for year, value in annual.items():
    plt.text(year, value + 30, str(value), ha="center", fontsize=9)

plt.title("Số title được thêm vào Netflix theo năm")
plt.xlabel("Năm được thêm")
plt.ylabel("Số title duy nhất")
plt.xticks(annual.index)
plt.ylim(0, annual.max() * 1.12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Bước 4: Tính kết quả nổi bật.
peak_year = annual.idxmax()
peak_value = annual.max()
change_2020 = (annual[2020] - annual[2019]) / annual[2019] * 100

print("Năm cao nhất:", peak_year)
print("Số title cao nhất:", peak_value)
print("Thay đổi 2020 so với 2019:", round(change_2020, 1), "%")


Hình 3.1. Số title được thêm vào Netflix từ năm 2011-2020
Quan sát số lượng nội dung (show_id duy nhất) được thêm vào theo năm cho thấy một xu hướng tăng rõ rệt bắt đầu từ năm 2016 với 429 title và đạt đỉnh vào năm 2019 với 2.016 title. Tuy nhiên đà tăng trưởng này đã chững lại và sụt giảm trong năm 2020 khi số lượng nội dung thêm mới chỉ còn 1.879 title, tương đương với mức giảm 6.8% (giảm đi 137 title so với năm 2019).
Sự sụt giảm trong năm 2020 là một quan sát thực tế từ dữ liệu, tuy nhiên do bộ dữ liệu hiện tại không chứa các biến số về môi trường kinh doanh hay tác động xã hội, nên ta không thể khẳng định nguyên nhân chính dẫn đến sự sụt giảm này.
## Phân tích cơ cấu Movie và TV Show
Biểu đồ cột chồng có tỷ lệ phần trăm được sử dụng làm công cụ trực quan hóa cho phần này vì nó cho phép so sánh rõ ràng sự thay đổi về cơ cấu và tỷ trọng phần trăm giữa hai nhóm Movie và TV Show trong cùng một năm.
# Bước 1: Tạo bảng chéo giữa năm và loại nội dung.
type_by_year = pd.crosstab(titles["added_year"], titles["type"])
type_by_year = type_by_year[["Movie", "TV Show"]]

print("Số lượng theo năm:")
print(type_by_year)

# Bước 2: Tính tỷ lệ phần trăm trong từng năm.
year_total = type_by_year.sum(axis=1)
type_share = type_by_year.div(year_total, axis=0) * 100

print("Tỷ lệ theo năm:")
print(type_share.round(1))

# Bước 3: Vẽ biểu đồ cột chồng 100%.
fig, ax = plt.subplots(figsize=(12, 5))
type_share.plot(
    kind="bar",
    stacked=True,
    color=["#E50914", "#333333"],
    ax=ax
)

# Ghi cả số lượng và tỷ lệ phần trăm vào giữa từng phần của cột.
for position, year in enumerate(type_share.index):
    movie_percent = type_share.loc[year, "Movie"]
    tv_percent = type_share.loc[year, "TV Show"]
    movie_value = type_by_year.loc[year, "Movie"]
    tv_value = type_by_year.loc[year, "TV Show"]

    if movie_percent > 0:
        ax.text(
            position,
            movie_percent / 2,
            f"{movie_value}\n{movie_percent:.1f}%",
            ha="center",
            va="center",
            color="white",
            fontsize=8
        )

    if tv_percent > 0:
        ax.text(
            position,
            movie_percent + tv_percent / 2,
            f"{tv_value}\n{tv_percent:.1f}%",
            ha="center",
            va="center",
            color="white",
            fontsize=8
        )

plt.title("Tỷ trọng Movie và TV Show theo năm")
plt.xlabel("Năm được thêm")
plt.ylabel("Tỷ lệ phần trăm")
plt.ylim(0, 100)
plt.yticks(range(0, 101, 20))
plt.xticks(rotation=0)
ax.grid(axis="y", alpha=0.25)
ax.set_axisbelow(True)
ax.legend(
    title="Loại nội dung",
    loc="upper left",
    bbox_to_anchor=(1.02, 1),
    borderaxespad=0
)
fig.subplots_adjust(right=0.82, bottom=0.15)
plt.show()

# Bước 4: So sánh thay đổi từ 2019 sang 2020.
movie_change = type_by_year.loc[2020, "Movie"] - type_by_year.loc[2019, "Movie"]
tv_change = type_by_year.loc[2020, "TV Show"] - type_by_year.loc[2019, "TV Show"]

# Bước 5: Phân rã mức tăng trong giai đoạn 2016-2019.
total_growth = year_total.loc[2019] - year_total.loc[2016]
movie_growth = type_by_year.loc[2019, "Movie"] - type_by_year.loc[2016, "Movie"]
tv_growth = type_by_year.loc[2019, "TV Show"] - type_by_year.loc[2016, "TV Show"]
movie_contribution = movie_growth / total_growth * 100

print("Movie thay đổi từ 2019 sang 2020:", movie_change)
print("TV Show thay đổi từ 2019 sang 2020:", tv_change)
print("Tổng title tăng từ 2016 đến 2019:", total_growth)
print("Movie đóng góp:", movie_growth, "title")
print("TV Show đóng góp:", tv_growth, "title")
print("Tỷ lệ đóng góp của Movie:", round(movie_contribution, 1), "%")


Hình 3.2. Tỷ trọng Movie và TV Show giai đoạn 2011-2020
Trong giai đoạn này, Movie là loại hình chiếm ưu thế tuyệt đối với 5.134 title (tương đương với 70.4%), trong khi TV Show có 2.160 (chiếm 29.6%).
Khi phân rã đóng góp theo từng năm, dữ liệu cho thấy sự biến động của tổng số lượng nội dung bị chi phối mạnh mẽ bởi nhóm Movie:
Giai đoạn tăng (2016-2019): Tổng nội dung tăng thêm 1.587 title, trong đó riêng Movie tăng 1.171 title, đóng góp tới 73.8% đà tăng trưởng chung.
Giai đoạn giảm (2020): Mức giảm 137 title trong năm 2020 được giải thích bởi sự sụt giảm của nhóm Movie (giảm 140 title), trong khi mảng TV Show vẫn tăng 3 title.
## Phân tích độ phủ của thể loại (genre) và quốc gia (country)
Đối với dữ liệu có nhiều hạng mục và tên nhãn dài như thể loại hay quốc gia, biểu đồ cột ngang sử dụng với bảng màu tuần tự để tối ưu không gian hiển thị và giúp người đọc dễ dàng so sánh thứ hạng của top 10 nhóm hàng đầu.
# Bước 1: Đếm title duy nhất theo genre.
genre_counts = genres.groupby("genre")["show_id"].nunique()

# Bước 2: Chọn 10 genre cao nhất.
top_genres = genre_counts.sort_values(ascending=False).head(10)
print(top_genres)

# Bước 3: Đảo thứ tự để genre lớn nhất nằm trên cùng biểu đồ ngang.
top_genres_chart = top_genres.sort_values()

plt.figure(figsize=(10, 6))

# Giá trị thấp dùng màu nhạt, giá trị cao dùng màu đậm.
genre_colors = sns.color_palette("Reds", len(top_genres_chart))
bars = plt.barh(
    top_genres_chart.index,
    top_genres_chart.values,
    color=genre_colors
)
plt.bar_label(bars, padding=3)
plt.title("Top 10 genre theo số title duy nhất")
plt.xlabel("Số title duy nhất")
plt.ylabel("Genre")
plt.xlim(0, top_genres_chart.max() * 1.12)
plt.grid(axis="x", alpha=0.2)
plt.tight_layout()
plt.show()

top_genre = top_genres.index[0]
top_genre_count = top_genres.iloc[0]
top_genre_share = top_genre_count / total_titles * 100

print("Genre đứng đầu:", top_genre)
print("Số title:", top_genre_count)
print("Tỷ lệ trên tổng title:", round(top_genre_share, 1), "%")


Hình 3.3. Top 10 thể loại có số nội dung nhiều nhất
Về thể loại, khi đếm số nội dung duy nhất theo thể loại thì “International Movies” là nhãn xuất hiện nhiều nhất với 2.343 title (chiếm 32.1% tổng nội dung), xếp thứ hai là “Dramas” với 2.013 title và thứ 3 là “Comedies” với 1.375 title.
# Bước 1: Đếm title duy nhất theo country.
country_counts = countries.groupby("country")["show_id"].nunique()

# Bước 2: Chọn 10 country cao nhất.
top_countries = country_counts.sort_values(ascending=False).head(10)
print(top_countries)

# Bước 3: Vẽ biểu đồ cột ngang.
top_countries_chart = top_countries.sort_values()

plt.figure(figsize=(10, 6))

# Giá trị thấp dùng màu nhạt, giá trị cao dùng màu đậm.
country_colors = sns.color_palette("Blues", len(top_countries_chart))
bars = plt.barh(
    top_countries_chart.index,
    top_countries_chart.values,
    color=country_colors
)
plt.bar_label(bars, padding=3)
plt.title("Top 10 quốc gia theo số title duy nhất")
plt.xlabel("Số title duy nhất")
plt.ylabel("Quốc gia")
plt.xlim(0, top_countries_chart.max() * 1.12)
plt.grid(axis="x", alpha=0.2)
plt.tight_layout()
plt.show()

# Bước 4: Kiểm tra độ bao phủ của dữ liệu country.
titles_with_country = countries["show_id"].nunique()
missing_country = total_titles - titles_with_country
country_coverage = titles_with_country / total_titles * 100

print("Số title có country:", titles_with_country)
print("Số title thiếu country:", missing_country)
print("Độ bao phủ country:", round(country_coverage, 1), "%")


Hình 3.4. Top 10 quốc gia có số nội dung nhiều nhất
Về quốc gia, nước Mỹ dẫn đầu với 3.053 title, bỏ xa Ấn Độ ở vị trí thứ 2 với 941 title và Vương Quốc Anh với 685 title.
## Phân tích cơ cấu phân loại độ tuổi
Để quan sát sự phân bổ tỷ trọng của nhiều nhãn phân loại độ tuổi thay đổi như thế nào qua từng năm một cách tổng quan nhất thì ta sẽ sử dụng biểu đồ Heatmap.
# Bước 1: Chọn 8 rating xuất hiện nhiều nhất.
top_ratings = titles["rating"].value_counts().head(8).index

# Bước 2: Tạo bảng chéo năm x rating và chuẩn hóa theo từng năm.
rating_share = pd.crosstab(
    titles["added_year"],
    titles["rating"],
    normalize="index"
) * 100

rating_heatmap = rating_share[top_ratings]

# Bước 3: Vẽ heatmap bằng Seaborn.
plt.figure(figsize=(10, 6))
ax = sns.heatmap(
    rating_heatmap,
    annot=True,
    fmt=".1f",
    cmap="Reds",
    linewidths=0.5,
    vmin=0,
    vmax=50,
    cbar_kws={"label": "Tỷ lệ title trong từng năm (%)"}
)
plt.title("Tỷ trọng rating theo năm")
plt.xlabel("Rating")
plt.ylabel("Năm được thêm")
plt.xticks(rotation=0)
plt.yticks(rotation=0)

plt.tight_layout()
plt.show()

# Bước 4: Tính tỷ trọng của hai rating lớn nhất.
known_rating = titles["rating"].notna().sum()
top_two_rating = titles["rating"].isin(["TV-MA", "TV-14"]).sum()
top_two_share = top_two_rating / known_rating * 100

print("Số title có rating:", known_rating)
print("Số title thuộc TV-MA hoặc TV-14:", top_two_rating)
print("Tỷ lệ TV-MA và TV-14:", round(top_two_share, 1), "%")
print("Số title thiếu rating:", titles["rating"].isna().sum())


Hình 3.5. Tỷ trọng rating giao đoạn 2011-2020
Trước khi phân tích biểu đồ này, ta sẽ giải thích các nhãn rating trước:
TV-MA: dành cho khán giả trưởng thành.
TV-14: có thể không phù hợp với trẻ dưới 14 tuổi.
TV-PG: trẻ em nên xem cùng sự hướng dẫn của phụ huynh.
R: nội dung hạn chế, thường dành cho người trưởng thành.
PG-13: có thể không phù hợp với trẻ dưới 13 tuổi.
TV-Y: phù hợp với trẻ nhỏ.
TV-Y7: phù hợp với trẻ từ 7 tuổi.
PG: Nội dung có thể phù hợp với trẻ em, nhưng cha mẹ nên xem xét và hướng dẫn.
Phân tích tỷ trọng trên 7.290 title có thông tin phân loại độ tuổi (rating) cho thấy Netflix tập trung chủ yếu vào nhóm đối tượng người trưởng thành và thanh thiếu niên lớn. Cụ thể, nhãn TV-MA (dành cho người trưởng thành) chiếm tỷ trọng cao nhất với 37.2% (2.712 title), liền sau là TV-14 (dành cho khán giả từ 14 tuổi trở lên) chiếm 25.1% (1.831 title). Hai nhóm này cộng lại chiếm 62.3% cấu trúc rating trên nền tảng trong giai đoạn 2011-2020.
## Kết luận chương
Kết quả từ khám phá dữ liệu (EDA) trên 7.294 bản ghi hợp lệ cho thấy cấu trúc danh mục nội dung của Netflix từ năm 2011 đến năm 2020. Mức độ bổ sung nội dung tăng nhanh từ năm 2016 đến 2019 sau đó thì giảm 6.8% vào năm 2020. Trong quá trình này, Movie đóng vai trò nhóm nội dung chính, chi phối trực tiếp xu hướng tăng và giảm. Thêm vào đó, nội dung đa số có nhãn quốc tế, xuất xứ từ Mỹ và tập trung phục vụ khán giả trường thành (TV-MA).


# KHAI PHÁ DỮ LIỆU
## Tổng hợp các insight
Qua quá trình phân tích 7.294 bản ghi, nhóm rút ra các Insight quan trọng phản ánh cấu trúc và xu hướng của danh mục nội dung Netflix:
Insight 1 (Về xu hướng): Số lượng nội dung được bổ sung tăng rõ rệt và đạt mức cao nhất vào năm 2019 với 2.016 title, sau đó giảm 6,8% vào năm 2020.
Insight 2 (Về loại nội dung): Movie chiếm tỷ trọng lớn trong danh mục với 70,4% tổng số title và là thành phần đóng góp chính vào các biến động về tổng số title trong giai đoạn được phân tích.
Insight 3 (Về nội dung và đối tượng): Nhóm thể loại International Movies chiếm tỷ trọng lớn nhất với 32,1%, trong khi hai nhóm rating TV-MA và TV-14 chiếm tổng cộng 62,3% số nội dung có phân loại.
## Diễn biến và phân tích biến động trong dữ liệu
Từ các Insight trên, câu chuyện dữ liệu về danh mục Netflix trong giai đoạn 2011–2020 được xâu chuỗi như sau:
Giai đoạn bùng nổ (2016–2019): Số lượng nội dung được bổ sung tăng mạnh, từ 429 title vào năm 2016 lên mức cao nhất 2.016 title vào năm 2019.
Giai đoạn sụt giảm (2020): Sau giai đoạn tăng liên tục, tổng số nội dung được bổ sung giảm 137 title so với năm 2019, tương đương mức giảm 6,8%.
Nguyên nhân của biến động trong dữ liệu: Phân rã đóng góp theo từng năm cho thấy mức giảm tổng cộng 137 title được hình thành từ việc Movie giảm 140 title, trong khi TV Show tăng 3 title. Do đó, sự giảm số lượng Movie là thành phần đóng góp chính vào mức giảm ròng của tổng số title trong năm 2020.
Từ đó, có thể thấy các biến động về tổng số title trong giai đoạn được phân tích có mối liên hệ rõ rệt với sự thay đổi về số lượng Movie, trong khi TV Show có mức biến động nhỏ hơn.
## Giới hạn dữ liệu
Trong quá trình rút trích Insight và phân tích nguyên nhân của biến động trong dữ liệu, nhóm phân biệt rõ giữa thành phần đóng góp được quan sát trong dữ liệu và nguyên nhân thực tế ngoài dữ liệu. Số liệu cho phép xác định Movie là thành phần đóng góp chính vào mức giảm tổng số title năm 2020, nhưng không đủ bằng chứng để kết luận nguyên nhân sâu xa là do đại dịch COVID-19, thay đổi chiến lược kinh doanh hay các yếu tố bên ngoài khác. Tập dữ liệu chủ yếu mô tả đặc điểm và số lượng nội dung, không chứa đầy đủ các biến về hành vi người dùng, lượt xem, doanh thu, chi phí sản xuất hoặc bối cảnh kinh tế – xã hội.
# XÂY DỰNG MÔ HÌNH DỰ BÁO
## Mục tiêu xây dựng mô hình
Mục tiêu là sử dụng Linear Regression để mô tả xu hướng số lượng nội dung được thêm vào Netflix theo tháng và dự báo số nội dung trong 9 tháng đầu năm 2021.
Quy trình gồm:
Sử dụng dữ liệu từ 01/2011 đến 12/2020.
Huấn luyện mô hình trên toàn bộ dữ liệu 2011–2020.
Dự báo từ 01/2021 đến 09/2021.
Đối chiếu kết quả dự báo với dữ liệu thực tế năm 2021.
Đánh giá bằng MAE và RMSE.
Phân tích residual và trực quan hóa kết quả.
## Import thư viện
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("default")
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.transparent": False,
})

from sklearn.linear_model import LinearRegression
## Đọc dữ liệu
Dữ liệu được lấy từ fact_monthly_addition.csv. Hai biến chính gồm:
month_index: chỉ số thời gian của tháng.
monthly_additions: số lượng nội dung được thêm trong tháng.
Cột date_key được chuyển sang kiểu thời gian để phục vụ phân tích.
Dữ liệu gồm 120 tháng, từ 01/2011 đến 12/2020, với tổng cộng 7.294 nội dung.
Code đọc và chuẩn bị dữ liệu:
ROOT = Path.cwd()

if not (ROOT / "data").exists():
    ROOT = ROOT.parent

file_path = ROOT / "data" / "normalized" / "fact_monthly_addition.csv"

df = pd.read_csv(file_path)

df["month"] = pd.to_datetime(
    df["date_key"].astype(str),
    format="%Y%m%d",
)

df.head()
Sau khi đọc dữ liệu, nhóm kiểm tra phạm vi thời gian và số lượng nội dung:
print("Số tháng: ", len(df))
print("Từ tháng: ", df["month"].min())
print("Đến tháng: ", df["month"].max())
print("Tổng số nội dung: ", df["monthly_additions"].sum())
Kết quả:
Số tháng:  120
Từ tháng:  2011-01-01 00:00:00
Đến tháng:  2020-12-01 00:00:00
Tổng số nội dung:  7294
## Xác định biến đầu vào và biến cần dự báo
Trong mô hình, nhóm sử dụng:
X = month_index: làm biến độc lập, đại diện cho thời gian
y = monthly_additions: làm biến mục tiêu, đại diện cho số lượng nội dung được bổ sung trong mỗi tháng.
Việc lựa chọn month_index giúp mô hình biểu diễn xu hướng thay đổi của số lượng nội dung theo thời gian.
## Huấn luyện mô hình
Nhóm sử dụng LinearRegression với toàn bộ dữ liệu 2011–2020.
Mô hình có dạng:

Kết quả:
Hệ Beta 1: 1.8082991874435725
Hệ Beta 0: -46.810468319559234
MAE: 26.836197073870874

Trong đó:
: giá trị được mô hình dự đoán.
: month_index.
: hệ số chặn
: hệ số hồi quy
final_model = LinearRegression()

final_model.fit(
    df[["month_index"]],
    df["monthly_additions"]
)

df["fitted"] = final_model.predict(
    df[["month_index"]]
)

df["residual"] = (
    df["monthly_additions"] - df["fitted"]
)

training_mae = df["residual"].abs().mean()

print("Hệ Beta 1:", final_model.coef_[0])
print("Hệ Beta 0:", final_model.intercept_)
print("MAE:", training_mae)

## Dự báo 9 tháng tiếp theo
Code:
forecast_horizon = 9
first_future_index = df["month_index"].max() + 1

future = pd.DataFrame({
    "month_index": range(
        first_future_index,
        first_future_index + forecast_horizon
    )
})

future["month"] = pd.date_range(
    start=df["month"].max() + pd.offsets.MonthBegin(1),
    periods=forecast_horizon,
    freq="MS"
)

future["forecast"] = final_model.predict(
    future[["month_index"]]
)

future["forecast_rounded"] = (
    future["forecast"]
    .round()
    .astype(int)
)

future


Bảng 5.1 Kết quả dự báo số Title thêm vào từ 01/2021 - 09/2021
| month_index | month | forecast | forecast_rounded |
| --- | --- | --- | --- |
| 120 | 2021-01-01 | 170.185434 | 170 |
| 121 | 2021-02-01 | 171.993733 | 172 |
| 122 | 2021-03-01 | 173.802033 | 174 |
| 123 | 2021-04-01 | 175.610332 | 176 |
| 124 | 2021-05-01 | 177.418631 | 177 |
| 125 | 2021-06-01 | 179.226930 | 179 |
| 126 | 2021-07-01 | 181.035229 | 181 |
| 127 | 2021-08-01 | 182.843528 | 183 |
| 128 | 2021-09-01 | 184.651828 | 185 |

Mô hình dự báo số lượng nội dung có xu hướng tăng dần từ khoảng 170 nội dung vào tháng 01/2021 đến khoảng 185 nội dung vào tháng 09/2021.
## Thu thập dữ liệu thực tế năm 2021
Để đánh giá dự báo, nhóm sử dụng dữ liệu netflix_titles.csv và lấy các nội dung được thêm từ 01/2021 đến 09/2021.
actual_path = ROOT / "data" / "processed" / "netflix_titles.csv"
actual_source = pd.read_csv(
    actual_path,
    usecols=["date_added"]
)
actual_source["date_added"] = pd.to_datetime(
    actual_source["date_added"],
    errors="coerce"
)

actual_2021 = (
    actual_source[
        actual_source["date_added"].between(
            "2021-01-01",
            "2021-09-30"
        )
    ]
    .assign(
        month=lambda data: (
            data["date_added"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
    )
    .groupby("month")
    .size()
    .rename("actual")
    .reset_index()
)

Sau đó ghép dữ liệu thực tế với dữ liệu dự báo:
comparison = future.merge(
    actual_2021,
    on="month",
    how="left",
    validate="one_to_one"
)

## Tính phần sai khác và các chỉ số đánh giá
Phần sai khác được định nghĩa:

comparison["residual"] = (
    comparison["actual"] - comparison["forecast"]
)

mae = comparison["residual"].abs().mean()
rmse = (comparison["residual"].pow(2).mean()) ** 0.5

metrics = pd.DataFrame({
    "metric": ["MAE", "RMSE"],
    "value": [mae, rmse]
})

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

Kết quả:
MAE: 36.78
RMSE: 44.76
MAE và RMSE được tính trên 9 tháng thực tế từ 01/2021 đến 09/2021, dùng để đánh giá sai số dự báo ngoài mẫu.
## Biểu đồ xu hướng, đường hồi quy và dự báo
output_dir = ROOT / "data" / "model_outputs"
output_dir.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(14, 6))

# Dữ liệu và đường hồi quy của tập train
plt.scatter(
    df["month"],
    df["monthly_additions"],
    label="Thực tế 2011–2020",
    alpha=0.7
)
plt.plot(
    df["month"],
    df["fitted"],
    label="Đường hồi quy",
    color="black"
)

# Dự báo và dữ liệu thực tế năm 2021
plt.plot(
    comparison["month"],
    comparison["forecast"],
    "o--",
    label="Dự báo 2021",
    color="orange"
)
plt.scatter(
    comparison["month"],
    comparison["actual"],
    label="Thực tế 2021",
    color="green",
    marker="x"
)

plt.axvline(
    pd.Timestamp("2021-01-01"),
    color="gray",
    linestyle=":"
)

plt.title("Xu hướng, đường hồi quy và dự báo")
plt.xlabel("Thời gian")
plt.ylabel("Số nội dung")
plt.xlim(pd.Timestamp("2011-01-01"), pd.Timestamp("2021-09-30"))
plt.xticks(
    pd.date_range("2011-01-01", "2021-01-01", freq="YS"),
    range(2011, 2022)
)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    output_dir / "trend_and_data_9_months.png",
    dpi=180
)
plt.show()

Kết quả:

Hình 5.1. Biểu đồ Xu hướng, đường hồi quy và dự báo
Biểu đồ thể hiện đồng thời dữ liệu thực tế 2011–2020, đường hồi quy, kết quả dự báo năm 2021 và dữ liệu thực tế của 9 tháng năm 2021.
## Residual Plot
Residual plot được sử dụng để quan sát sai số của mô hình trên toàn bộ tập dữ liệu 2011–2020.
plt.figure(figsize=(14, 6))

plt.scatter(
    df["month"],
    df["residual"],
    color="teal"
)
plt.axhline(
    0,
    color="black",
    linestyle="--"
)

plt.title("Residual trên tập train 2011–2020")
plt.xlabel("Thời gian")
plt.ylabel("Residual = Thực tế − Fitted")
plt.xlim(pd.Timestamp("2011-01-01"), pd.Timestamp("2020-12-31"))
plt.xticks(
    pd.date_range("2011-01-01", "2020-01-01", freq="YS"),
    range(2011, 2021)
)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    output_dir / "residual_plot.png",
    dpi=180
)
plt.show()

Kết quả:

Hình 5.2. Biểu đồ Residual trên tập train 2011-2020
Residual được tính theo:

Biểu đồ giúp quan sát mức độ chênh lệch giữa giá trị thực tế và giá trị mà mô hình fitted trên dữ liệu lịch sử.
## Nhận xét
Mô hình được huấn luyện trên toàn bộ 120 tháng từ 01/2011 đến 12/2020 và dự báo 9 tháng từ 01/2021 đến 09/2021. Kết quả cho thấy Linear Regression mô tả được xu hướng tuyến tính tổng thể, nhưng dữ liệu thực tế năm 2021 vẫn có những dao động đáng kể so với đường dự báo. Hạn chế chính của mô hình là chỉ sử dụng month_index, do đó chưa mô hình hóa các yếu tố như mùa vụ và các biến động bất thường theo từng tháng.
## Kết luận
Kết quả cho thấy mô hình có khả năng phản ánh xu hướng tăng dài hạn nhưng chưa phù hợp để mô tả chính xác các biến động ngắn hạn theo từng tháng. Vì vậy, trong phạm vi đồ án, Linear Regression được sử dụng như một mô hình dự báo cơ sở và là cơ sở để minh họa phương pháp xây dựng, đánh giá và ngoại suy chuỗi dữ liệu theo thời gian.



# XÂY DỰNG DASHBOARD
## Mục tiêu và phạm vi xây dựng dashboard
Dashboard được xây dựng để chuyển các bảng dữ liệu đã chuẩn hóa và kết quả phân tích thành một giao diện trực quan, giúp người xem quan sát nhanh quy mô catalog Netflix, theo dõi xu hướng bổ sung nội dung và chủ động phân tích theo nhiều chiều. Dashboard không nhằm đo lường lượt xem, doanh thu hay mức độ yêu thích của khán giả; mọi chỉ số trong dashboard đều mô tả số lượng title có trong dữ liệu.
Phạm vi dashboard gồm năm trang: Tổng quan, Xu hướng nội dung, Phân bố nội dung theo quốc gia, Đặc điểm nội dung và Đánh giá mô hình dự báo. Các trang sử dụng chung phạm vi dữ liệu date_added từ năm 2011 đến năm 2020, trong đó các chỉ số title được tính theo show_id duy nhất để tránh double-count khi kết hợp với các bảng bridge.
Về mặt dữ liệu, dashboard sử dụng dim_title làm bảng trung tâm, kết hợp với dim_date, fact_monthly_addition và các bảng bridge_genre, bridge_country, bridge_director, bridge_actor. Cách tổ chức này giúp các biểu đồ thể hiện đúng quan hệ nhiều-nhiều giữa title với genre, country, director và actor.
## Kiến trúc thông tin và bố cục dashboard
Dashboard được tổ chức theo luồng từ tổng quát đến chi tiết. Người dùng bắt đầu tại trang Tổng quan để nắm các chỉ số chính, sau đó chuyển sang trang Xu hướng nội dung để phân tích diễn biến theo thời gian, trang Phân bố nội dung theo quốc gia để quan sát khía cạnh địa lý, trang Đặc điểm nội dung để tìm hiểu genre, rating và duration, cuối cùng là trang Đánh giá mô hình dự báo để xem kết quả ngoại suy và sai số.

Hình 6.1. Cấu trúc điều hướng và bố cục chung của dashboard
Thanh điều hướng bên trái sử dụng trạng thái màu để chỉ ra trang hiện tại. Cách bố trí này làm giảm số thao tác cần thiết khi chuyển giữa các góc nhìn và giúp người dùng duy trì được ngữ cảnh phân tích. Các bộ lọc được đặt ở khu vực bên phải hoặc khu vực cố định của từng trang, bảo đảm người dùng nhận biết được phạm vi đang áp dụng.
## Trang Tổng quan
Trang Tổng quan là điểm bắt đầu của dashboard, cung cấp một bức tranh khái quát về catalog trong phạm vi được chọn. Hàng KPI phía trên tóm tắt số title, số Movie, số TV Show, số quốc gia liên quan và năm có số lượng bổ sung cao nhất. Các KPI này giúp người xem nhận diện nhanh quy mô và cơ cấu dữ liệu trước khi đi sâu vào các trang còn lại.

Hình 6.2. Trang Tổng quan của dashboard
Biểu đồ tròn ở khu vực trung tâm thể hiện tỷ trọng Movie và TV Show. Biểu đồ thanh về rating cho phép so sánh số lượng title theo nhóm phân loại độ tuổi, trong khi biểu đồ theo giai đoạn phát hành cung cấp thêm bối cảnh về năm phát hành của nội dung. Bảng phân rã Movie và TV Show theo rating hỗ trợ đối chiếu cơ cấu giữa hai loại nội dung.
Trang này có slicer năm, rating và loại nội dung. Khi người dùng thay đổi phạm vi năm hoặc chọn một loại nội dung, các KPI và biểu đồ liên quan phải được cập nhật đồng thời. Total Titles cần dùng DISTINCTCOUNT(show_id), đồng thời kết quả ở trạng thái toàn bộ phạm vi phải đối chiếu được với 7.294 title trong báo cáo validation.
## Trang Xu hướng nội dung
Trang Xu hướng nội dung tập trung vào câu hỏi: số lượng title được thêm vào Netflix thay đổi như thế nào theo thời gian và loại nội dung nào đóng góp nhiều hơn vào biến động đó?

Hình 6.3. Trang Xu hướng nội dung và hierarchy drill-down
Treemap ở bên trái biểu diễn quy mô tương đối của các genre. International Movies, Dramas và Comedies chiếm các vùng lớn, cho thấy đây là những nhóm xuất hiện trên nhiều title trong dữ liệu. Vì một title có thể thuộc nhiều genre, treemap chỉ nên được đọc như số title liên quan đến từng genre; các vùng không được cộng lại để suy ra tổng catalog.
Biểu đồ đường ở góc trên bên phải thể hiện tổng số title được thêm theo năm. Đường xu hướng cho thấy lượng bổ sung tăng mạnh từ sau năm 2016, đạt đỉnh vào năm 2019 rồi giảm nhẹ trong năm 2020. Biểu đồ cột chồng bên dưới phân rã tổng số theo Movie và TV Show, qua đó cho thấy Movie là thành phần đóng góp chính vào mức tăng giai đoạn 2016–2019 và mức giảm năm 2020.
Trang sử dụng hierarchy year -> quarter -> month để hỗ trợ drill-down. Trục thời gian của các biểu đồ bổ sung được xây dựng từ date_added; release_year chỉ nên được dùng trong các biểu đồ mô tả năm phát hành, tránh trộn lẫn hai khái niệm thời gian.
## Trang Phân bố nội dung theo quốc gia
Trang này trình bày mối liên hệ địa lý của các title. Bản đồ ở khu vực phía trên cho phép nhận diện các quốc gia xuất hiện trong dữ liệu, còn hai biểu đồ phía dưới dùng để xếp hạng quốc gia và so sánh cơ cấu Movie với TV Show tại từng quốc gia.

Hình 6.4. Trang Phân bố nội dung theo quốc gia
United States đứng đầu về số title liên quan, tiếp theo là India và United Kingdom. Kết quả này phản ánh số title có trường country tương ứng trong dataset, không nên diễn giải thành thị phần sản xuất hoặc quy mô thị trường. Một title có thể được gắn với nhiều quốc gia, vì vậy các quốc gia được thể hiện qua bridge_country và các chỉ số phải dùng DISTINCTCOUNT(show_id).
Trường country_code được bổ sung để hỗ trợ nhận diện trên bản đồ. Khi mở dashboard trên môi trường khác, cần bảo đảm country được gán đúng Data Category là Country/Region và bản đồ đang dùng đúng trường country_code. Ngoài ra, country không có đầy đủ cho toàn bộ title; phạm vi bao phủ và số title thiếu country cần được nêu trong phần giới hạn của kết quả.
## Trang Đặc điểm nội dung
Trang Đặc điểm nội dung đi sâu vào cấu trúc của catalog theo genre, rating, số mùa và thời lượng. Trang này kết hợp nhiều loại biểu đồ để phục vụ các câu hỏi khác nhau thay vì chỉ lặp lại một chỉ số tổng hợp.

Hình 6.5. Trang Đặc điểm nội dung
Biểu đồ thanh phía trên bên trái cho thấy TV Show tập trung mạnh ở nhóm một mùa, trong khi số lượng giảm dần ở các nhóm nhiều mùa. Đây là đặc điểm mô tả của các title trong snapshot dữ liệu và không thể dùng để suy ra thời lượng xem hoặc mức độ thành công của chương trình.
Biểu đồ donut phía trên bên phải mô tả cơ cấu rating. TV-MA và TV-14 là hai nhóm chiếm tỷ trọng lớn trong các title có rating. Các title thiếu rating cần được loại khỏi mẫu số khi tính tỷ lệ rating, đồng thời phải báo cáo riêng để tránh làm sai lệch kết quả.
Heatmap genre theo năm cho phép quan sát các nhóm thể loại nổi bật thay đổi thế nào theo thời gian. Histogram duration thể hiện phân phối thời lượng của Movie; trường duration_seasons được dùng riêng cho TV Show. Việc tách hai loại biến này giúp tránh so sánh trực tiếp số phút của Movie với số mùa của TV Show.
## Trang Đánh giá mô hình dự báo
Trang Đánh giá mô hình dự báo trình bày kết quả ngoại suy số title được thêm vào theo tháng trong 9 tháng đầu năm 2021. Mô hình sử dụng Linear Regression với month_index làm biến đầu vào và monthly_additions làm biến mục tiêu. Kết quả cần được đọc như một baseline mô tả xu hướng, không phải dự báo chính thức của Netflix.

Hình 6.6. Trang Đánh giá mô hình dự báo
Ba KPI chính gồm MAE, RMSE và số tháng forecast. Với output hiện tại, MAE là 36,78, RMSE là 44,76 và horizon là 9 tháng. MAE cho biết sai số tuyệt đối trung bình, còn RMSE nhấn mạnh hơn các tháng có sai số lớn. KPI Growth Threshold là tham số tham chiếu để so sánh với đường tăng trưởng dự báo, không phải một chỉ số đánh giá độc lập của mô hình.
Biểu đồ Actual vs Forecast by Month so sánh số title thực tế và số title dự báo theo từng tháng. Forecast có xu hướng tăng đều, trong khi actual dao động mạnh hơn; vì vậy đường forecast phù hợp để mô tả xu hướng tuyến tính tổng thể nhưng chưa phản ánh tốt biến động ngắn hạn. Biểu đồ Prediction Error by Month thể hiện dấu và độ lớn sai số, còn biểu đồ Actual vs Forecast Relationship cho phép quan sát mức độ phân tán giữa hai đại lượng.
Khi diễn giải trang này, cần phân biệt dữ liệu lịch sử 2011–2020, forecast năm 2021 và actual 9 tháng đầu năm 2021. Không nên gộp forecast với actual để tạo thành một chuỗi quan sát duy nhất hoặc dùng kết quả này để kết luận về chiến lược kinh doanh của Netflix.
## Kết luận chương
Dashboard đã chuyển các kết quả tiền xử lý, phân tích khám phá và mô hình forecast thành một hệ thống trực quan gồm năm trang. Mỗi trang đảm nhiệm một vai trò riêng: Tổng quan cung cấp bức tranh chung; Xu hướng nội dung giải thích diễn biến theo thời gian; Phân bố theo quốc gia bổ sung góc nhìn địa lý; Đặc điểm nội dung mô tả genre, rating, duration và số mùa; Đánh giá mô hình dự báo trình bày xu hướng ngoại suy và sai số.

Việc kết hợp KPI, biểu đồ, bản đồ, slicer, drill-down, tooltip và cross-filtering giúp người xem tự khám phá dữ liệu thay vì chỉ tiếp nhận một kết luận cố định. Tuy nhiên, giá trị của dashboard phụ thuộc vào việc sử dụng đúng grain của từng bảng, tránh double-count title và giữ nhất quán giữa dữ liệu, measure, hình ảnh và phần diễn giải. Trong phạm vi của đề tài, dashboard là công cụ mô tả catalog Netflix trong snapshot dữ liệu 2011–2020, không phải công cụ đo lường hành vi người dùng hay dự báo kinh doanh.
# KẾT LUẬN
Đề tài đã xây dựng được quy trình phân tích dữ liệu tương đối đầy đủ, bắt đầu từ việc kiểm tra dữ liệu Netflix gốc, làm sạch và chuẩn hóa các trường, tổ chức dữ liệu thành các bảng phục vụ phân tích, rồi thực hiện phân tích khám phá, rút trích insight, xây dựng mô hình dự báo và phát triển dashboard Power BI. Việc tách các thuộc tính đa trị như thể loại, quốc gia, đạo diễn và diễn viên thành các bảng liên kết giúp mô hình dữ liệu rõ ràng hơn, đồng thời tạo điều kiện phân tích theo nhiều chiều. Qua quá trình thực hiện, nhóm có cơ hội vận dụng Python cho xử lý dữ liệu, các nguyên tắc mô hình hóa dữ liệu và kỹ thuật trực quan hóa tương tác vào một bài toán thực tế.
Trong phạm vi 7.294 title có ngày bổ sung thuộc giai đoạn 2011–2020, kết quả phân tích cho thấy số lượng nội dung được thêm vào tăng mạnh trong các năm cuối giai đoạn và đạt mức cao nhất vào năm 2019 với 2.016 title, trước khi giảm khoảng 6,8% vào năm 2020. Movie chiếm tỷ trọng lớn hơn TV Show; dữ liệu cũng cho thấy sự tập trung về số lượng ở một số quốc gia, thể loại và nhóm phân loại độ tuổi. Dashboard được tổ chức thành năm trang để người dùng theo dõi tổng quan, xu hướng theo thời gian, phân bố địa lý, đặc điểm nội dung và kết quả dự báo. Mô hình Linear Regression được sử dụng như một mô hình cơ sở để ngoại suy số title được bổ sung theo tháng; các chỉ số sai số giúp đánh giá kết quả định lượng thay vì chỉ quan sát đường dự báo. Những kết quả này mô tả cấu trúc danh mục trong bộ dữ liệu, không trực tiếp phản ánh lượt xem, doanh thu hay mức độ yêu thích của người dùng Netflix.
Bên cạnh các kết quả đạt được, nhóm nhận thấy đề tài vẫn còn một số hạn chế. Thứ nhất, bộ dữ liệu chủ yếu chứa thông tin mô tả danh mục và thời điểm bổ sung, không có các biến về lượt xem, thời lượng xem, doanh thu, chi phí sản xuất hoặc hành vi người dùng; vì vậy phạm vi kết luận chỉ giới hạn ở số lượng và đặc điểm của title trong dữ liệu. Thứ hai, dữ liệu được sử dụng là một bản chụp tại một thời điểm, nên không thể xem như lịch sử đầy đủ về toàn bộ danh mục Netflix qua các năm và có thể chưa phản ánh những thay đổi sau thời điểm thu thập. Thứ ba, mô hình dự báo hiện tại chỉ sử dụng chỉ mục thời gian trong hồi quy tuyến tính. Mô hình có thể biểu diễn xu hướng tuyến tính tổng quát nhưng chưa mô hình hóa rõ tính mùa vụ, điểm gãy xu hướng hay các biến động bất thường; do đó kết quả dự báo cần được xem là tham khảo, không phải dự báo chính thức của Netflix. Cuối cùng, các bảng thể loại và quốc gia có quan hệ đa trị nên số lượng theo từng nhóm có thể chồng lấn; chất lượng của một số trực quan hóa, đặc biệt là bản đồ, cũng phụ thuộc vào việc chuẩn hóa tên địa lý, thiết lập quan hệ và kiểm tra tương tác trong Power BI. Những hạn chế này cần được xem xét khi diễn giải kết quả và khi đánh giá mức độ khái quát của các insight.
Trong hướng phát triển tiếp theo, nhóm có thể mở rộng nguồn dữ liệu bằng cách bổ sung các bản chụp dữ liệu ở nhiều thời điểm để theo dõi biến động danh mục ổn định hơn, đồng thời kết hợp dữ liệu phù hợp về lượt xem, mức độ tương tác hoặc doanh thu nếu có nguồn đáng tin cậy và quyền sử dụng hợp lệ. Về mô hình dự báo, có thể bổ sung biến mùa vụ, đường trung bình trượt và so sánh Linear Regression với các phương pháp chuỗi thời gian như ARIMA hoặc Prophet bằng cách chia tập dữ liệu theo thứ tự thời gian và đánh giá trên cùng một giai đoạn ngoài mẫu. Về dữ liệu và dashboard, nên tiếp tục tự động hóa kiểm tra khóa, khóa ngoại, giá trị thiếu và các measure đếm title duy nhất; kiểm thử định kỳ Filter, Drill-down, Tooltip và Cross-filtering; cải thiện tooltip, chú thích và khả năng truy xuất từ insight về dữ liệu nguồn. Các cải tiến này sẽ giúp quy trình có khả năng tái lập tốt hơn, giảm nguy cơ sai lệch khi cập nhật dữ liệu và tăng giá trị sử dụng của dashboard.
Tóm lại, đề tài đã tạo được một nền tảng thực hành xuyên suốt từ xử lý dữ liệu đến phân tích, dự báo và trực quan hóa tương tác. Giá trị chính của sản phẩm là tổ chức và trình bày dữ liệu danh mục Netflix theo các góc nhìn có thể kiểm tra được, đồng thời minh họa cách xây dựng một mô hình dự báo cơ sở. Nhóm cũng nhận thức rằng độ tin cậy của kết quả phụ thuộc vào chất lượng và phạm vi của dữ liệu, cách thiết kế measure, việc kiểm thử dashboard và giới hạn của mô hình. Vì vậy, các kết quả trong báo cáo nên được hiểu trong đúng phạm vi nghiên cứu đã xác định; việc mở rộng dữ liệu, so sánh mô hình và kiểm định sản phẩm kỹ hơn là những bước cần thiết để phát triển đề tài thành một hệ thống phân tích có độ tin cậy và khả năng ứng dụng cao hơn.
TÀI LIỆU THAM KHẢO
I. Milovanović, D. Foures, and G. Vettigli, Python Data Visualization Cookbook, 2nd ed. Birmingham, UK: Packt Publishing, 2015.
J. Steele and N. Iliinsky, Eds., Beautiful Visualization: Looking at Data through the Eyes of Experts. Sebastopol, CA: O'Reilly Media, 2010.
Shivam Bansal, “Netflix Movies and TV Shows,” Kaggle. [Trực tuyến]. Có tại: https://www.kaggle.com/datasets/shivamb/netflix-shows. Truy cập ngày 09/10/2026.
Microsoft, “Power BI report and dashboard creation documentation,” Microsoft Learn. [Trực tuyến]. Có tại: https://learn.microsoft.com/en-us/power-bi/create-reports/. Truy cập ngày 09/10/2026.
pandas Development Team, “User Guide” pandas Documentation. [Trực tuyến]. Có tại: https://pandas.pydata.org/docs/user_guide/index.html. Truy cập ngày 09/10/2026.
scikit-learn developers, “LinearRegression”, scikit-learn Documentation. [Trực tuyến]. Có tại: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html. Truy cập ngày 09/10/2026.
scikit-learn developers, “Model evaluation,” scikit-learn Documentation. [Trực tuyến]. Có tại: https://scikit-learn.org/stable/modules/model_evaluation.html. Truy cập ngày 09/10/2026.