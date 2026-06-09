# Data Dictionary

## dim_fund
| Column | Type | Description | Source |
|---|---|---|---|
| amfi_code | TEXT (PK) | AMFI unique fund identifier | 07_scheme_performance.csv |
| scheme_name | TEXT | Full name of the mutual fund scheme | 07_scheme_performance.csv |
| fund_house | TEXT | Asset Management Company name | 07_scheme_performance.csv |
| category | TEXT | SEBI fund category (e.g. Large Cap, ELSS) | 07_scheme_performance.csv |
| expense_ratio_pct | REAL | Annual expense ratio in % (range: 0.1–2.5) | 07_scheme_performance.csv |

## fact_nav
| Column | Type | Description | Source |
|---|---|---|---|
| amfi_code | TEXT (FK → dim_fund) | Fund identifier | 02_nav_history.csv |
| nav_date | DATE | Date of NAV record | 02_nav_history.csv |
| nav | REAL | Net Asset Value (INR); forward-filled for holidays; must be > 0 | 02_nav_history.csv |

## fact_transactions
| Column | Type | Description | Source |
|---|---|---|---|
| transaction_id | TEXT | Unique transaction identifier | 08_investor_transactions.csv |
| amfi_code | TEXT (FK → dim_fund) | Fund identifier | 08_investor_transactions.csv |
| investor_id | TEXT | Investor identifier | 08_investor_transactions.csv |
| transaction_date | DATE | Date of transaction | 08_investor_transactions.csv |
| transaction_type | TEXT | Standardised type: SIP / Lumpsum / Redemption | 08_investor_transactions.csv |
| amount_inr | REAL | Transaction amount in INR; must be > 0 | 08_investor_transactions.csv |
| kyc_status | TEXT | KYC compliance status (Verified / Pending / Rejected) | 08_investor_transactions.csv |

## fact_performance
| Column | Type | Description | Source |
|---|---|---|---|
| amfi_code | TEXT (FK → dim_fund) | Fund identifier | 07_scheme_performance.csv |
| return_1yr_pct | REAL | 1-year trailing return % | 07_scheme_performance.csv |
| return_3yr_pct | REAL | 3-year trailing return % | 07_scheme_performance.csv |
| return_5yr_pct | REAL | 5-year trailing return % | 07_scheme_performance.csv |
| alpha | REAL | Risk-adjusted excess return vs benchmark | 07_scheme_performance.csv |
| sharpe_ratio | REAL | Return per unit of risk (negative = underperformer) | 07_scheme_performance.csv |
| max_drawdown_pct | REAL | Peak-to-trough decline % (less negative = safer) | 07_scheme_performance.csv |

## fact_aum
| Column | Type | Description | Source |
|---|---|---|---|
| date | DATE | Month-end date | 03_aum_by_fund_house.csv |
| fund_house | TEXT | AMC name | 03_aum_by_fund_house.csv |
| aum_cr | REAL | Assets Under Management in crores (INR) | 03_aum_by_fund_house.csv |

## fact_sip_inflows
| Column | Type | Description | Source |
|---|---|---|---|
| month | TEXT | Month in YYYY-MM format | 04_monthly_sip_inflows.csv |
| sip_inflow_cr | REAL | Total SIP inflows in crores (INR) | 04_monthly_sip_inflows.csv |
| yoy_growth_pct | REAL | Year-on-year growth %; back-filled for missing months | 04_monthly_sip_inflows.csv |

## dim_date
| Column | Type | Description | Source |
|---|---|---|---|
| date | DATE | Calendar date | Derived from fact_nav |
| date_id | INTEGER | Surrogate key in YYYYMMDD format | Derived |
| year | INTEGER | Calendar year | Derived |
| month | INTEGER | Calendar month (1–12) | Derived |
| quarter | INTEGER | Calendar quarter (1–4) | Derived |
| is_weekday | INTEGER | 1 if Mon–Fri, 0 if weekend | Derived |