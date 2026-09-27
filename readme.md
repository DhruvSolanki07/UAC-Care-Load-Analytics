# UAC Care Load Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end analytical pipeline and interactive dashboard for examining system capacity, care pipeline dynamics, transfers, discharges, and net care-load pressure in the Unaccompanied Alien Children (UAC) care system.

---

## 📌 Project Overview

The Unaccompanied Alien Children (UAC) care system involves complex inter-agency coordination between **Customs and Border Protection (CBP)** (custody & apprehension) and the **Department of Health and Human Services (HHS)** (care, shelter, & sponsor placement). 

This project provides:
- **System Load Modeling:** Tracking historical aggregate care load across both agencies.
- **Pipeline Dynamics:** Comparing intake/apprehensions, cross-agency transfers, and final discharges.
- **Pressure Analysis:** Measuring net intake strain and identifying capacity bottleneck periods.
- **Forecasting & Trend Analysis:** Modeling future care demand and seasonal patterns.
- **Interactive Visualizations:** A Streamlit dashboard for dynamic filtering and exploration.

---

## 🎯 Key Objectives

- **Quantify System Load:** Compute total system load across CBP custody and HHS care facilities.
- **Analyze Inter-Agency Handoffs:** Measure latency and flow efficiency between CBP transfer-outs and HHS intake.
- **Identify Surge & Pressure Windows:** Highlight dates where net intake exceeds system discharge capacity.
- **Evaluate Data Integrity:** Implement anomaly detection rules to flag invalid data or reporting gaps.
- **Support Decision-Making:** Deliver publication-ready research reports and an interactive web interface.

---

## 📊 Dataset & Observations

- **Source:** HHS Unaccompanied Children Program Data
- **Observation Window:** January 2023 – December 2025
- **Features Tracked:**
  - Children apprehended and placed in CBP custody
  - Children in CBP custody
  - Children transferred out of CBP custody
  - Children in HHS Care
  - Children discharged from HHS Care to sponsors
  - Computed Metrics: `total_system_load`, `net_intake`, `care_load_growth_rate`, 7-day rolling averages, and data quality flags.

---

## 🛠️ Technology Stack

- **Data Processing & Analytics:** Python, Pandas, NumPy
- **Visualization:** Plotly Express & Plotly Graph Objects, Matplotlib, Seaborn
- **Statistical Modeling & Forecasting:** Scikit-Learn, Statsmodels
- **Dashboard & UI:** Streamlit
- **Notebooks & Reproducibility:** Jupyter Notebooks
- **Reporting:** ReportLab, WeasyPrint / HTML-to-PDF pipeline

---

## 📂 Project Structure

```text
UAC-Care-Load-Analytics/
├── .gitignore                     # Git ignore rules for environments & caches
├── app.py                         # Interactive Streamlit analytics dashboard
├── requirements.txt               # Python package dependencies
├── readme.md                      # Project documentation and run guide
├── data/
│   ├── raw/                       # Original raw HHS dataset
│   │   └── HHS_Unaccompanied_Alien_Children_Program.csv
│   └── processed/                 # Cleaned and feature-engineered datasets
│       ├── uac_care_cleaned.csv
│       ├── uac_cleaned.csv
│       └── uac_features.csv
├── models/                        # Serialized models and checkpoints (.gitkeep)
├── notebooks/                     # Step-by-step analytical notebooks
│   ├── 01_data_cleaning.ipynb     # Data parsing, missing values, & cleaning
│   ├── 02_feature_engineering.ipynb # System load & flow indicators
│   ├── 03_eda.ipynb               # Exploratory data analysis & trends
│   ├── 04_pressure_analysis.ipynb # Bottleneck & capacity stress analysis
│   └── 05_forecasting.ipynb       # Time-series modeling & projections
├── reports/                       # Generated documentation & reports
│   ├── executive_summary.pdf      # High-level findings executive summary
│   ├── UAC_researchPaper.pdf      # Detailed research paper
│   └── figures/                   # High-res analytical charts (fig1–fig6)
├── scripts/                       # Report generation & compilation utilities
│   ├── build_exec_summary.py
│   └── build_paper_html.py
└── src/                           # Modular reusable Python source code
    └── data_cleaning.py
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/DhruvSolanki07/UAC-Care-Load-Analytics.git
cd UAC-Care-Load-Analytics
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Interactive Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to explore the dashboard.

---

## 📈 Key Research Findings

1. **HHS Carries the Bulk of System Load:** Over 85% of children in the pipeline are under HHS care rather than CBP custody, reflecting lengthier sponsorship verification compared to initial processing.
2. **Net Intake Surges:** Care-load stress surges when apprehension rates spike without a commensurate increase in sponsor discharge throughput.
3. **Data Gaps:** Calendar non-reporting days require robust handling (non-zero interpolation) to avoid distorting flow metrics.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).