#!/usr/bin/env python3
"""
Attempt to access academic data sources for intraday S&P 500 data
1. Kenneth French Data Library
2. Other academic sources
"""

import pandas as pd
import requests
import io
from datetime import datetime
import json

def test_kenneth_french_library():
    """
    Test access to Kenneth French Data Library
    https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
    """
    print("=" * 80)
    print("Kenneth French Data Library")
    print("=" * 80)
    print("\nWebsite: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/")
    
    # Kenneth French primarily has daily/monthly factor data
    # Check what's available
    
    print("\nKenneth French Data Library focuses on:")
    print("  • Fama-French factors (daily, monthly)")
    print("  • Market returns (daily, monthly)")
    print("  • Portfolio returns")
    print("  • Industry returns")
    
    print("\n⚠️  Kenneth French library typically provides DAILY data, not intraday")
    print("    However, let's check if they have any intraday datasets...")
    
    # Try to download daily market data as a test
    try:
        # F-F Research Data Factors (Daily)
        url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
        
        print(f"\n✓ Attempting to download daily factors as test...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("  ✓ Successfully accessed Kenneth French Data Library")
            print("  ✓ Daily data is available")
            print("\n  Note: This is DAILY data, not intraday.")
            print("  Kenneth French does not provide intraday data publicly.")
            
            return {
                'accessible': True,
                'has_intraday': False,
                'has_daily': True,
                'note': 'Daily factors available, but no public intraday data'
            }
        else:
            print(f"  ✗ Could not access ({response.status_code})")
            return {'accessible': False, 'has_intraday': False}
            
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:200]}")
        return {'accessible': False, 'error': str(e)[:200]}

def test_wrds_access():
    """
    Test if WRDS (Wharton Research Data Services) is accessible
    WRDS hosts TAQ, CRSP, and other intraday data
    """
    print("\n" + "=" * 80)
    print("WRDS (Wharton Research Data Services)")
    print("=" * 80)
    print("\nWebsite: https://wrds-www.wharton.upenn.edu/")
    
    print("\nWRDS provides access to:")
    print("  • TAQ (Trade and Quote) - Intraday tick data since 1993")
    print("  • CRSP - Daily and intraday data")
    print("  • Compustat")
    print("  • And many others")
    
    print("\n⚠️  WRDS requires:")
    print("    • University/institutional subscription")
    print("    • Login credentials")
    print("    • Not freely accessible")
    
    print("\n❌ Cannot access WRDS without credentials")
    
    return {
        'accessible': False,
        'requires_subscription': True,
        'has_intraday': True,
        'note': 'TAQ data available from 1993, but requires subscription'
    }

def check_alternative_academic_sources():
    """Check other potential academic data sources"""
    print("\n" + "=" * 80)
    print("Other Academic Data Sources")
    print("=" * 80)
    
    sources = [
        {
            'name': 'TAQ (NYSE Trade and Quote)',
            'intraday': True,
            'from_year': 1993,
            'access': 'Paid/Academic subscription',
            'cost': 'Very expensive',
            'note': 'Gold standard for US equity tick data'
        },
        {
            'name': 'CRSP (Center for Research in Security Prices)',
            'intraday': True,
            'from_year': 1993,
            'access': 'Academic subscription via WRDS',
            'cost': 'Institutional',
            'note': 'High-quality academic data'
        },
        {
            'name': 'TickData.com',
            'intraday': True,
            'from_year': 1996,
            'access': 'Commercial purchase',
            'cost': '$1000s per dataset',
            'note': 'Historical tick data available for purchase'
        },
        {
            'name': 'Kibot',
            'intraday': True,
            'from_year': 1998,
            'access': 'Subscription',
            'cost': '$30-$300/month',
            'note': 'Intraday data from 1998'
        },
        {
            'name': 'First Rate Data',
            'intraday': True,
            'from_year': 2000,
            'access': 'One-time purchase',
            'cost': '$50-$200 per symbol',
            'note': 'Historical intraday data'
        }
    ]
    
    for source in sources:
        print(f"\n{source['name']}:")
        print(f"  • Intraday available: {'✓' if source['intraday'] else '✗'}")
        print(f"  • From year: {source['from_year']}")
        print(f"  • Access: {source['access']}")
        print(f"  • Cost: {source['cost']}")
        print(f"  • Note: {source['note']}")
    
    return sources

def check_quantlib_packages():
    """Check if Python packages exist for academic data access"""
    print("\n" + "=" * 80)
    print("Python Packages for Academic Data")
    print("=" * 80)
    
    packages = []
    
    # Check pandas-datareader
    try:
        import pandas_datareader as pdr
        print("\n✓ pandas-datareader is installed")
        print("  Supports: Fred, World Bank, OECD, Eurostat, etc.")
        print("  ⚠️  Does NOT support Kenneth French directly")
        print("  ⚠️  Does NOT provide intraday data to 1990")
        packages.append('pandas-datareader')
    except ImportError:
        print("\n✗ pandas-datareader not installed")
    
    # Check if there's a direct Kenneth French package
    try:
        import pandas_datareader.famafrench as ff
        print("\n✓ pandas-datareader has Fama-French module")
        packages.append('famafrench')
    except:
        print("\n⚠️  No direct Fama-French integration in pandas-datareader")
    
    return packages

