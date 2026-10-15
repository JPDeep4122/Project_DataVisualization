# Graph Report - Project_DataVisualization  (2026-10-15)

## Corpus Check
- 26 files · ~76,888 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 22 file(s) not represented in the graph (top: .csv 15, .ipynb 3, (none) 1)

## Summary
- 202 nodes · 353 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Relational Data Normalization
- Academic References & Rubrics
- Data Cleaning Pipeline
- ETL Pipeline & Validation
- Project Report & Dashboard Architecture
- Data Auditing Engine
- System Architecture & Workflow
- SQLite Database Persistence
- Content Volume Forecast Model
- Team Roles & Responsibilities
- Model Residual & Error Analysis

## God Nodes (most connected - your core abstractions)
1. `Data Pipeline and Analytics Workflow Diagram` - 16 edges
2. `run_pipeline()` - 13 edges
3. `normalize_data()` - 12 edges
4. `run_audit()` - 10 edges
5. `build_report()` - 10 edges
6. `clean_netflix_titles()` - 9 edges
7. `Netflix IDV Project Overview` - 8 edges
8. `load_csv_to_database()` - 7 edges
9. `validate_database()` - 7 edges
10. `main()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Netflix IDV Final Project Report PDF` --semantically_similar_to--> `Research Scope and Timeline Methodology`  [INFERRED] [semantically similar]
  docs/26_AnhAnhHoc_IDV_REPORT.pdf → graphify-out/converted/26_AnhAnhHoc_IDV_REPORT_9b28c1f3.md
- `Research Scope and Timeline Methodology` --semantically_similar_to--> `Catalog Scope and Counting Rules`  [INFERRED] [semantically similar]
  graphify-out/converted/26_AnhAnhHoc_IDV_REPORT_9b28c1f3.md → README.md
- `Seven-Table Relational Schema Design` --semantically_similar_to--> `Normalized Relational Schema`  [INFERRED] [semantically similar]
  graphify-out/converted/26_AnhAnhHoc_IDV_REPORT_9b28c1f3.md → README.md
- `Monthly Additions Forecast Model` --semantically_similar_to--> `Linear Regression Forecast Baseline`  [INFERRED] [semantically similar]
  graphify-out/converted/26_AnhAnhHoc_IDV_REPORT_9b28c1f3.md → README.md
- `Five-Page Power BI Interactive Design` --semantically_similar_to--> `Power BI 5-Page Analytical Dashboard`  [INFERRED] [semantically similar]
  graphify-out/converted/26_AnhAnhHoc_IDV_REPORT_9b28c1f3.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **End-to-End Pipeline and Analytical System** — readme_pipeline_architecture, readme_data_model, readme_linear_regression_model, readme_power_bi_dashboard [EXTRACTED 1.00]
- **Relational Modeling and Data Quality Assurance** — graphify_out_converted_26_anhanhhoc_idv_report_9b28c1f3_data_audit_and_cleaning, graphify_out_converted_26_anhanhhoc_idv_report_9b28c1f3_data_model_architecture, graphify_out_converted_26_anhanhhoc_idv_report_9b28c1f3_validation_rules [EXTRACTED 1.00]
- **Three-Tier Architecture Team Role Allocation** — docs_team_roles_frontend_ui_ux, docs_team_roles_backend_service, docs_team_roles_database_repo, docs_team_roles_devops_qa [EXTRACTED 1.00]
- **Nghiên cứu tham khảo học thuật phân tích dữ liệu Netflix** — docs_references_báo_cáo_cuối_kỳ_phân_tích_dữ_liệu_hệ_thống_phim_trên_netflix_ippa233277_studocu, docs_references_báo_cáo_đồ_án_kết_thúc_môn_phân_tích_dữ_liệu_kinh_doanh_netflix_movies_tv_studocu, docs_references_phân_tích_dữ_liệu_phim_và_chương_trình_truyền_hình_vjp_studocu [INFERRED 0.85]
- **Khung 4 tiêu chuẩn chấm điểm đồ án IDV** — docs_rubric_rubric_idv_cuối_kỳ_criteria_data_preprocessing, docs_rubric_rubric_idv_cuối_kỳ_criteria_dashboard_design, docs_rubric_rubric_idv_cuối_kỳ_criteria_insight_forecasting, docs_rubric_rubric_idv_cuối_kỳ_criteria_scientific_report_demo [EXTRACTED 1.00]
- **Bộ mô hình học máy phân cụm và dự báo trên dữ liệu phim Netflix** — docs_references_báo_cáo_đồ_án_kết_thúc_môn_phân_tích_dữ_liệu_kinh_doanh_netflix_movies_tv_studocu_linear_regression_duration, docs_references_báo_cáo_đồ_án_kết_thúc_môn_phân_tích_dữ_liệu_kinh_doanh_netflix_movies_tv_studocu_kmeans_clustering, docs_references_báo_cáo_đồ_án_kết_thúc_môn_phân_tích_dữ_liệu_kinh_doanh_netflix_movies_tv_studocu_random_forest_classification [EXTRACTED 1.00]

## Communities (13 total, 2 thin omitted)

### Community 0 - "Relational Data Normalization"
Cohesion: 0.10
Nodes (13): create_bridge_actor(), create_bridge_country(), create_bridge_director(), create_bridge_genre(), create_dim_date(), create_dim_title(), create_fact_monthly_addition(), get_country_code() (+5 more)

