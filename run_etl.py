#!/usr/bin/env python3
"""
Quick ETL Execution Script - Clean All Data & Save to data/processed/
Run this to execute Tasks 1-6 in sequence
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3
from sqlalchemy import create_engine, text
from datetime import datetime

# Setup paths
BASE_PATH = Path(__file__).parent
RAW_DATA = BASE_PATH / "data" / "raw"
PROCESSED_DATA = BASE_PATH / "data" / "processed"
SQL_PATH = BASE_PATH / "sql"
DB_PATH = SQL_PATH / "bluestock_mf.db"

# Create directories
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
SQL_PATH.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("🚀 MUTUAL FUND ANALYTICS - ETL PIPELINE")
print("=" * 70)
print(f"\n📁 Paths:")
print(f"  Raw data:    {RAW_DATA}")
print(f"  Processed:   {PROCESSED_DATA}")
print(f"  Database:    {DB_PATH}\n")

# ============================================================================
# TASK 1: Clean NAV History
# ============================================================================
print("📊 TASK 1: Cleaning NAV History...")
try:
    nav_df = pd.read_csv(RAW_DATA / "02_nav_history.csv")
    print(f"  ✓ Loaded {len(nav_df):,} records")
    
    # Convert date to datetime
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    
    # Sort by amfi_code and date
    nav_df = nav_df.sort_values(['amfi_code', 'date']).reset_index(drop=True)
    
    # Remove duplicates
    nav_df = nav_df.drop_duplicates()
    
    # Forward-fill NAV
    nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].ffill()
    
    # Validate NAV > 0
    nav_df = nav_df[nav_df['nav'] > 0]
    
    # Save to processed folder
    nav_clean_path = PROCESSED_DATA / "nav_history_clean.csv"
    nav_df.to_csv(nav_clean_path, index=False)
    
    print(f"  ✓ Saved: {nav_clean_path}")
    print(f"    Records: {len(nav_df):,} | Schemes: {nav_df['amfi_code'].nunique()}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================================
# TASK 2: Clean Investor Transactions
# ============================================================================
print("\n👥 TASK 2: Cleaning Investor Transactions...")
try:
    inv_df = pd.read_csv(RAW_DATA / "08_investor_transactions.csv")
    print(f"  ✓ Loaded {len(inv_df):,} records")
    
    # Standardize transaction type
    inv_df['transaction_type'] = inv_df['transaction_type'].str.title()
    
    # Convert date
    inv_df['transaction_date'] = pd.to_datetime(inv_df['transaction_date'])
    
    # Validate amount > 0
    inv_df = inv_df[inv_df['amount_inr'] > 0]
    
    # Standardize KYC status
    inv_df['kyc_status'] = inv_df['kyc_status'].str.title()
    
    # Save to processed folder
    inv_clean_path = PROCESSED_DATA / "investor_transactions_clean.csv"
    inv_df.to_csv(inv_clean_path, index=False)
    
    print(f"  ✓ Saved: {inv_clean_path}")
    print(f"    Records: {len(inv_df):,} | Funds: {inv_df['amfi_code'].nunique()}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================================
# TASK 3: Clean Scheme Performance
# ============================================================================
print("\n⭐ TASK 3: Cleaning Scheme Performance...")
try:
    scheme_df = pd.read_csv(RAW_DATA / "07_scheme_performance.csv")
    print(f"  ✓ Loaded {len(scheme_df):,} records")
    
    # Convert return columns to numeric
    return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
    for col in return_cols:
        scheme_df[col] = pd.to_numeric(scheme_df[col], errors='coerce')
    
    # Detect anomalies using IQR
    for col in return_cols:
        Q1 = scheme_df[col].quantile(0.25)
        Q3 = scheme_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        scheme_df[f'{col}_anomaly'] = (scheme_df[col] < lower) | (scheme_df[col] > upper)
    
    # Validate expense ratio
    valid_expense = ((scheme_df['expense_ratio_pct'] >= 0.1) & 
                     (scheme_df['expense_ratio_pct'] <= 2.5)).sum()
    
    # Save to processed folder
    scheme_clean_path = PROCESSED_DATA / "scheme_performance_clean.csv"
    scheme_df.to_csv(scheme_clean_path, index=False)
    
    print(f"  ✓ Saved: {scheme_clean_path}")
    print(f"    Records: {len(scheme_df)} | Valid Expense Ratio: {valid_expense}/{len(scheme_df)}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================================
# TASK 4: Create SQLite Schema
# ============================================================================
print("\n🏗️  TASK 4: Creating SQLite Schema...")
try:
    engine = create_engine(f'sqlite:///{DB_PATH}')
    
    schema_sql = """
    CREATE TABLE IF NOT EXISTS dim_fund (
        fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code TEXT UNIQUE NOT NULL,
        scheme_name TEXT NOT NULL,
        fund_house TEXT,
        category TEXT,
        expense_ratio REAL
    );
    CREATE TABLE IF NOT EXISTS dim_date (
        date_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE UNIQUE NOT NULL,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        day_of_week TEXT
    );
    CREATE TABLE IF NOT EXISTS fact_nav (
        nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_id INTEGER NOT NULL,
        date_id INTEGER NOT NULL,
        nav REAL NOT NULL,
        FOREIGN KEY(fund_id) REFERENCES dim_fund(fund_id),
        FOREIGN KEY(date_id) REFERENCES dim_date(date_id),
        UNIQUE(fund_id, date_id)
    );
    CREATE TABLE IF NOT EXISTS fact_transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_id INTEGER NOT NULL,
        date_id INTEGER NOT NULL,
        transaction_type TEXT,
        amount_inr REAL,
        kyc_status TEXT,
        state TEXT,
        FOREIGN KEY(fund_id) REFERENCES dim_fund(fund_id),
        FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
    );
    CREATE TABLE IF NOT EXISTS fact_performance (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_id INTEGER NOT NULL,
        return_1yr REAL,
        return_3yr REAL,
        return_5yr REAL,
        FOREIGN KEY(fund_id) REFERENCES dim_fund(fund_id),
        UNIQUE(fund_id)
    );
    CREATE INDEX IF NOT EXISTS idx_fund_amfi ON dim_fund(amfi_code);
    CREATE INDEX IF NOT EXISTS idx_date_datevalue ON dim_date(date);
    CREATE INDEX IF NOT EXISTS idx_nav_fund_date ON fact_nav(fund_id, date_id);
    CREATE INDEX IF NOT EXISTS idx_trans_fund_date ON fact_transactions(fund_id, date_id);
    """
    
    with engine.connect() as conn:
        for statement in schema_sql.split(';'):
            if statement.strip():
                conn.execute(text(statement))
        conn.commit()
    
    print(f"  ✓ Schema created: {DB_PATH}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================================
# TASK 5: Load Data into Database
# ============================================================================
print("\n💾 TASK 5: Loading Data into SQLite...")
try:
    # Load fund dimension
    fund_df = scheme_df[['amfi_code', 'scheme_name', 'fund_house', 'category', 'expense_ratio_pct']].copy()
    fund_df.columns = ['amfi_code', 'scheme_name', 'fund_house', 'category', 'expense_ratio']
    fund_df = fund_df.drop_duplicates(subset=['amfi_code'])
    fund_df.to_sql('dim_fund', engine, if_exists='append', index=False)
    print(f"  ✓ Loaded dim_fund: {len(fund_df)} records")
    
    # Load date dimension
    date_df = pd.DataFrame({'date': pd.date_range('2022-01-01', '2025-12-31')})
    date_df['year'] = date_df['date'].dt.year
    date_df['month'] = date_df['date'].dt.month
    date_df['day'] = date_df['date'].dt.day
    date_df['day_of_week'] = date_df['date'].dt.day_name()
    date_df.to_sql('dim_date', engine, if_exists='append', index=False)
    print(f"  ✓ Loaded dim_date: {len(date_df)} records")
    
    # Load fact tables
    nav_df.to_sql('fact_nav', engine, if_exists='append', index=False)
    print(f"  ✓ Loaded fact_nav: {len(nav_df):,} records")
    
    inv_df.to_sql('fact_transactions', engine, if_exists='append', index=False)
    print(f"  ✓ Loaded fact_transactions: {len(inv_df):,} records")
    
    perf_df = scheme_df[['amfi_code', 'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']].copy()
    perf_df.columns = ['amfi_code', 'return_1yr', 'return_3yr', 'return_5yr']
    perf_df.to_sql('fact_performance', engine, if_exists='append', index=False)
    print(f"  ✓ Loaded fact_performance: {len(perf_df)} records")
    
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================================
# TASK 6: Save SQL Queries
# ============================================================================
print("\n📋 TASK 6: Saving Analytical Queries...")
try:
    queries_file = SQL_PATH / "queries.sql"
    with open(queries_file, 'w') as f:
        f.write("""
