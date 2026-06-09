# 🚀 EDA ANALYSIS - QUICK START GUIDE

## ⚡ 30-Second Setup

```powershell
# 1. Navigate to project
cd "C:\Users\pushk\OneDrive\Desktop\AIML\Blue Stocks\mutual-fund-analytics"

# 2. Activate environment
.\.venv\Scripts\Activate.ps1

# 3. Launch notebook
jupyter notebook notebooks/03_eda_analysis.ipynb
```

---

## 📊 CELL EXECUTION GUIDE

### **Phase 1: Setup (Cells 1-3)**
```
✅ Cell 1: Import all libraries
✅ Cell 2: Load 6 datasets (NAV, AUM, SIP, Category, Investor, Portfolio)
✅ Cell 3: Convert dates and validate data
```
**⏱️ Time**: ~5 seconds

---

### **Phase 2: Overview (Cells 4-5)**
```
📝 Markdown: Notebook introduction
📝 Markdown: Chart 1 header
```
**⏱️ Time**: ~0 seconds (markdown only)

---

### **Phase 3: Chart 1 - NAV Trends (Cells 6-7)**
```
✅ Cell 6: Generate Plotly line chart with 40 schemes
   - 2023 Bull Run (green zone, +35-45%)
   - 2024 Correction (red zone, -15-22%)
✅ Cell 7: Export to HTML (01_nav_trends_all_schemes.html)
```
**⏱️ Time**: ~3 seconds | **Output**: Interactive chart + PNG

---

### **Phase 4: Chart 2 - AUM by Fund House (Cells 8-9)**
```
✅ Cell 8: Seaborn grouped bar chart
   - X-axis: Fund Houses
   - Y-axis: AUM (₹ Lakh Cr)
   - Colors: Yearly breakdown
   - Highlight: SBI ₹12.5L Cr
✅ Cell 9: Export to PNG (02_aum_by_fund_house.png)
```
**⏱️ Time**: ~2 seconds | **Output**: High-res static chart

---

### **Phase 5: Chart 3 - SIP Inflows (Cells 10-11)**
```
📝 Markdown: Chart 3 header
✅ Cell 10: Plotly time-series chart
   - Monthly SIP Jan 2022 - Dec 2025
   - All-time high annotation: ₹31,002 Cr (Dec 2025)
   - Interactive hover tooltips
   - Growth calculation: +148%
✅ Cell 11: Export to HTML (03_sip_inflows_monthly.html)
```
**⏱️ Time**: ~2 seconds | **Output**: Interactive chart

---

### **Phase 6: Chart 4 - Category Heatmap (Cells 12-13)**
```
📝 Markdown: Chart 4 header
✅ Cell 12: Seaborn heatmap
   - X-axis: Months (Jan 2022 - Dec 2025)
   - Y-axis: Fund Categories (Equity, Debt, Hybrid)
   - Color: Inflow intensity
   - Yellow-Blue gradient
✅ Cell 13: Export to PNG (04_category_inflow_heatmap.png)
```
**⏱️ Time**: ~2 seconds | **Output**: Static heatmap

---

### **Phase 7: Demographics (Cells 14-18)**
```
📝 Markdown: Demographics header

5A - Age Distribution Pie:
✅ Cell 14: Plotly donut chart
   - Investor count by age group
   - Export to HTML (05a_age_distribution_pie.html)

5B - SIP by Age Box Plot:
✅ Cell 15: Plotly box plot
   - SIP amount distribution
   - By age group segments
   - Export to HTML (05b_sip_by_age_boxplot.html)

5C - Gender Distribution:
✅ Cell 16: Plotly pie chart
   - Gender split
   - Export to HTML (05c_gender_distribution.html)
```
**⏱️ Time**: ~3 seconds | **Output**: 3 interactive charts

---

### **Phase 8: Geographic Distribution (Cells 19-21)**
```
📝 Markdown: Geography header

6A - Top 15 States:
✅ Cell 17: Plotly horizontal bar
   - Total SIP by state
   - Viridis color gradient
   - Export to HTML (06a_state_distribution_top15.html)

6B - City Tier:
✅ Cell 18: Plotly pie chart
   - T1 vs T2 vs B30 split
   - Export to HTML (06b_city_tier_distribution.html)
```
**⏱️ Time**: ~2 seconds | **Output**: 2 interactive charts

---

### **Phase 9: Folio Count Growth (Cells 22-24)**
```
📝 Markdown: Chart 7 header
✅ Cell 19: Plotly line chart
   - Start: 13.26 Cr (Jan 2022)
   - End: 26.12 Cr (Dec 2025)
   - Growth: +100%
   - Milestone dashed lines
✅ Cell 20: Export to HTML (07_folio_count_growth.html)
```
**⏱️ Time**: ~2 seconds | **Output**: Interactive chart

---

### **Phase 10: Correlation Matrix (Cells 25-27)**
```
📝 Markdown: Chart 8 header
✅ Cell 21: Calculate daily returns correlation
   - Top 10 schemes
   - Pairwise correlation matrix
✅ Cell 22: Seaborn heatmap
   - RdBu color scale
   - Annotation enabled
   - Statistics: Mean=0.75, Max=0.92
✅ Cell 23: Export to PNG (08_return_correlation_matrix.png)
```
**⏱️ Time**: ~2 seconds | **Output**: High-res heatmap

---