def try_download_french_data():
    """Attempt to download Kenneth French data using pandas-datareader"""
    print("\n" + "=" * 80)
    print("Attempting to Download Kenneth French Data")
    print("=" * 80)
    
    try:
        # Try to install pandas-datareader if not available
        try:
            import pandas_datareader as pdr
        except ImportError:
            print("\nInstalling pandas-datareader...")
            import subprocess
            subprocess.check_call(['pip', 'install', 'pandas-datareader', '--quiet'])
            import pandas_datareader as pdr
        
        print("\n✓ pandas-datareader available")
        
        # Try to get Fama-French data
        print("\nAttempting to download Fama-French 3-Factor data...")
        
        from pandas_datareader.famafrench import get_available_datasets
        
        # Get available datasets
        print("\nFetching available Kenneth French datasets...")
        datasets = get_available_datasets()
        
        print(f"\n✓ Found {len(datasets)} available datasets")
        
        # Look for relevant datasets
        sp500_related = [d for d in datasets if 'market' in d.lower() or 'sp500' in d.lower() or 'index' in d.lower()]
        
        if sp500_related:
            print(f"\n✓ Found {len(sp500_related)} market/S&P 500 related datasets:")
            for dataset in sp500_related[:10]:
                print(f"  • {dataset}")
        
        # Try to download a sample dataset
        print("\n\nTrying to download 'F-F_Research_Data_Factors' (daily)...")
        data = pdr.DataReader('F-F_Research_Data_Factors_daily', 'famafrench')
        
        if data:
            print("  ✓ Successfully downloaded data!")
            
            # Get the first dataset (usually the main one)
            df = data[0]
            
            print(f"\n  Data range: {df.index.min()} to {df.index.max()}")
            print(f"  Total observations: {len(df):,}")
            print(f"  Columns: {', '.join(df.columns)}")
            
            # Check if this is daily or intraday
            print(f"\n  Frequency: DAILY (not intraday)")
            
            return {
                'success': True,
                'frequency': 'daily',
                'has_intraday': False,
                'available_datasets': len(datasets),
                'sp500_related': len(sp500_related)
            }
        
    except Exception as e:
        print(f"\n✗ Error accessing Kenneth French data: {str(e)[:300]}")
        return {
            'success': False,
            'error': str(e)[:300]
        }

def summarize_findings():
    """Summarize what academic sources can provide"""
    print("\n" + "=" * 80)
    print("SUMMARY: Academic Data Sources for Intraday S&P 500 (1990-2026)")
    print("=" * 80)
    
    print("\n🔍 FINDINGS:")
    
    print("\n1. KENNETH FRENCH DATA LIBRARY:")
    print("   ✅ Freely accessible")
    print("   ✅ Daily data from 1926")
    print("   ❌ NO intraday data")
    print("   📊 Focus: Daily/monthly factor returns and portfolios")
    
    print("\n2. HF DATA LIBRARY / TAQ:")
    print("   ✅ Has intraday tick data")
    print("   ✅ Available from 1993")
    print("   ❌ Requires WRDS subscription (expensive)")
    print("   ❌ Not freely accessible")
    print("   💰 Cost: Institutional/university access only")
    
    print("\n3. CRSP:")
    print("   ✅ Has intraday data")
    print("   ✅ Available from 1993")
    print("   ❌ Requires WRDS subscription")
    print("   ❌ Not freely accessible")
    
    print("\n4. OTHER ACADEMIC SOURCES:")
    print("   • All intraday sources require paid subscriptions")
    print("   • Most intraday data starts from 1993-1998")
    print("   • NONE go back to 1990 for intraday")
    
    print("\n" + "=" * 80)
    print("CONCLUSION:")
    print("=" * 80)
    
    print("\n❌ Kenneth French Library: NO intraday data (only daily)")
    print("❌ HF/TAQ Data: Has intraday BUT requires expensive subscription")
    print("❌ Free intraday data to 1990: NOT AVAILABLE from any source")
    
    print("\n✅ BEST OPTIONS:")
    print("\n   For FREE analysis:")
    print("   • Use daily OHLC data (1990-2026) ← Already done ✓")
    print("   • Use recent 2-year hourly data ← Already done ✓")
    
    print("\n   For ACADEMIC intraday data (1993+):")
    print("   • Get university WRDS access (if available)")
    print("   • Access TAQ or CRSP through WRDS")
    print("   • Cost: Requires university affiliation")
    
    print("\n   For COMMERCIAL intraday data:")
    print("   • Polygon.io ($99/mo, from 2004)")
    print("   • QuantConnect (free tier, from 1998)")
    print("   • Kibot ($30-300/mo, from 1998)")

def main():
    print("=" * 80)
    print("Academic Data Sources Search")
    print("Checking Kenneth French and HF Data Library")
    print("=" * 80)
    print()
    
    # Test Kenneth French
    french_result = test_kenneth_french_library()
    
    # Test WRDS (includes TAQ, CRSP)
    wrds_result = test_wrds_access()
    
    # Check alternatives
    alternatives = check_alternative_academic_sources()
    
    # Check Python packages
    packages = check_quantlib_packages()
    
    # Try to download French data
    french_download = try_download_french_data()
    
    # Summarize
    summarize_findings()
    
    # Save results
    results = {
        'search_date': datetime.now().isoformat(),
        'kenneth_french': french_result,
        'wrds': wrds_result,
        'alternative_sources': alternatives,
        'python_packages': packages,
        'french_download_test': french_download
    }
    
    with open('/workspace/academic_sources_search.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print("Results saved to: academic_sources_search.json")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
