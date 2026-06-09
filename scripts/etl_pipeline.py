
import pandas as pd
import numpy as np
import os
from pathlib import Path
import sqlite3
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define paths using pathlib for cross-platform compatibility
BASE_DIR = Path(__file__).parent.parent
DATA_RAW = BASE_DIR / 'data' / 'raw'
DATA_PROCESSED = BASE_DIR / 'data' / 'processed'
DB_PATH = BASE_DIR / 'data' / 'db' / 'bluestock_mf.db'

# Ensure directories exist
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


class ETLPipeline:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.engine = None
        self.processed_data = {}
        
    def create_connection(self):
        """Create SQLite database connection using SQLAlchemy"""
        try:
            self.engine = create_engine(f'sqlite:///{self.db_path}')
            logger.info(f"Connected to database: {self.db_path}")
            return self.engine
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")
            raise

    def load_raw_data(self):
        """Load all raw CSV files"""
        logger.info("Loading raw data files...")
        
        raw_files = {
            'fund_master': DATA_RAW / '01_fund_master.csv',
            'nav_history': DATA_RAW / '02_nav_history.csv',
            'aum_by_fund_house': DATA_RAW / '03_aum_by_fund_house.csv',
            'monthly_sip_inflows': DATA_RAW / '04_monthly_sip_inflows.csv',
            'category_inflows': DATA_RAW / '05_category_inflows.csv',
            'industry_folio_count': DATA_RAW / '06_industry_folio_count.csv',
            'scheme_performance': DATA_RAW / '07_scheme_performance.csv',
            'investor_transactions': DATA_RAW / '08_investor_transactions.csv',
            'portfolio_holdings': DATA_RAW / '09_portfolio_holdings.csv',
            'benchmark_indices': DATA_RAW / '10_benchmark_indices.csv'
        }
        
        raw_data = {}
        for key, filepath in raw_files.items():
            if filepath.exists():
                try:
                    raw_data[key] = pd.read_csv(filepath)
                    logger.info(f"Loaded {key}: {len(raw_data[key])} rows")
                except Exception as e:
                    logger.warning(f"Failed to load {key}: {e}")
            else:
                logger.warning(f"File not found: {filepath}")
        
        return raw_data

    def clean_nav_history(self, nav_df):
        """Clean NAV history data"""
        logger.info("Cleaning NAV history...")
        
        # Convert date column to datetime
        nav_df['date'] = pd.to_datetime(nav_df['date'])
        
        # Handle missing NAV values - forward fill within each scheme
        nav_df['nav'] = pd.to_numeric(nav_df['nav'], errors='coerce')
        nav_df = nav_df.sort_values(['amfi_code', 'date'])
        nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].fillna(method='ffill')
        
        # Fill remaining NaN values with scheme average
        nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].fillna(nav_df.groupby('amfi_code')['nav'].transform('mean'))
        
        # Remove any duplicates
        nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
        
        logger.info(f"NAV history cleaned: {len(nav_df)} rows")
        return nav_df

    def clean_scheme_performance(self, perf_df):
        """Clean scheme performance data"""
        logger.info("Cleaning scheme performance...")
        
        # Convert numeric columns
        numeric_cols = ['return_1yr', 'return_3yr', 'return_5yr', 'expense_ratio', 'aum']
        for col in numeric_cols:
            if col in perf_df.columns:
                perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')
        
        # Remove rows with missing critical data
        perf_df = perf_df.dropna(subset=['amfi_code', 'scheme_name'])
        
        logger.info(f"Scheme performance cleaned: {len(perf_df)} rows")
        return perf_df

    def clean_investor_transactions(self, trans_df):
        """Clean investor transaction data"""
        logger.info("Cleaning investor transactions...")
        
        trans_df['date'] = pd.to_datetime(trans_df['date'], errors='coerce')
        trans_df['sip_amount'] = pd.to_numeric(trans_df['sip_amount'], errors='coerce')
        
        # Remove invalid transactions
        trans_df = trans_df.dropna(subset=['investor_id', 'sip_amount'])
        trans_df = trans_df[trans_df['sip_amount'] > 0]
        
        logger.info(f"Investor transactions cleaned: {len(trans_df)} rows")
        return trans_df

    def clean_portfolio_holdings(self, holdings_df):
        """Clean portfolio holdings data"""
        logger.info("Cleaning portfolio holdings...")
        
        holdings_df['weight'] = pd.to_numeric(holdings_df['weight'], errors='coerce')
        holdings_df = holdings_df.dropna(subset=['amfi_code', 'security_name'])
        
        logger.info(f"Portfolio holdings cleaned: {len(holdings_df)} rows")
        return holdings_df

    def transform_and_save(self, raw_data):
        """Transform raw data and save to processed folder"""
        logger.info("Transforming and saving processed data...")
        
        # Process NAV data
        if 'nav_history' in raw_data:
            nav_clean = self.clean_nav_history(raw_data['nav_history'].copy())
            nav_clean.to_csv(DATA_PROCESSED / 'nav_history_clean.csv', index=False)
            self.processed_data['nav_history'] = nav_clean
        
        # Process scheme performance
        if 'scheme_performance' in raw_data:
            perf_clean = self.clean_scheme_performance(raw_data['scheme_performance'].copy())
            perf_clean.to_csv(DATA_PROCESSED / 'scheme_performance_clean.csv', index=False)
            self.processed_data['scheme_performance'] = perf_clean
        
        # Process investor transactions
        if 'investor_transactions' in raw_data:
            trans_clean = self.clean_investor_transactions(raw_data['investor_transactions'].copy())
            trans_clean.to_csv(DATA_PROCESSED / 'investor_transactions_clean.csv', index=False)
            self.processed_data['investor_transactions'] = trans_clean
        
        # Process portfolio holdings
        if 'portfolio_holdings' in raw_data:
            hold_clean = self.clean_portfolio_holdings(raw_data['portfolio_holdings'].copy())
            hold_clean.to_csv(DATA_PROCESSED / 'portfolio_holdings_clean.csv', index=False)
            self.processed_data['portfolio_holdings'] = hold_clean
        
        # Copy other datasets as-is
        for key in ['fund_master', 'aum_by_fund_house', 'monthly_sip_inflows', 
                    'category_inflows', 'industry_folio_count', 'benchmark_indices']:
            if key in raw_data:
                raw_data[key].to_csv(DATA_PROCESSED / f'{key}_clean.csv', index=False)
                self.processed_data[key] = raw_data[key]
        
        logger.info(f"Processed {len(self.processed_data)} datasets")
        return self.processed_data

    def create_database_schema(self):
        """Create SQLite database schema"""
        logger.info("Creating database schema...")
        
        with self.engine.connect() as conn:
            # Create dimension and fact tables
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS dim_fund (
                    fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amfi_code TEXT UNIQUE NOT NULL,
                    scheme_name TEXT NOT NULL,
                    fund_house TEXT,
                    category TEXT,
                    subcategory TEXT,
                    launch_date TEXT,
                    expense_ratio REAL
                )
            '''))
            
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS dim_date (
                    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE UNIQUE NOT NULL,
                    year INTEGER,
                    month INTEGER,
                    day INTEGER,
                    day_of_week TEXT,
                    is_trading_day INTEGER DEFAULT 1
                )
            '''))
            
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS fact_nav (
                    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fund_id INTEGER NOT NULL,
                    date_id INTEGER NOT NULL,
                    nav REAL NOT NULL,
                    daily_return REAL,
                    FOREIGN KEY(fund_id) REFERENCES dim_fund(fund_id),
                    FOREIGN KEY(date_id) REFERENCES dim_date(date_id),
                    UNIQUE(fund_id, date_id)
                )
            '''))
            
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS fact_transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fund_id INTEGER NOT NULL,
                    date_id INTEGER NOT NULL,
                    investor_id TEXT,
                    sip_amount REAL,
                    units INTEGER,
                    transaction_type TEXT,
                    FOREIGN KEY(fund_id) REFERENCES dim_fund(fund_id),
                    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
                )
            '''))
            
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS fact_aum (
                    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fund_id INTEGER NOT NULL,
                    date_id INTEGER NOT NULL,
                    aum_value REAL,
                    aum_lakh_cr REAL,
                    FOREIGN KEY(fund_id) REFERENCES dim_fund(fund_id),
                    FOREIGN KEY(date_id) REFERENCES dim_date(date_id),
                    UNIQUE(fund_id, date_id)
                )
            '''))
            
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS fact_performance (
                    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fund_id INTEGER NOT NULL,
                    return_1yr REAL,
                    return_3yr REAL,
                    return_5yr REAL,
                    cagr REAL,
                    sharpe_ratio REAL,
                    sortino_ratio REAL,
                    max_drawdown REAL,
                    beta REAL,
                    alpha REAL,
                    tracking_error REAL,
                    fund_score REAL,
                    last_updated TEXT,
                    FOREIGN KEY(fund_id) REFERENCES dim_fund(fund_id),
                    UNIQUE(fund_id)
                )
            '''))
            
            conn.commit()
            logger.info("Database schema created successfully")

    def load_to_database(self):
        """Load processed data into SQLite database"""
        logger.info("Loading data into database...")
        
        try:
            # Load dimension data
            if 'fund_master' in self.processed_data:
                fund_df = self.processed_data['fund_master']
                # Rename columns to match schema if needed
                if 'amfi_code' in fund_df.columns:
                    fund_df[['amfi_code', 'scheme_name', 'fund_house', 'category']].to_sql(
                        'dim_fund', self.engine, if_exists='append', index=False
                    )
                    logger.info(f"Loaded {len(fund_df)} funds to dim_fund")
            
            # Load NAV fact table
            if 'nav_history' in self.processed_data:
                nav_df = self.processed_data['nav_history'].copy()
                nav_df['date'] = pd.to_datetime(nav_df['date'])
                
                # Create date dimension entries
                dates = nav_df[['date']].drop_duplicates().sort_values('date')
                dates['year'] = dates['date'].dt.year
                dates['month'] = dates['date'].dt.month
                dates['day'] = dates['date'].dt.day
                dates['day_of_week'] = dates['date'].dt.day_name()
                dates['is_trading_day'] = 1
                
                dates.to_sql('dim_date', self.engine, if_exists='append', index=False)
                logger.info(f"Loaded {len(dates)} dates to dim_date")
                
                # Load NAV facts
                nav_df.to_sql('fact_nav', self.engine, if_exists='append', index=False)
                logger.info(f"Loaded {len(nav_df)} NAV records")
            
            # Load transaction data
            if 'investor_transactions' in self.processed_data:
                trans_df = self.processed_data['investor_transactions'].copy()
                trans_df['date'] = pd.to_datetime(trans_df['date'])
                trans_df.to_sql('fact_transactions', self.engine, if_exists='append', index=False)
                logger.info(f"Loaded {len(trans_df)} transactions")
            
            logger.info("Data loading completed successfully")
            
        except Exception as e:
            logger.error(f"Error loading data to database: {e}")
            raise

    def run_pipeline(self):
        """Execute the complete ETL pipeline"""
        logger.info("=" * 50)
        logger.info("Starting ETL Pipeline")
        logger.info("=" * 50)
        
        try:
            # Create database connection
            self.create_connection()
            
            # Load raw data
            raw_data = self.load_raw_data()
            
            # Transform and save to processed folder
            self.transform_and_save(raw_data)
            
            # Create database schema
            self.create_database_schema()
            
            # Load to database
            self.load_to_database()
            
            logger.info("=" * 50)
            logger.info("ETL Pipeline completed successfully!")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise


if __name__ == '__main__':
    pipeline = ETLPipeline()
    pipeline.run_pipeline()