### **Phase 11: Sector Allocation (Cells 28-30)**
```
📝 Markdown: Chart 9 header
✅ Cell 24: Aggregate sector weights
   - From portfolio_holdings.csv
   - Top 10 sectors
   - Banking 28%, IT 18%, Pharma 12%
✅ Cell 25: Plotly donut chart
   - Interactive legend
   - Color-coded segments
✅ Cell 26: Export to HTML (09_sector_allocation_donut.html)
```
**⏱️ Time**: ~2 seconds | **Output**: Interactive chart

---

### **Phase 12: Key Findings (Cells 31-41)**
```
📝 Finding 1: 2023 Bull Run (Chart reference: Chart 1)
📝 Finding 2: 2024 Volatility (Chart reference: Chart 1)
📝 Finding 3: SIP Momentum (Chart reference: Chart 3)
📝 Finding 4: Market Concentration (Chart reference: Chart 2)
📝 Finding 5: Equity Preference (Chart reference: Chart 4)
📝 Finding 6: Age Patterns (Chart reference: Charts 5A & 5B)
📝 Finding 7: Metro Dominance (Chart reference: Chart 6A)
📝 Finding 8: Correlation Analysis (Chart reference: Chart 8)
📝 Finding 9: Folio Growth (Chart reference: Chart 7)
📝 Finding 10: Sector Rotation (Chart reference: Chart 9)
```
**⏱️ Time**: ~0 seconds (markdown cells)

---

### **Phase 13: Summary (Cell 42)**
```
✅ Final Summary Cell:
   - Print analysis completion status
   - List all generated files
   - Display key statistics
   - Execution summary
```
**⏱️ Time**: ~1 second

---

## ⏱️ TOTAL EXECUTION TIME

| Phase | Time |
|-------|------|
| Setup & Load | ~5 sec |
| NAV Trends | ~3 sec |
| AUM Charts | ~2 sec |
| SIP Trends | ~2 sec |
| Category Heatmap | ~2 sec |
| Demographics | ~3 sec |
| Geography | ~2 sec |
| Folio Growth | ~2 sec |
| Correlation | ~2 sec |
| Sectors | ~2 sec |
| Findings | ~0 sec |
| Summary | ~1 sec |
| **TOTAL** | **~26 seconds** |

✅ **Full notebook execution: <1 minute**

---

## 📊 OUTPUT FILES GENERATED

After running all cells, you'll have:

### **Interactive HTML Charts** (8 files)
```
reports/
├── 01_nav_trends_all_schemes.html          (Zoomable, hoverable)
├── 03_sip_inflows_monthly.html             (Time-series with tooltip)
├── 05a_age_distribution_pie.html           (Clickable donut)
├── 05b_sip_by_age_boxplot.html             (Box plot analysis)
├── 05c_gender_distribution.html            (Gender split pie)
├── 06a_state_distribution_top15.html       (Top states bar)
├── 06b_city_tier_distribution.html         (City tier pie)
├── 09_sector_allocation_donut.html         (Sector breakdown)
└── 07_folio_count_growth.html              (Folio trend)
```

### **Static PNG Charts** (5 files)
```
reports/
├── 02_aum_by_fund_house.png                (300 DPI, printable)
├── 04_category_inflow_heatmap.png          (300 DPI heatmap)
├── 08_return_correlation_matrix.png        (300 DPI matrix)
├── 07_folio_count_growth.png               (300 DPI)
└── nav_trend_analysis.png                  (300 DPI)
```

---

## 🎯 VERIFICATION CHECKLIST

After execution, verify you have:

- [ ] Notebook executed without errors
- [ ] 34 cells completed
- [ ] 8-9 HTML files in `reports/` (interactive charts)
- [ ] 5 PNG files in `reports/` (static exports)
- [ ] All charts displaying properly
- [ ] Summary statistics printed at end
- [ ] No data load warnings/errors

---

## ⚠️ TROUBLESHOOTING

### **Missing Data Files**
```
Error: FileNotFoundError: data/processed/*.csv
Solution: Run ETL pipeline first
  python scripts/etl_pipeline.py
```

### **Library Import Errors**
```
Error: ModuleNotFoundError: plotly
Solution: Install missing packages
  pip install -r requirements.txt
```

### **Chart Not Rendering**
```
Error: Figure not displaying
Solution: Ensure Jupyter has proper kernel
  jupyter notebook --ip=127.0.0.1
```

### **Export Permission Error**
```
Error: Permission denied reports/
Solution: Check folder permissions
  icacls "reports" /grant:r "%username%":F
```

---

## 💡 PRO TIPS

1. **Run individually**: Don't need to run all cells - each chart is independent
2. **Export as PDF**: Open HTML in browser → Print as PDF for reports
3. **Modify charts**: Edit color schemes, ranges in source cells
4. **Add annotations**: Use `fig.add_annotation()` in Plotly cells
5. **Combine into dashboard**: Use Streamlit or Power BI with these charts

---

## 📈 NEXT STEPS

After EDA analysis, proceed to:
1. **Performance Analytics** (D4) - Risk-return metrics
2. **Dashboard** (D5) - Interactive web interface
3. **Advanced Analytics** (D6) - Predictive modeling
4. **Reports** (D7) - PDF/PowerPoint generation

---

## ✅ READY TO EXECUTE

Your notebook is now ready! Open in Jupyter and run all cells to:
- ✅ Generate 12 comprehensive visualizations
- ✅ Document 10 key business insights
- ✅ Export publication-ready PNG charts
- ✅ Create interactive HTML dashboards
- ✅ Complete EDA phase of capstone project

**Happy analyzing! 📊📈**

