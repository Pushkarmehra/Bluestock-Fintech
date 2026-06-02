"""
Main orchestration module for Mutual Fund Analytics
Coordinates data ingestion and analysis workflows
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from data_ingestion import MutualFundDataIngestion
from live_nav_fetch import MFAPIFetcher


def main():
    """Main orchestration function"""
    
    print("\n" + "="*80)
    print("MUTUAL FUND ANALYTICS - DAY 1 INGESTION & ANALYSIS")
    print("="*80 + "\n")
    
    # Step 1: Data Ingestion
    print("STEP 1: DATA INGESTION FROM CSV FILES")
    print("-" * 80)
    ingestion = MutualFundDataIngestion()
    ingestion.run_complete_ingestion()
    
    # Step 2: Live NAV Fetch
    print("\nSTEP 2: LIVE NAV FETCH FROM MFAPI.IN")
    print("-" * 80)
    fetcher = MFAPIFetcher()
    fetcher.run_complete_fetch()
    
    print("\n" + "="*80)
    print("✓ DAY 1 WORKFLOW COMPLETE")
    print("="*80)
    print("\nDeliverables created:")
    print("  - data_ingestion.py: Full data ingestion and exploration module")
    print("  - live_nav_fetch.py: Live NAV fetcher from MFAPI.in")
    print("  - requirements.txt: Updated with all dependencies")
    print("  - CSV files: Saved in data/raw/ folder")
    print("\nNext steps:")
    print("  1. Add your 10 CSV datasets to data/raw/ folder")
    print("  2. Run: python main.py")
    print("  3. Explore generated reports in data/raw/")


if __name__ == "__main__":
    main()