-- Top 5 Funds by Average NAV
SELECT df.amfi_code, df.scheme_name, ROUND(AVG(fn.nav), 2) as avg_nav
FROM fact_nav fn JOIN dim_fund df ON fn.fund_id = df.fund_id
GROUP BY fn.fund_id ORDER BY avg_nav DESC LIMIT 5;

-- Monthly NAV Trends
SELECT dd.year, dd.month, ROUND(AVG(fn.nav), 2) as avg_nav, COUNT(DISTINCT fn.fund_id) as schemes
FROM fact_nav fn JOIN dim_date dd ON fn.date_id = dd.date_id
GROUP BY dd.year, dd.month ORDER BY dd.year DESC, dd.month DESC;

-- Top 10 States by Transaction Volume
SELECT ft.state, COUNT(*) as count, ROUND(SUM(ft.amount_inr), 2) as total
FROM fact_transactions ft WHERE ft.state IS NOT NULL
GROUP BY ft.state ORDER BY total DESC LIMIT 10;

-- Transaction Type Distribution
SELECT ft.transaction_type, COUNT(*) as count, ROUND(SUM(ft.amount_inr), 2) as total
FROM fact_transactions ft GROUP BY ft.transaction_type ORDER BY total DESC;

-- KYC Status Distribution
SELECT ft.kyc_status, COUNT(*) as count, ROUND(SUM(ft.amount_inr), 2) as total
FROM fact_transactions ft WHERE ft.kyc_status IS NOT NULL
GROUP BY ft.kyc_status ORDER BY total DESC;

