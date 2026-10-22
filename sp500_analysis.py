#!/usr/bin/env python3
"""
S&P 500 Opening vs Closing Analysis (1990-2026)
Analyzes if opening prices are higher or lower than previous day's closing prices
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def fetch_sp500_data(start_date="1990-01-01", end_date="2026-10-22"):
    """Fetch S&P 500 historical data"""
    print(f"Fetching S&P 500 data from {start_date} to {end_date}...")
    sp500 = yf.Ticker("^GSPC")
    df = sp500.history(start=start_date, end=end_date)
    print(f"Downloaded {len(df)} trading days")
    return df

def analyze_opening_vs_previous_close(df):
    """Analyze opening price vs previous day's closing price"""
    # Create previous close column
    df['Previous_Close'] = df['Close'].shift(1)
    
    # Calculate the difference
    df['Open_vs_Prev_Close'] = df['Open'] - df['Previous_Close']
    df['Open_Higher'] = df['Open_vs_Prev_Close'] > 0
    df['Open_Lower'] = df['Open_vs_Prev_Close'] < 0
    df['Open_Same'] = df['Open_vs_Prev_Close'] == 0
    
    # Remove first row (no previous close)
    df_analysis = df[1:]
    
    results = {
        'total_days': len(df_analysis),
        'open_higher': df_analysis['Open_Higher'].sum(),
        'open_lower': df_analysis['Open_Lower'].sum(),
        'open_same': df_analysis['Open_Same'].sum(),
        'avg_difference': df_analysis['Open_vs_Prev_Close'].mean(),
        'median_difference': df_analysis['Open_vs_Prev_Close'].median(),
        'std_difference': df_analysis['Open_vs_Prev_Close'].std(),
        'max_gap_up': df_analysis['Open_vs_Prev_Close'].max(),
        'max_gap_down': df_analysis['Open_vs_Prev_Close'].min(),
    }
    
    # Calculate percentages
    results['pct_higher'] = (results['open_higher'] / results['total_days']) * 100
    results['pct_lower'] = (results['open_lower'] / results['total_days']) * 100
    results['pct_same'] = (results['open_same'] / results['total_days']) * 100
    
    return df_analysis, results

def analyze_intraday_movements(df):
    """Analyze movement 1 hour after open and 1 hour before close"""
    # Note: Daily data doesn't have intraday prices
    # We'll use High/Low as proxies and analyze the ranges
    
    df['Daily_Range'] = df['High'] - df['Low']
    df['Open_to_High'] = df['High'] - df['Open']
    df['Open_to_Low'] = df['Low'] - df['Open']
    df['Close_from_High'] = df['Close'] - df['High']
    df['Close_from_Low'] = df['Close'] - df['Low']
    
    # Analyze if high/low occurred early or late in the day (approximation)
    df['High_Relative'] = (df['High'] - df['Open']) / df['Daily_Range']
    df['Close_Relative'] = (df['Close'] - df['Low']) / df['Daily_Range']
    
    intraday_results = {
        'avg_daily_range': df['Daily_Range'].mean(),
        'avg_open_to_high': df['Open_to_High'].mean(),
        'avg_open_to_low': df['Open_to_Low'].mean(),
        'days_closed_near_high': (df['Close'] >= df['High'] * 0.95).sum(),
        'days_closed_near_low': (df['Close'] <= df['Low'] * 1.05).sum(),
        'days_opened_near_low': (df['Open'] <= df['Low'] * 1.05).sum(),
        'days_opened_near_high': (df['Open'] >= df['High'] * 0.95).sum(),
    }
    
    return intraday_results