### Community 1 - "Academic References & Rubrics"
Cohesion: 0.11
Nodes (27): Báo cáo cuối kỳ: Phân tích dữ liệu hệ thống phim trên Netflix (HCMUTE), Phân tích phân phối nội dung Movie vs TV Show theo năm và diễn viên đạo diễn, Thao tác CRUD và chuẩn hóa dữ liệu trên Pandas DataFrame, Quy trình làm sạch dữ liệu Netflix (Xử lý null, duplicates, chuẩn hóa kiểu dữ liệu), Bộ phương thức trực quan hóa phân phối và tương quan phim (11 hàm plot), Giao diện ứng dụng Tkinter tương tác người dùng và hiển thị đồ thị, Báo cáo Đồ án Phân tích Dữ liệu Kinh doanh: Netflix Movies & TV Shows (HUFLIT), Thông tin thị trường nội dung Netflix (Tỷ lệ 69.6% Movie, 30.4% TV Show, Top Mỹ & Ấn Độ) (+19 more)

### Community 2 - "Data Cleaning Pipeline"
Cohesion: 0.14
Nodes (9): clean_all_data(), clean_date_added(), clean_duration(), clean_netflix_titles(), clean_release_year(), clean_text_columns(), cleaning_summary(), save_cleaned_data() (+1 more)

### Community 3 - "ETL Pipeline & Validation"
Cohesion: 0.15
Nodes (9): run_pipeline(), build_report(), load_normalized_data(), main(), save_report(), validate_business_rules(), validate_foreign_keys(), validate_primary_keys() (+1 more)

### Community 4 - "Project Report & Dashboard Architecture"
Cohesion: 0.12
Nodes (19): Report Video Demo and GitHub Repository Links, Netflix IDV Final Project Report PDF, Kaggle Netflix Movies and TV Shows Dataset, Python Data Visualization Cookbook 2nd Edition, Microsoft Power BI Documentation, Scikit-Learn Documentation on Linear Models and Model Evaluation, Beautiful Visualization: Looking at Data through the Eyes of Experts, Five-Page Power BI Interactive Design (+11 more)

### Community 5 - "Data Auditing Engine"
Cohesion: 0.22
Nodes (7): audit_date(), audit_duplicate(), audit_key(), audit_multivalue(), audit_scope(), audit_structure(), run_audit()

### Community 6 - "System Architecture & Workflow"
Cohesion: 0.23
Nodes (16): Data Pipeline and Analytics Workflow Diagram, Data Auditing (audit.py), Cleaned and Normalized Dataset (Các bảng dữ liệu đã được làm sạch và chuẩn hóa), Data Cleaning (cleanning.py), Interactive Dashboard, Database Loading (database.py), Exploratory Data Analysis (EDA), Staged ETL and Quality Assurance Boundary (+8 more)

### Community 7 - "SQLite Database Persistence"
Cohesion: 0.26
Nodes (4): create_database(), load_csv_to_database(), main(), validate_database()

### Community 8 - "Content Volume Forecast Model"
Cohesion: 0.36
Nodes (7): Thực tế 2021 (Actual 2021 Evaluation Data), Xu hướng, đường hồi quy và dự báo (Trend, Regression Line and Forecast Chart), Số nội dung (Content Volume Metric), Dự báo 2021 (Forecast 2021 for 9 Months), Thực tế 2011–2020 (Historical Actual Data), Đường hồi quy (Linear Regression Trend Line), Thời gian (Time Horizon 2011-2021)

### Community 9 - "Team Roles & Responsibilities"
Cohesion: 0.33
Nodes (6): Backend Developer (Controller and Validation), Backend Developer (Core Business Logic), Database and Repository (Data Access), Git Master, DevOps and QA Lead, Frontend Developer (Logic and API Integration), Frontend Developer (UI/UX Layout)

### Community 10 - "Model Residual & Error Analysis"
Cohesion: 0.50
Nodes (5): Residual Plot Train 2011-2020, Autocorrelation and Systematic Bias 2011-2016, Heteroscedasticity and Variance Increase Post-2016, Residual Metric (Actual - Fitted), Training Period 2011-2020

## Knowledge Gaps
- **17 isolated node(s):** `Frontend Developer (UI/UX Layout)`, `Database and Repository (Data Access)`, `Git Master, DevOps and QA Lead`, `Automated Post-Normalization Integrity Verification`, `Kaggle Netflix Movies and TV Shows Dataset` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 72 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_pipeline()` connect `ETL Pipeline & Validation` to `Relational Data Normalization`, `Data Cleaning Pipeline`, `SQLite Database Persistence`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `run_pipeline()` (e.g. with `clean_netflix_titles()` and `save_cleaned_data()`) actually correct?**
  _`run_pipeline()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Frontend Developer (UI/UX Layout)`, `Database and Repository (Data Access)`, `Git Master, DevOps and QA Lead` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Relational Data Normalization` be split into smaller, more focused modules?**
  _Cohesion score 0.10227272727272728 - nodes in this community are weakly interconnected._
- **Why does `normalize_data()` connect `Relational Data Normalization` to `ETL Pipeline & Validation`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `Academic References & Rubrics` be split into smaller, more focused modules?**
  _Cohesion score 0.10582010582010581 - nodes in this community are weakly interconnected._
- **Should `Data Cleaning Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.14245014245014245 - nodes in this community are weakly interconnected._