#!/usr/bin/env python3
"""
Attempt to access QuantConnect data for S&P 500 (SPY)
"""

import subprocess
import sys

def install_quantconnect():
    """Try to install QuantConnect package"""
    print("=" * 80)
    print("Installing QuantConnect Package")
    print("=" * 80)
    
    try:
        print("\nAttempting to install quantconnect...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'quantconnect', '--quiet'])
        print("✓ Successfully installed quantconnect")
        return True
    except Exception as e:
        print(f"✗ Could not install: {e}")
        return False

def explain_quantconnect_access():
    """Explain how to access QuantConnect data"""
    print("\n" + "=" * 80)
    print("QuantConnect Data Access Methods")
    print("=" * 80)
    
    print("\n📚 QuantConnect provides data through several methods:")
    
    print("\n1️⃣  METHOD 1: Through QuantConnect Cloud Platform (EASIEST)")
    print("─" * 80)
    print("   • Sign up: https://www.quantconnect.com/")
    print("   • Free account with data access")
    print("   • Run backtests in their cloud")
    print("   • Download results as CSV")
    print("   • No local installation needed")
    
    print("\n2️⃣  METHOD 2: Local LEAN Engine")
    print("─" * 80)
    print("   • Download LEAN: https://github.com/QuantConnect/Lean")
    print("   • Run backtests locally")
    print("   • Data downloaded automatically")
    print("   • More control, more setup")
    
    print("\n3️⃣  METHOD 3: QuantConnect API")
    print("─" * 80)
    print("   • Requires API key from account")
    print("   • Access data programmatically")
    print("   • Good for automated workflows")
    
    print("\n📊 Data Available:")
    print("   • SPY (S&P 500 ETF): 1998 - Present")
    print("   • Resolution: Tick, Second, Minute, Hour, Daily")
    print("   • Format: Trade and Quote data")
    
    print("\n💡 RECOMMENDATION:")
    print("   Start with Method 1 (Cloud Platform):")
    print("   1. Create free account at quantconnect.com")
    print("   2. Create new algorithm project")
    print("   3. Use this simple code to download data:")
    
    sample_code = '''
# QuantConnect Algorithm to export SPY minute data
class DataExporter(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(1998, 1, 1)  # Start from 1998
        self.SetEndDate(2026, 10, 22)   # Until today
        self.AddEquity("SPY", Resolution.Minute)
        
    def OnData(self, data):
        if data.ContainsKey("SPY"):
            bar = data["SPY"]
            # Data is automatically logged and can be downloaded
            self.Log(f"{self.Time},{bar.Open},{bar.High},{bar.Low},{bar.Close},{bar.Volume}")
'''
    
    print("\n" + "─" * 80)
    print(sample_code)
    print("─" * 80)
    
    print("\n   4. Run backtest")
    print("   5. Download results from Backtest page")

def provide_alternative_download_methods():
    """Provide information on alternative download methods"""
    print("\n" + "=" * 80)
    print("Alternative Methods to Get Historical Intraday Data")
    print("=" * 80)
    
    print("\n🔧 METHOD A: Polygon.io Free Tier")
    print("─" * 80)
    print("   URL: https://polygon.io/")
    print("   • Free tier: 5 API calls/minute")
    print("   • Historical data from 2004")
    print("   • Can slowly download data over time")
    print("   • Good for recent years (2020-2026)")
    
    print("\n🔧 METHOD B: Alpha Vantage")
    print("─" * 80)
    print("   URL: https://www.alphavantage.co/")
    print("   • Free API key")
    print("   • Intraday available but limited")
    print("   • 5 requests/minute, 500/day")
    print("   • Best for recent 1-2 years")
    
    print("\n🔧 METHOD C: Yahoo Finance (Extended)")
    print("─" * 80)
    print("   • We already used this for last 2 years")
    print("   • Limited to 730 days")
    print("   • Good for recent analysis only")
    
    print("\n💰 PAID BUT AFFORDABLE:")
    print("   • Polygon.io Starter: $99/month (from 2004)")
    print("   • Kibot: $30-300/month (from 1998)")
    print("   • First Rate Data: One-time $50-200 (from 2000)")

def create_manual_polygon_script():
    """Create a script to slowly download data from Polygon.io free tier"""
    print("\n" + "=" * 80)
    print("Creating Sample Script for Polygon.io")
    print("=" * 80)
    
    script = '''#!/usr/bin/env python3
"""
Sample script to download S&P 500 data from Polygon.io (Free Tier)
Requires: pip install requests
Sign up for free API key: https://polygon.io/
"""

import requests
import time
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY_HERE"  # Get from polygon.io

def download_spy_data(date):
    """Download SPY data for a specific date"""
    url = f"https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/{date}/{date}"
    params = {"apiKey": API_KEY, "adjusted": "true", "sort": "asc", "limit": 50000}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK" and data["resultsCount"] > 0:
            return data["results"]
    
    return None

def download_historical_range(start_date, end_date):
    """Download data for a date range (respecting free tier limits)"""
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    all_data = []
    call_count = 0
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        print(f"Downloading {date_str}...")
        
        data = download_spy_data(date_str)
        if data:
            all_data.extend(data)
            print(f"  ✓ Got {len(data)} bars")
        
        call_count += 1
        
        # Free tier: 5 calls/minute
        if call_count % 5 == 0:
            print("  Waiting 60s (rate limit)...")
            time.sleep(60)
        
        current += timedelta(days=1)
    
    return all_data

# Example usage:
# data = download_historical_range("2024-01-01", "2024-01-31")
# df = pd.DataFrame(data)
# df.to_csv("spy_jan_2024.csv", index=False)
'''
    
    with open('/workspace/polygon_downloader_sample.py', 'w') as f:
        f.write(script)
    
    print("\n✓ Created sample script: polygon_downloader_sample.py")
    print("  • Sign up at polygon.io for free API key")
    print("  • Replace YOUR_API_KEY_HERE with your key")
    print("  • Run to slowly download historical data")
    print("  • Respects free tier rate limits (5 calls/min)")

def main():
    print("=" * 80)
    print("Accessing Historical Intraday Data")
    print("=" * 80)
    print()
    
    # Try to install QuantConnect
    qc_installed = install_quantconnect()
    
    # Explain access methods
    explain_quantconnect_access()
    
    # Provide alternatives
    provide_alternative_download_methods()
    
    # Create sample script
    create_manual_polygon_script()
    
    print("\n" + "=" * 80)
    print("📋 SUMMARY & NEXT STEPS")
    print("=" * 80)
    
    print("\n🏆 BEST FREE OPTION: QuantConnect")
    print("   Step 1: Sign up at https://www.quantconnect.com/")
    print("   Step 2: Create algorithm project")
    print("   Step 3: Use sample code above to export data")
    print("   Step 4: Download results")
    print("   Coverage: 1998-2026 (28 years!)")
    
    print("\n🥈 SECOND OPTION: Polygon.io Free Tier")
    print("   Step 1: Sign up at https://polygon.io/")
    print("   Step 2: Get free API key")
    print("   Step 3: Use polygon_downloader_sample.py")
    print("   Step 4: Slowly download (5 calls/min limit)")
    print("   Coverage: 2004-2026")
    
    print("\n💰 PAID OPTION: Polygon.io Starter ($99/mo)")
    print("   • No rate limits")
    print("   • Download everything quickly")
    print("   • From 2004")
    
    print("\n📊 WHAT YOU ALREADY HAVE:")
    print("   ✓ Daily data 1990-2026 (complete)")
    print("   ✓ Hourly data 2024-2026 (last 2 years)")
    print("   ✓ All major analyses complete")
    
    print("\n💡 RECOMMENDATION:")
    print("   Your current analysis is already excellent!")
    print("   If you want more intraday:")
    print("   → Try QuantConnect for 1998-2026")
    print("   → Or use your existing 2-year hourly data")
    
    print()

if __name__ == "__main__":
    main()
