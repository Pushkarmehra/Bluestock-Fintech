#!/usr/bin/env python3
"""
Mutual Fund Analytics Pipeline Runner
Orchestrates entire workflow: ETL -> EDA -> Analytics
"""

import sys
import subprocess
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Project root
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Ensure output directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def run_command(cmd, description):
    """Execute a shell command and report status"""
    logger.info(f"Starting: {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✓ Completed: {description}")
            return True
        else:
            logger.error(f"✗ Failed: {description}")
            logger.error(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"✗ Exception in {description}: {e}")
        return False

def main():
    """Main orchestration function"""
    
    logger.info("="*70)
    logger.info("MUTUAL FUND ANALYTICS - COMPLETE PIPELINE")
    logger.info("="*70)
    
    pipeline_steps = [
        (
            f"python {PROJECT_ROOT / 'scripts' / 'etl_pipeline.py'}",
            "ETL Pipeline (Extract, Transform, Load)"
        ),
        (
            f"jupyter nbconvert --to notebook --execute {PROJECT_ROOT / 'notebooks' / '03_eda_analysis.ipynb'}",
            "EDA Analysis Notebook"
        ),
        (
            f"jupyter nbconvert --to notebook --execute {PROJECT_ROOT / 'notebooks' / '04_performance_analytics.ipynb'}",
            "Performance Analytics Notebook"
        ),
        (
            f"python {PROJECT_ROOT / 'scripts' / 'monte_carlo_simulation.py'}",
            "Monte Carlo Simulation (Bonus)"
        ),
    ]
    
    completed = 0
    failed = 0
    
    for cmd, description in pipeline_steps:
        if run_command(cmd, description):
            completed += 1
        else:
            failed += 1
    
    # Summary
    logger.info("="*70)
    logger.info(f"PIPELINE SUMMARY")
    logger.info(f"  Completed: {completed}/{len(pipeline_steps)}")
    logger.info(f"  Failed: {failed}/{len(pipeline_steps)}")
    
    if failed == 0:
        logger.info("✓ All pipeline steps completed successfully!")
        logger.info("\nNext Steps:")
        logger.info("  1. Review generated CSVs in reports/ folder")
        logger.info("  2. Launch Streamlit dashboard: streamlit run dashboard/app.py")
        logger.info("  3. Check data_dictionary.md for field definitions")
        return 0
    else:
        logger.error(f"✗ Pipeline failed with {failed} error(s)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
