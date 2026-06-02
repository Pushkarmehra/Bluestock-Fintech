"""
Live NAV Fetcher Module
Fetches live Net Asset Value (NAV) data for mutual funds from mfapi.in
"""

import requests
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MFAPIFetcher:
    """Fetch mutual fund data from MFAPI.in"""
    
    BASE_URL = "https://api.mfapi.in"
    
    # Key schemes to fetch
    KEY_SCHEMES = {
        'HDFC Top 100 Direct': 125497,
        'SBI Bluechip': 119551,
        'ICICI Bluechip': 120503,
        'Nippon Large Cap': 118632,
        'Axis Bluechip': 119092,
        'Kotak Bluechip': 120841
    }
    
    def __init__(self, output_path='data/raw'):
        """Initialize fetcher with output path"""
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        logger.info(f"MFAPIFetcher initialized - Output path: {self.output_path}")
    
    def fetch_scheme_nav(self, scheme_code, scheme_name=''):
        """
        Fetch NAV data for a single scheme
        
        Args:
            scheme_code (int): AMFI scheme code
            scheme_name (str): Name of the scheme
            
        Returns:
            dict: Parsed JSON response or None if failed
        """
        try:
            url = f"{self.BASE_URL}/mf/{scheme_code}"
            logger.info(f"Fetching NAV for {scheme_name or scheme_code}: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✓ Successfully fetched {scheme_name or scheme_code}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to fetch {scheme_name or scheme_code}: {str(e)}")
            return None
    
    def parse_nav_data(self, data, scheme_code, scheme_name=''):
        """
        Parse NAV response into DataFrame
        
        Args:
            data (dict): Raw JSON response from MFAPI
            scheme_code (int): AMFI scheme code
            scheme_name (str): Name of the scheme
            
        Returns:
            DataFrame: Parsed NAV data
        """
        try:
            meta = data.get('meta', {})
            nav_list = data.get('data', [])
            
            if not nav_list:
                logger.warning(f"No NAV data found for {scheme_name or scheme_code}")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(nav_list)
            
            # Add metadata
            df['scheme_code'] = scheme_code
            df['scheme_name'] = scheme_name or meta.get('scheme_name', '')
            df['fund_house'] = meta.get('fund_house', '')
            
            # Convert date column
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], format='%d-%b-%Y', errors='coerce')
            
            # Convert nav to numeric
            if 'nav' in df.columns:
                df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
            
            logger.info(f"Parsed {len(df)} NAV records for {scheme_name or scheme_code}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to parse NAV data for {scheme_name or scheme_code}: {str(e)}")
            return None
    
    def fetch_and_save_single_scheme(self, scheme_code, scheme_name=''):
        """
        Fetch and save NAV data for a single scheme
        
        Args:
            scheme_code (int): AMFI scheme code
            scheme_name (str): Name of the scheme
            
        Returns:
            bool: True if successful
        """
        data = self.fetch_scheme_nav(scheme_code, scheme_name)
        if not data:
            return False
        
        df = self.parse_nav_data(data, scheme_code, scheme_name)
        if df is None or df.empty:
            return False
        
        # Save to CSV
        filename = f"nav_{scheme_code}_{scheme_name.replace(' ', '_')}.csv"
        filepath = self.output_path / filename
        
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Saved NAV data to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save NAV data: {str(e)}")
            return False
    
    def fetch_all_key_schemes(self):
        """
        Fetch NAV data for all key schemes
        
        Returns:
            dict: DataFrames for each scheme
        """
        results = {}
        
        print(f"\n{'='*80}")
        print("FETCHING LIVE NAV DATA FOR KEY SCHEMES")
        print(f"{'='*80}\n")
        
        for scheme_name, scheme_code in self.KEY_SCHEMES.items():
            print(f"Fetching: {scheme_name} ({scheme_code})")
            data = self.fetch_scheme_nav(scheme_code, scheme_name)
            
            if data:
                df = self.parse_nav_data(data, scheme_code, scheme_name)
                if df is not None:
                    results[scheme_name] = df
                    # Save individual file
                    self.fetch_and_save_single_scheme(scheme_code, scheme_name)
            
            # Rate limiting
            time.sleep(0.5)
        
        return results
    
    def fetch_combined_nav_file(self):
        """
        Fetch and combine all key schemes into a single CSV
        
        Returns:
            DataFrame: Combined NAV data for all schemes
        """
        all_data = self.fetch_all_key_schemes()
        
        if not all_data:
            logger.error("No scheme data fetched")
            return None
        
        # Combine all DataFrames
        combined_df = pd.concat(all_data.values(), ignore_index=True)
        
        # Save combined file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"live_nav_combined_{timestamp}.csv"
        filepath = self.output_path / filename
        
        try:
            combined_df.to_csv(filepath, index=False)
            logger.info(f"Saved combined NAV data to {filepath}")
            print(f"\n✓ Combined {len(all_data)} schemes into {filename}")
            return combined_df
        except Exception as e:
            logger.error(f"Failed to save combined NAV data: {str(e)}")
            return None
    
    def get_latest_nav_for_scheme(self, scheme_code):
        """
        Get the latest NAV for a specific scheme
        
        Args:
            scheme_code (int): AMFI scheme code
            
        Returns:
            dict: Latest NAV info or None if failed
        """
        data = self.fetch_scheme_nav(scheme_code)
        if not data or not data.get('data'):
            return None
        
        latest = data['data'][0]  # Most recent is first
        meta = data.get('meta', {})
        
        return {
            'scheme_code': scheme_code,
            'scheme_name': meta.get('scheme_name', ''),
            'fund_house': meta.get('fund_house', ''),
            'date': latest.get('date', ''),
            'nav': latest.get('nav', ''),
            'fetched_at': datetime.now().isoformat()
        }
    
    def generate_nav_report(self):
        """Generate a report of latest NAVs for key schemes"""
        print(f"\n{'='*80}")
        print("LATEST NAV REPORT FOR KEY SCHEMES")
        print(f"{'='*80}\n")
        
        report_data = []
        
        for scheme_name, scheme_code in self.KEY_SCHEMES.items():
            nav_info = self.get_latest_nav_for_scheme(scheme_code)
            if nav_info:
                report_data.append(nav_info)
                print(f"{nav_info['scheme_name']:40} | {nav_info['nav']:>8} | {nav_info['date']}")
        
        if report_data:
            report_df = pd.DataFrame(report_data)
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"nav_report_{timestamp}.csv"
            filepath = self.output_path / filename
            
            try:
                report_df.to_csv(filepath, index=False)
                logger.info(f"Saved NAV report to {filepath}")
            except Exception as e:
                logger.error(f"Failed to save NAV report: {str(e)}")
            
            return report_df
        
        return None
    
    def run_complete_fetch(self):
        """Run complete NAV fetch and save process"""
        logger.info("Starting complete NAV fetch process...")
        
        # Fetch combined data
        combined_df = self.fetch_combined_nav_file()
        
        if combined_df is not None:
            print(f"\n{'='*80}")
            print("NAV DATA SUMMARY")
            print(f"{'='*80}")
            print(f"\nTotal Records: {len(combined_df)}")
            print(f"Schemes: {combined_df['scheme_name'].nunique()}")
            print(f"Date Range: {combined_df['date'].min()} to {combined_df['date'].max()}")
            print(f"\nSample Data:\n{combined_df.head(10)}")
        
        # Generate report
        self.generate_nav_report()
        
        logger.info("NAV fetch process complete!")


def main():
    """Main entry point"""
    fetcher = MFAPIFetcher()
    fetcher.run_complete_fetch()


if __name__ == "__main__":
    main()