def analyze_by_decade(df):
    """Break down analysis by decade"""
    df['Year'] = df.index.year
    df['Decade'] = (df['Year'] // 10) * 10
    
    decade_results = {}
    
    for decade in sorted(df['Decade'].unique()):
        decade_df = df[df['Decade'] == decade]
        
        decade_results[f"{decade}s"] = {
            'total_days': len(decade_df),
            'open_higher': decade_df['Open_Higher'].sum(),
            'open_lower': decade_df['Open_Lower'].sum(),
            'pct_higher': (decade_df['Open_Higher'].sum() / len(decade_df)) * 100,
            'pct_lower': (decade_df['Open_Lower'].sum() / len(decade_df)) * 100,
            'avg_difference': decade_df['Open_vs_Prev_Close'].mean(),
        }
    
    return decade_results

def analyze_by_day_of_week(df):
    """Analyze patterns by day of week"""
    df['DayOfWeek'] = df.index.dayofweek
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    dow_results = {}
    
    for day_num, day_name in enumerate(day_names):
        day_df = df[df['DayOfWeek'] == day_num]
        if len(day_df) > 0:
            dow_results[day_name] = {
                'total_days': len(day_df),
                'open_higher': day_df['Open_Higher'].sum(),
                'open_lower': day_df['Open_Lower'].sum(),
                'pct_higher': (day_df['Open_Higher'].sum() / len(day_df)) * 100,
                'pct_lower': (day_df['Open_Lower'].sum() / len(day_df)) * 100,
                'avg_difference': day_df['Open_vs_Prev_Close'].mean(),
            }
    
    return dow_results

def main():
    print("=" * 80)
    print("S&P 500 Opening vs Closing Analysis (1990-2026)")
    print("=" * 80)
    print()
    
    # Fetch data
    df = fetch_sp500_data()
    
    # Main analysis
    print("\n" + "=" * 80)
    print("MAIN ANALYSIS: Opening vs Previous Day's Close")
    print("=" * 80)
    df_analysis, results = analyze_opening_vs_previous_close(df)
    
    print(f"\nTotal Trading Days Analyzed: {results['total_days']:,}")
    print(f"\nOpening HIGHER than previous close: {results['open_higher']:,} days ({results['pct_higher']:.2f}%)")
    print(f"Opening LOWER than previous close:  {results['open_lower']:,} days ({results['pct_lower']:.2f}%)")
    print(f"Opening SAME as previous close:     {results['open_same']:,} days ({results['pct_same']:.2f}%)")
    
    print(f"\nAverage Gap: ${results['avg_difference']:.2f}")
    print(f"Median Gap: ${results['median_difference']:.2f}")
    print(f"Standard Deviation: ${results['std_difference']:.2f}")
    print(f"Largest Gap Up: ${results['max_gap_up']:.2f}")
    print(f"Largest Gap Down: ${results['max_gap_down']:.2f}")
    
    # Intraday analysis
    print("\n" + "=" * 80)
    print("INTRADAY MOVEMENT ANALYSIS")
    print("=" * 80)
    print("Note: Using daily High/Low as proxies (no intraday data)")
    intraday = analyze_intraday_movements(df_analysis)
    
    print(f"\nAverage Daily Range: ${intraday['avg_daily_range']:.2f}")
    print(f"Average Open to High: ${intraday['avg_open_to_high']:.2f}")
    print(f"Average Open to Low: ${intraday['avg_open_to_low']:.2f}")
    print(f"\nDays closed near daily high (within 5%): {intraday['days_closed_near_high']:,}")
    print(f"Days closed near daily low (within 5%): {intraday['days_closed_near_low']:,}")
    print(f"Days opened near daily low (within 5%): {intraday['days_opened_near_low']:,}")
    print(f"Days opened near daily high (within 5%): {intraday['days_opened_near_high']:,}")
    
    # Decade analysis
    print("\n" + "=" * 80)
    print("ANALYSIS BY DECADE")
    print("=" * 80)
    decade_results = analyze_by_decade(df_analysis)
    
    for decade, stats in decade_results.items():
        print(f"\n{decade}:")
        print(f"  Total Days: {stats['total_days']:,}")
        print(f"  Higher: {stats['open_higher']:,} ({stats['pct_higher']:.2f}%)")
        print(f"  Lower: {stats['open_lower']:,} ({stats['pct_lower']:.2f}%)")
        print(f"  Avg Gap: ${stats['avg_difference']:.2f}")
    
    # Day of week analysis
    print("\n" + "=" * 80)
    print("ANALYSIS BY DAY OF WEEK")
    print("=" * 80)
    dow_results = analyze_by_day_of_week(df_analysis)
    
    for day, stats in dow_results.items():
        print(f"\n{day}:")
        print(f"  Total Days: {stats['total_days']:,}")
        print(f"  Higher: {stats['open_higher']:,} ({stats['pct_higher']:.2f}%)")
        print(f"  Lower: {stats['open_lower']:,} ({stats['pct_lower']:.2f}%)")
        print(f"  Avg Gap: ${stats['avg_difference']:.2f}")
    
    # Save results to JSON
    all_results = {
        'analysis_date': datetime.now().isoformat(),
        'period': '1990-01-01 to 2026-10-22',
        'overall': results,
        'intraday': intraday,
        'by_decade': decade_results,
        'by_day_of_week': dow_results,
    }
    
    with open('/workspace/sp500_analysis_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print("Results saved to: sp500_analysis_results.json")
    print("=" * 80)
    
    # Save detailed CSV
    df_analysis.to_csv('/workspace/sp500_detailed_data.csv')
    print("Detailed data saved to: sp500_detailed_data.csv")
    print()

if __name__ == "__main__":
    main()
