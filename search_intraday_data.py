#!/usr/bin/env python3
"""
Search for S&P 500 Intraday Data going back to 1990
Tests multiple data sources and methods
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json

def test_yfinance_intraday_limits():
    """Test what intraday data is available through yfinance"""
    print("=" * 80)
    print("Testing yfinance Intraday Data Availability")
    print("=" * 80)
    
    ticker = yf.Ticker("^GSPC")
    
    intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]
    periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    
    results = []
    
    print("\nTesting different interval/period combinations...\n")
    
    # Test specific intervals with different periods
    test_combinations = [
        ("1m", "1d"),
        ("1m", "5d"),
        ("1m", "1mo"),
        ("5m", "1mo"),
        ("5m", "3mo"),
        ("15m", "3mo"),
        ("15m", "6mo"),
        ("30m", "6mo"),
        ("1h", "1y"),
        ("1h", "2y"),
        ("1h", "5y"),
        ("1h", "max"),
    ]
    
    for interval, period in test_combinations:
        try:
            print(f"Trying interval={interval}, period={period}...", end=" ")
            df = ticker.history(period=period, interval=interval)
            
            if not df.empty:
                start_date = df.index.min()
                end_date = df.index.max()
                num_candles = len(df)
                
                result = {
                    'interval': interval,
                    'period': period,
                    'success': True,
                    'num_candles': num_candles,
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'days_covered': (end_date - start_date).days
                }
                
                print(f"✓ SUCCESS: {num_candles} candles from {start_date.date()} to {end_date.date()}")
                results.append(result)
            else:
                print("✗ No data returned")
                results.append({
                    'interval': interval,
                    'period': period,
                    'success': False,
                    'error': 'Empty dataframe'
                })
        except Exception as e:
            print(f"✗ ERROR: {str(e)[:100]}")
            results.append({
                'interval': interval,
                'period': period,
                'success': False,
                'error': str(e)[:200]
            })
    
    return results

def test_specific_date_ranges():
    """Test fetching intraday data for specific historical date ranges"""
    print("\n" + "=" * 80)
    print("Testing Specific Historical Date Ranges")
    print("=" * 80)
    
    ticker = yf.Ticker("^GSPC")
    
    # Test different historical periods
    test_ranges = [
        ("2024-01-01", "2024-12-31", "1h", "2024 (1 year back)"),
        ("2023-01-01", "2023-12-31", "1h", "2023 (2 years back)"),
        ("2020-01-01", "2020-12-31", "1h", "2020 (Pandemic year)"),
        ("2015-01-01", "2015-12-31", "1h", "2015 (10 years back)"),
        ("2010-01-01", "2010-12-31", "1h", "2010 (15 years back)"),
        ("2000-01-01", "2000-12-31", "1h", "2000 (25 years back)"),
        ("1995-01-01", "1995-12-31", "1h", "1995 (30 years back)"),
        ("1990-01-01", "1990-12-31", "1h", "1990 (35 years back)"),
    ]
    
    results = []
    
    for start, end, interval, description in test_ranges:
        try:
            print(f"\nTrying {description}: {start} to {end}, interval={interval}...")
            df = ticker.history(start=start, end=end, interval=interval)
            
            if not df.empty:
                actual_start = df.index.min()
                actual_end = df.index.max()
                num_candles = len(df)
                
                print(f"  ✓ SUCCESS: {num_candles} candles from {actual_start.date()} to {actual_end.date()}")
                
                results.append({
                    'description': description,
                    'requested_start': start,
                    'requested_end': end,
                    'interval': interval,
                    'success': True,
                    'num_candles': num_candles,
                    'actual_start': str(actual_start),
                    'actual_end': str(actual_end),
                })
            else:
                print(f"  ✗ No data available")
                results.append({
                    'description': description,
                    'requested_start': start,
                    'requested_end': end,
                    'interval': interval,
                    'success': False,
                    'error': 'No data available'
                })
        except Exception as e:
            print(f"  ✗ ERROR: {str(e)[:150]}")
            results.append({
                'description': description,
                'requested_start': start,
                'requested_end': end,
                'interval': interval,
                'success': False,
                'error': str(e)[:200]
            })
    
    return results

def test_alternative_symbols():
    """Test if alternative S&P 500 symbols have better intraday data"""
    print("\n" + "=" * 80)
    print("Testing Alternative S&P 500 Symbols")
    print("=" * 80)
    
    # Different S&P 500 related symbols
    symbols = [
        ("^GSPC", "S&P 500 Index"),
        ("SPY", "SPDR S&P 500 ETF"),
        ("^SPX", "S&P 500 (alternative)"),
        ("ES=F", "E-mini S&P 500 Futures"),
    ]
    
    results = []
    
    for symbol, description in symbols:
        try:
            print(f"\nTesting {description} ({symbol})...")
            ticker = yf.Ticker(symbol)
            
            # Try 1h interval with max period
            df = ticker.history(period="max", interval="1h")
            
            if not df.empty:
                start_date = df.index.min()
                end_date = df.index.max()
                num_candles = len(df)
                years_covered = (end_date - start_date).days / 365.25
                
                print(f"  ✓ Available: {num_candles:,} 1h candles")
                print(f"  ✓ From: {start_date}")
                print(f"  ✓ To: {end_date}")
                print(f"  ✓ Coverage: {years_covered:.1f} years")
                
                results.append({
                    'symbol': symbol,
                    'description': description,
                    'success': True,
                    'num_candles': num_candles,
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'years_covered': years_covered
                })
            else:
                print(f"  ✗ No intraday data available")
                results.append({
                    'symbol': symbol,
                    'description': description,
                    'success': False,
                    'error': 'No data'
                })
        except Exception as e:
            print(f"  ✗ ERROR: {str(e)[:150]}")
            results.append({
                'symbol': symbol,
                'description': description,
                'success': False,
                'error': str(e)[:200]
            })
    
    return results

def summarize_findings(yf_results, date_results, symbol_results):
    """Create a summary of what intraday data is available"""
    print("\n" + "=" * 80)
    print("SUMMARY OF FINDINGS")
    print("=" * 80)
    
    # Find best available data
    successful_yf = [r for r in yf_results if r.get('success', False)]
    successful_dates = [r for r in date_results if r.get('success', False)]
    successful_symbols = [r for r in symbol_results if r.get('success', False)]
    
    summary = {
        'yfinance_limits': {
            'successful_combinations': len(successful_yf),
            'best_coverage': max([r.get('days_covered', 0) for r in successful_yf]) if successful_yf else 0,
            'max_candles': max([r.get('num_candles', 0) for r in successful_yf]) if successful_yf else 0,
        },
        'historical_availability': {
            'years_tested': len(date_results),
            'years_with_data': len(successful_dates),
            'oldest_available': None
        },
        'alternative_symbols': {
            'symbols_tested': len(symbol_results),
            'symbols_with_data': len(successful_symbols),
            'best_symbol': None
        }
    }
    
    # Find oldest available data
    if successful_dates:
        oldest = min(successful_dates, key=lambda x: x['actual_start'])
        summary['historical_availability']['oldest_available'] = {
            'year': oldest['description'],
            'start_date': oldest['actual_start'],
            'candles': oldest['num_candles']
        }
    
    # Find best symbol
    if successful_symbols:
        best = max(successful_symbols, key=lambda x: x.get('years_covered', 0))
        summary['alternative_symbols']['best_symbol'] = {
            'symbol': best['symbol'],
            'description': best['description'],
            'years_covered': best['years_covered'],
            'start_date': best['start_date']
        }
    
    print("\n🔍 Key Findings:")
    print(f"\n1. yfinance API Limits:")
    print(f"   - Successfully fetched {len(successful_yf)}/{len(yf_results)} combinations")
    if successful_yf:
        best_yf = max(successful_yf, key=lambda x: x.get('days_covered', 0))
        print(f"   - Best coverage: {best_yf['days_covered']} days ({best_yf['interval']} interval)")
        print(f"   - Max candles: {best_yf['num_candles']:,} candles")
        print(f"   - Date range: {best_yf['start_date']} to {best_yf['end_date']}")
    
    print(f"\n2. Historical Data Availability:")
    print(f"   - Tested {len(date_results)} different years")
    print(f"   - Found data for {len(successful_dates)} years")
    if summary['historical_availability']['oldest_available']:
        oldest_info = summary['historical_availability']['oldest_available']
        print(f"   - Oldest available: {oldest_info['year']}")
        print(f"   - Starting from: {oldest_info['start_date']}")
    
    print(f"\n3. Alternative Symbols:")
    print(f"   - Tested {len(symbol_results)} symbols")
    print(f"   - {len(successful_symbols)} have intraday data")
    if summary['alternative_symbols']['best_symbol']:
        best_sym = summary['alternative_symbols']['best_symbol']
        print(f"   - Best symbol: {best_sym['symbol']} ({best_sym['description']})")
        print(f"   - Coverage: {best_sym['years_covered']:.1f} years")
        print(f"   - Starts from: {best_sym['start_date']}")
    
    print("\n" + "=" * 80)
    print("CONCLUSION:")
    print("=" * 80)
    
    if successful_yf or successful_dates or successful_symbols:
        print("\n✓ Intraday data IS available, but with limitations:")
        print("\n  • Free APIs (like Yahoo Finance) typically limit intraday data to ~2 years")
        print("  • Older intraday data (pre-2020) is rarely available through free sources")
        print("  • For data back to 1990, you would need:")
        print("    - Paid data providers (Bloomberg, Refinitiv, QuantConnect, Polygon.io)")
        print("    - Historical tick databases")
        print("    - Academic/research databases (CRSP, Compustat)")
    else:
        print("\n✗ No intraday data found through tested free sources")
    
    print("\n  • RECOMMENDATION: Use daily OHLC data for long-term analysis (1990-2026)")
    print("  • For recent intraday analysis (last ~2 years), use available hourly data")
    
    return summary

def main():
    print("=" * 80)
    print("S&P 500 Intraday Data Search (1990-2026)")
    print("=" * 80)
    print("\nSearching for available intraday data sources...")
    print("This may take a few minutes...\n")
    
    # Run all tests
    yf_results = test_yfinance_intraday_limits()
    date_results = test_specific_date_ranges()
    symbol_results = test_alternative_symbols()
    
    # Summarize
    summary = summarize_findings(yf_results, date_results, symbol_results)
    
    # Save results
    all_results = {
        'search_date': datetime.now().isoformat(),
        'yfinance_tests': yf_results,
        'historical_date_tests': date_results,
        'alternative_symbol_tests': symbol_results,
        'summary': summary
    }
    
    with open('/workspace/intraday_data_search_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print("Results saved to: intraday_data_search_results.json")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
