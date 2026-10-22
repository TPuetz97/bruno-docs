#!/usr/bin/env python3
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
