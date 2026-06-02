"""
Data Ingestion Module for Mutual Fund Analytics
Loads and explores 10 CSV datasets
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MutualFundDataIngestion:
    """Handle data ingestion and exploration for mutual fund datasets"""
    
    def __init__(self, data_raw_path='data/raw', data_processed_path='data/processed'):
        """Initialize data paths"""
        self.raw_path = Path(data_raw_path)
        self.processed_path = Path(data_processed_path)
        self.datasets = {}
        self.anomalies = {}
        
        # Ensure directories exist
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Data paths initialized - Raw: {self.raw_path}, Processed: {self.processed_path}")
    
    def load_datasets(self):
        """
        Load all CSV datasets from raw data folder
        Expected datasets (10 files):
        1. fund_master.csv
        2. nav_history.csv
        3. scheme_performance.csv
        4. expense_ratio.csv
        5. portfolio_allocation.csv
        6. fund_returns.csv
        7. fund_risk_metrics.csv
        8. market_index.csv
        9. sector_allocation.csv
        10. daily_nav.csv
        """
        csv_files = list(self.raw_path.glob('*.csv'))
        logger.info(f"Found {len(csv_files)} CSV files in {self.raw_path}")
        
        if len(csv_files) == 0:
            logger.warning("No CSV files found in raw data folder")
            return
        
        for file_path in sorted(csv_files):
            try:
                df = pd.read_csv(file_path)
                dataset_name = file_path.stem
                self.datasets[dataset_name] = df
                logger.info(f"✓ Loaded {dataset_name}: {df.shape[0]} rows × {df.shape[1]} columns")
            except Exception as e:
                logger.error(f"✗ Failed to load {file_path.name}: {str(e)}")
    
    def explore_dataset(self, name, df):
        """Explore a single dataset and report findings"""
        print(f"\n{'='*80}")
        print(f"DATASET: {name.upper()}")
        print(f"{'='*80}")
        
        # Shape
        print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Data types
        print(f"\nData Types:\n{df.dtypes}")
        
        # First few rows
        print(f"\nFirst 5 rows:\n{df.head()}")
        
        # Anomalies
        anomalies = []
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            anomaly_msg = f"Missing values: {missing[missing > 0].to_dict()}"
            anomalies.append(anomaly_msg)
            print(f"\n⚠ {anomaly_msg}")
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            anomaly_msg = f"Duplicate rows: {duplicates}"
            anomalies.append(anomaly_msg)
            print(f"\n⚠ {anomaly_msg}")
        
        # Check for data type inconsistencies
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    # Try to convert to numeric
                    pd.to_numeric(df[col], errors='coerce')
                    non_numeric = df[col].isnull().sum() - df[col].isnull().sum()
                    if non_numeric > 0:
                        anomaly_msg = f"Non-numeric values in {col}: {non_numeric}"
                        anomalies.append(anomaly_msg)
                        print(f"\n⚠ {anomaly_msg}")
                except:
                    pass
        
        # Summary statistics
        print(f"\nSummary Statistics:\n{df.describe(include='all')}")
        
        self.anomalies[name] = anomalies
        return anomalies
    
    def explore_all_datasets(self):
        """Explore all loaded datasets"""
        if not self.datasets:
            logger.warning("No datasets loaded. Call load_datasets() first.")
            return
        
        for name, df in self.datasets.items():
            self.explore_dataset(name, df)
    
    def explore_fund_master(self):
        """Deep dive into fund master dataset"""
        if 'fund_master' not in self.datasets:
            logger.warning("fund_master dataset not found")
            return
        
        fm = self.datasets['fund_master']
        print(f"\n{'='*80}")
        print("FUND MASTER - DEEP EXPLORATION")
        print(f"{'='*80}")
        
        # Unique fund houses
        if 'Fund House' in fm.columns or 'fund_house' in fm.columns:
            fund_house_col = 'Fund House' if 'Fund House' in fm.columns else 'fund_house'
            print(f"\nUnique Fund Houses ({fm[fund_house_col].nunique()}):")
            print(fm[fund_house_col].value_counts())
        
        # Categories
        if 'Category' in fm.columns or 'category' in fm.columns:
            cat_col = 'Category' if 'Category' in fm.columns else 'category'
            print(f"\nUnique Categories ({fm[cat_col].nunique()}):")
            print(fm[cat_col].value_counts())
        
        # Sub-categories
        if 'Sub-Category' in fm.columns or 'sub_category' in fm.columns:
            subcat_col = 'Sub-Category' if 'Sub-Category' in fm.columns else 'sub_category'
            print(f"\nUnique Sub-Categories ({fm[subcat_col].nunique()}):")
            print(fm[subcat_col].value_counts().head(15))
        
        # Risk Grade
        if 'Risk Grade' in fm.columns or 'risk_grade' in fm.columns:
            risk_col = 'Risk Grade' if 'Risk Grade' in fm.columns else 'risk_grade'
            print(f"\nRisk Grades:")
            print(fm[risk_col].value_counts())
        
        # AMFI Code structure
        if 'Scheme Code' in fm.columns or 'scheme_code' in fm.columns:
            code_col = 'Scheme Code' if 'Scheme Code' in fm.columns else 'scheme_code'
            print(f"\nAMFI Scheme Code Statistics:")
            print(f"  Total Schemes: {len(fm)}")
            print(f"  Unique Codes: {fm[code_col].nunique()}")
            print(f"  Code Data Type: {fm[code_col].dtype}")
            print(f"  Sample Codes: {fm[code_col].head().tolist()}")
    
    def validate_amfi_codes(self):
        """Validate AMFI codes across datasets"""
        if 'fund_master' not in self.datasets or 'nav_history' not in self.datasets:
            logger.warning("fund_master or nav_history dataset not found")
            return
        
        print(f"\n{'='*80}")
        print("AMFI CODE VALIDATION")
        print(f"{'='*80}")
        
        fm = self.datasets['fund_master']
        nh = self.datasets['nav_history']
        
        # Find scheme code columns
        fm_code_col = None
        nh_code_col = None
        
        for col in ['Scheme Code', 'scheme_code', 'SchemeCode']:
            if col in fm.columns:
                fm_code_col = col
                break
        
        for col in ['Scheme Code', 'scheme_code', 'SchemeCode']:
            if col in nh.columns:
                nh_code_col = col
                break
        
        if not fm_code_col or not nh_code_col:
            logger.warning("Could not find scheme code columns")
            return
        
        fm_codes = set(fm[fm_code_col].unique())
        nh_codes = set(nh[nh_code_col].unique())
        
        missing_in_nav = fm_codes - nh_codes
        extra_in_nav = nh_codes - fm_codes
        
        print(f"\nFund Master - Total schemes: {len(fm)}, Unique codes: {len(fm_codes)}")
        print(f"NAV History - Unique codes: {len(nh_codes)}")
        
        if missing_in_nav:
            print(f"\n⚠ Codes in fund_master but NOT in nav_history: {len(missing_in_nav)}")
            print(f"  Sample: {list(missing_in_nav)[:5]}")
        else:
            print(f"\n✓ All fund_master codes found in nav_history")
        
        if extra_in_nav:
            print(f"\n⚠ Codes in nav_history but NOT in fund_master: {len(extra_in_nav)}")
            print(f"  Sample: {list(extra_in_nav)[:5]}")
        else:
            print(f"\n✓ No extra codes in nav_history")
    
    def generate_quality_summary(self):
        """Generate a data quality summary"""
        print(f"\n{'='*80}")
        print("DATA QUALITY SUMMARY")
        print(f"{'='*80}")
        
        print(f"\nDatasets Loaded: {len(self.datasets)}")
        
        total_rows = sum(len(df) for df in self.datasets.values())
        print(f"Total Records: {total_rows}")
        
        print(f"\nAnomalies Found:")
        total_anomalies = sum(len(v) for v in self.anomalies.values())
        if total_anomalies == 0:
            print("  ✓ No anomalies detected")
        else:
            for name, anomalies in self.anomalies.items():
                if anomalies:
                    print(f"\n  {name}:")
                    for anomaly in anomalies:
                        print(f"    - {anomaly}")
        
        print(f"\n{'='*80}\n")
    
    def run_complete_ingestion(self):
        """Run complete data ingestion and exploration"""
        logger.info("Starting complete data ingestion process...")
        
        self.load_datasets()
        
        if self.datasets:
            self.explore_all_datasets()
            self.explore_fund_master()
            self.validate_amfi_codes()
            self.generate_quality_summary()
            
            logger.info("Data ingestion complete!")
            return True
        else:
            logger.error("No datasets loaded. Ensure CSV files are in data/raw folder.")
            return False


def main():
    """Main entry point"""
    ingestion = MutualFundDataIngestion()
    ingestion.run_complete_ingestion()


if __name__ == "__main__":
    main()
