CREATE TABLE dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    expense_ratio REAL
);
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER,
    is_weekday INTEGER
);

-- fact tables
CREATE TABLE fact_nav (
    amfi_code TEXT,
    date_id INTEGER,
    nav REAL,
    daily_return_pct REAL,

    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_transactions (
    tx_id INTEGER PRIMARY KEY,
    investor_id TEXT,
    amfi_code TEXT,
    date_id INTEGER,
    amount REAL,
    type TEXT,

    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
CREATE TABLE fact_performance (
    amfi_code TEXT,
    as_of_date DATE,
    return_1yr REAL,
    sharpe REAL,
    alpha REAL,
    max_dd REAL,

    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_portfolio (
    amfi_code TEXT,
    stock_symbol TEXT,
    weight_pct REAL,
    sector TEXT,
    date DATE,

    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
CREATE TABLE fact_aum (
    fund_house TEXT,
    date DATE,
    aum_crore REAL,
    num_schemes INTEGER
);
CREATE TABLE fact_sip_industry (
    month DATE,
    sip_inflow_crore REAL,
    sip_accounts_crore REAL
);