-- Funds by Category
SELECT df.category, COUNT(DISTINCT df.fund_id) as fund_count, ROUND(AVG(df.expense_ratio), 2) as avg_expense
FROM dim_fund df GROUP BY df.category ORDER BY fund_count DESC;

-- Fund Performance Scorecard
SELECT df.scheme_name, df.fund_house, df.category,
  ROUND(AVG(fp.return_1yr), 2) as avg_1yr, ROUND(AVG(fp.return_3yr), 2) as avg_3yr
FROM fact_performance fp JOIN dim_fund df ON fp.fund_id = df.fund_id
ORDER BY avg_3yr DESC LIMIT 15;

-- Transaction Trends by Month
SELECT dd.year, dd.month, COUNT(*) as count, ROUND(SUM(ft.amount_inr), 2) as monthly_inflow
FROM fact_transactions ft JOIN dim_date dd ON ft.date_id = dd.date_id
GROUP BY dd.year, dd.month ORDER BY dd.year DESC, dd.month DESC;

-- Expense Ratio Analysis
SELECT CASE WHEN expense_ratio < 0.5 THEN 'Low' WHEN expense_ratio < 1.0 THEN 'Medium' ELSE 'High' END as bracket,
  COUNT(*) as funds, ROUND(AVG(expense_ratio), 2) as avg_expense
FROM dim_fund GROUP BY bracket;

-- Fund House Analysis
SELECT df.fund_house, COUNT(DISTINCT df.fund_id) as funds, COUNT(DISTINCT ft.transaction_id) as transactions,
  ROUND(SUM(ft.amount_inr), 2) as total_inflow
FROM dim_fund df LEFT JOIN fact_transactions ft ON df.fund_id = ft.fund_id
GROUP BY df.fund_house ORDER BY total_inflow DESC;
""")
    print(f"  ✓ Saved: {queries_file}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("✅ ETL PIPELINE COMPLETE!")
print("=" * 70)
print(f"\n📁 Output Files Created:")
print(f"  ✓ {PROCESSED_DATA / 'nav_history_clean.csv'}")
print(f"  ✓ {PROCESSED_DATA / 'investor_transactions_clean.csv'}")
print(f"  ✓ {PROCESSED_DATA / 'scheme_performance_clean.csv'}")
print(f"  ✓ {DB_PATH}")
print(f"  ✓ {SQL_PATH / 'queries.sql'}")
print("\n💡 Next Steps:")
print("  1. Review cleaned files in data/processed/")
print("  2. Query database: sql/bluestock_mf.db")
print("  3. Run dashboard: python dashboard/app.py")
print("=" * 70 + "\n")
