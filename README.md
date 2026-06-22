# 📊 Indian Mutual Fund Industry — Data Analytics Capstone

**Organisation:** Bluestock Fintech  
**Period Covered:** January 2022 – March 2025  
**Data Source:** AMFI India (amfiindia.com)  
**Version:** v1.0

---

## Project Overview

This project delivers an end-to-end data analytics pipeline and reporting suite for the Indian Mutual Fund industry. It covers eight analytical dimensions: AUM growth, SIP inflows, folio count, investor demographics, NAV performance, sector allocation, geographic distribution, and category-wise net inflows.

### Deliverables

| File | Description |
|------|-------------|
| `Final_Report.pdf` | 17-page professional PDF report with all findings, charts, and recommendations |
| `Bluestock_MF_Presentation.pptx` | 12-slide executive presentation |
| `run_pipeline.py` | Master execution script — runs all 5 pipeline stages |
| `README.md` | This file |
| `notebooks/01_data_ingestion.ipynb` | Stage 1: Data fetch & raw storage |
| `notebooks/02_data_cleaning.ipynb` | Stage 2: Cleaning, deduplication, type casting |
| `notebooks/03_eda_analysis.ipynb` | Stage 3: EDA, visualisations |
| `notebooks/04_Fund_Performance_Analytics.ipynb` | Stage 4: Risk-return metrics |
| `notebooks/05_advanced_analytics.ipynb` | Stage 5: Cohort analysis, T30/B30, ML features |

---

## Quick Start

### Prerequisites

```bash
# Python 3.10+
pip install pandas numpy matplotlib seaborn plotly scipy scikit-learn \
            jupyter pyarrow fastparquet requests tqdm pyyaml

# Optional (for dashboard)
pip install dash plotly-dash
```

### Clone & Setup

```bash
git clone https://github.com/bluestock/mf-capstone.git
cd mf-capstone
pip install -r requirements.txt
```

### Run the Full Pipeline

```bash
python run_pipeline.py
```

This executes all 5 stages in sequence. Use `--stage N` to run a specific stage:

```bash
python run_pipeline.py --stage 3   # Run only EDA analysis
python run_pipeline.py --from 2    # Run from stage 2 onwards
```

### Run Individual Notebooks

```bash
jupyter notebook notebooks/01_data_ingestion.ipynb
```

Or convert and run headlessly:

```bash
jupyter nbconvert --to notebook --execute notebooks/03_eda_analysis.ipynb
```

---

## ETL Architecture

```
AMFI India (Public URLs)
        │
        ▼
[Stage 01] data_ingestion.ipynb    → data/raw/*.csv
        │
        ▼
[Stage 02] data_cleaning.ipynb     → data/clean/*.parquet
        │
        ▼
[Stage 03] eda_analysis.ipynb      → outputs/charts/*.png
        │
        ▼
[Stage 04] Fund_Performance_Analytics.ipynb → outputs/analytics/*.parquet
        │
        ▼
[Stage 05] advanced_analytics.ipynb → outputs/advanced/*.parquet
```

Each stage writes intermediate outputs to enable point-in-time restarts without re-fetching upstream data.

---

## Dataset Descriptions

| Dataset | Source URL Pattern | Format | Frequency |
|---------|-------------------|--------|-----------|
| NAV History | `amfiindia.com/spages/NAVAll.txt` | Text/CSV | Daily |
| AUM by Fund House | AMFI monthly reports | CSV | Monthly |
| SIP Inflows | AMFI SIP data portal | CSV | Monthly |
| Folio Count | AMFI statistics page | CSV | Monthly |
| Investor Demographics | AMFI investor data | Excel | Quarterly |
| Category Net Inflows | AMFI category report | CSV | Monthly |
| Sector Allocation | Scheme-level disclosure | CSV | Monthly |

---

## Key Findings Summary

1. **SIP Inflows ~3x** — ₹11,000 Cr (Jan 2022) → ₹31,002 Cr (early 2026)
2. **Folio Count 2x** — 13.26 Cr → 26.12 Cr in under 4 years
3. **Millennial Dominance** — 26–35 age group = 41%; 26–45 = ~66% of investors
4. **SBI MF Leads** — ₹12.5 Lakh Crore AUM in 2025
5. **Liquid Fund Anomaly** — Net inflows 10x higher than any equity category (institutional)
6. **Banking + IT = 37%** of equity fund sector allocation
7. **T30:B30 = 66:34** — Meaningful B30 penetration underway
8. **SIP Uniformity** — Median ₹10–20K across ALL age groups (product-driven, not demographic)
9. **Low Cross-Fund Correlation** — Genuine diversification opportunity in multi-fund portfolios
10. **Pan-India SIP** — Punjab leads Maharashtra; states within 15% of each other

---

## Project Structure

```
mf-capstone/
├── README.md
├── run_pipeline.py          # Master orchestration script
├── config.yaml              # Pipeline configuration
├── requirements.txt
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_Fund_Performance_Analytics.ipynb
│   ├── 05_advanced_analytics.ipynb
│   └── EDA_Findings.ipynb   # Summary findings notebook
├── data/
│   ├── raw/                 # Stage 01 outputs (CSV)
│   └── clean/               # Stage 02 outputs (Parquet)
├── outputs/
│   ├── charts/              # Stage 03 PNG charts
│   ├── analytics/           # Stage 04 performance data
│   └── advanced/            # Stage 05 advanced analytics
├── reports/
│   ├── Final_Report.pdf
│   └── Bluestock_MF_Presentation.pptx
└── dashboard/
    └── app.py               # Dash dashboard (optional)
```

---

## Dashboard

A Plotly Dash interactive dashboard is available under `dashboard/app.py`.

### Run Locally

```bash
cd dashboard
python app.py
# Open http://localhost:8050
```

### Publish to Tableau Public / Power BI Service

- Export Parquet files to CSV: `python scripts/export_csv.py`
- Import into Tableau Public or Power BI Desktop
- Publish from within the respective application

Dashboard URL (after publish): _Add your URL here_

---

## Git Workflow

```bash
# Final commit and tag
git add .
git commit -m "Final: Complete Bluestock MF Capstone"
git tag v1.0
git push origin main --tags
```

---

## Self-Review Checklist

- [x] All 5 pipeline stages run without errors
- [x] All 10 EDA findings documented with visualisations
- [x] Final_Report.pdf — 17 pages, professional formatting
- [x] Presentation — 12 slides, executive-ready
- [x] README.md — complete setup and run instructions
- [x] Code — docstrings added, debug prints removed
- [x] run_pipeline.py — master execution script functional
- [x] GitHub — v1.0 tag ready to push

---

## Limitations

- Investor demographic data is quarterly; monthly values are interpolated
- NAV dataset may have survivorship bias (merged/wound-up schemes excluded)
- Liquid fund dominance in inflow data reflects institutional behaviour, not retail
- No live benchmark data for precise alpha/beta computation

---

## License & Attribution

**Data:** AMFI India — publicly available under AMFI's data sharing policy  
**Code:** © 2025 Bluestock Fintech. Internal use only.  
**Report:** Prepared for Bluestock Fintech Capstone Program, June 2025

> This analysis is for informational purposes only and does not constitute investment advice.
