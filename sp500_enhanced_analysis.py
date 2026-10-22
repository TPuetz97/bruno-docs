#!/usr/bin/env python3
"""
Enhanced S&P 500 Analysis with Intraday Data
Attempts to get 1-hour after open and 1-hour before close data for recent years
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def fetch_recent_intraday_data(symbol="^GSPC", days_back=730):
    """
    Fetch recent intraday data (last 2 years) at 1-hour intervals
    Note: Yahoo Finance limits intraday data availability
    """
    print(f"\nAttempting to fetch intraday data for recent {days_back} days...")
    
    try:
        ticker = yf.Ticker(symbol)
        # Get 1-hour interval data for the last period allowed
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        df_1h = ticker.history(start=start_date, end=end_date, interval="1h")
        
        if not df_1h.empty:
            print(f"Successfully fetched {len(df_1h)} 1-hour candles")
            return df_1h
        else:
            print("No intraday data available")
            return None
    except Exception as e:
        print(f"Error fetching intraday data: {e}")
        return None

def analyze_intraday_1h_after_open_1h_before_close(df_1h):
    """
    Analyze price movement 1 hour after open and 1 hour before close
    """
    if df_1h is None or df_1h.empty:
        return None
    
    # Group by trading day
    df_1h['Date'] = df_1h.index.date
    df_1h['Time'] = df_1h.index.time
    
    results_by_day = []
    
    for date in df_1h['Date'].unique():
        day_data = df_1h[df_1h['Date'] == date].copy()
        day_data = day_data.sort_index()
        
        if len(day_data) < 2:
            continue
            
        # Get market open (first candle) and close (last candle)
        market_open = day_data.iloc[0]['Open']
        market_close = day_data.iloc[-1]['Close']
        
        # Try to get 1 hour after open (approximately second candle if 1h interval)
        if len(day_data) >= 2:
            one_hour_after_open = day_data.iloc[1]['Close']
        else:
            one_hour_after_open = None
            
        # Try to get 1 hour before close (approximately second-to-last candle)
        if len(day_data) >= 2:
            one_hour_before_close = day_data.iloc[-2]['Close']
        else:
            one_hour_before_close = None
        
        results_by_day.append({
            'date': date,
            'market_open': market_open,
            'market_close': market_close,
            'one_hour_after_open': one_hour_after_open,
            'one_hour_before_close': one_hour_before_close,
            'candles_in_day': len(day_data)
        })
    
    df_results = pd.DataFrame(results_by_day)
    
    # Calculate movements
    df_results['move_first_hour'] = df_results['one_hour_after_open'] - df_results['market_open']
    df_results['move_last_hour'] = df_results['market_close'] - df_results['one_hour_before_close']
    df_results['full_day_move'] = df_results['market_close'] - df_results['market_open']
    
    # Analyze patterns
    analysis = {
        'total_days_analyzed': len(df_results),
        'first_hour': {
            'avg_move': df_results['move_first_hour'].mean(),
            'positive_days': (df_results['move_first_hour'] > 0).sum(),
            'negative_days': (df_results['move_first_hour'] < 0).sum(),
            'pct_positive': ((df_results['move_first_hour'] > 0).sum() / len(df_results)) * 100,
            'pct_negative': ((df_results['move_first_hour'] < 0).sum() / len(df_results)) * 100,
        },
        'last_hour': {
            'avg_move': df_results['move_last_hour'].mean(),
            'positive_days': (df_results['move_last_hour'] > 0).sum(),
            'negative_days': (df_results['move_last_hour'] < 0).sum(),
            'pct_positive': ((df_results['move_last_hour'] > 0).sum() / len(df_results)) * 100,
            'pct_negative': ((df_results['move_last_hour'] < 0).sum() / len(df_results)) * 100,
        },
        'full_day': {
            'avg_move': df_results['full_day_move'].mean(),
            'positive_days': (df_results['full_day_move'] > 0).sum(),
            'negative_days': (df_results['full_day_move'] < 0).sum(),
        }
    }
    
    return analysis, df_results

def create_summary_statistics(df):
    """Create detailed summary statistics"""
    
    # Remove rows with NaN in crucial columns
    df_clean = df.dropna(subset=['Open_vs_Prev_Close'])
    
    summary = {
        'gaps_by_size': {
            'large_gap_up_over_50': (df_clean['Open_vs_Prev_Close'] > 50).sum(),
            'medium_gap_up_10_to_50': ((df_clean['Open_vs_Prev_Close'] > 10) & 
                                       (df_clean['Open_vs_Prev_Close'] <= 50)).sum(),
            'small_gap_up_0_to_10': ((df_clean['Open_vs_Prev_Close'] > 0) & 
                                     (df_clean['Open_vs_Prev_Close'] <= 10)).sum(),
            'small_gap_down_0_to_minus_10': ((df_clean['Open_vs_Prev_Close'] < 0) & 
                                             (df_clean['Open_vs_Prev_Close'] >= -10)).sum(),
            'medium_gap_down_minus_10_to_minus_50': ((df_clean['Open_vs_Prev_Close'] < -10) & 
                                                     (df_clean['Open_vs_Prev_Close'] >= -50)).sum(),
            'large_gap_down_under_minus_50': (df_clean['Open_vs_Prev_Close'] < -50).sum(),
        },
        'volatility': {
            'days_with_abs_gap_over_10': (abs(df_clean['Open_vs_Prev_Close']) > 10).sum(),
            'days_with_abs_gap_over_20': (abs(df_clean['Open_vs_Prev_Close']) > 20).sum(),
            'days_with_abs_gap_over_50': (abs(df_clean['Open_vs_Prev_Close']) > 50).sum(),
        }
    }
    
    return summary

def main():
    print("=" * 80)
    print("Enhanced S&P 500 Analysis with Intraday Data")
    print("=" * 80)
    
    # Load the previously generated analysis
    try:
        with open('/workspace/sp500_analysis_results.json', 'r') as f:
            main_results = json.load(f)
        print("\nLoaded main analysis results from previous run")
    except:
        print("\nMain analysis file not found. Run sp500_analysis.py first.")
        return
    
    # Try to fetch recent intraday data
    df_1h = fetch_recent_intraday_data(days_back=730)
    
    enhanced_results = {
        'main_analysis': main_results,
        'intraday_1h_analysis': None
    }
    
    if df_1h is not None:
        print("\n" + "=" * 80)
        print("INTRADAY ANALYSIS (Recent 2 Years)")
        print("=" * 80)
        
        intraday_analysis, intraday_df = analyze_intraday_1h_after_open_1h_before_close(df_1h)
        
        if intraday_analysis:
            print(f"\nAnalyzed {intraday_analysis['total_days_analyzed']} recent trading days")
            
            print("\n--- FIRST HOUR AFTER OPEN ---")
            print(f"Average movement: ${intraday_analysis['first_hour']['avg_move']:.2f}")
            print(f"Positive movements: {intraday_analysis['first_hour']['positive_days']} days "
                  f"({intraday_analysis['first_hour']['pct_positive']:.2f}%)")
            print(f"Negative movements: {intraday_analysis['first_hour']['negative_days']} days "
                  f"({intraday_analysis['first_hour']['pct_negative']:.2f}%)")
            
            print("\n--- LAST HOUR BEFORE CLOSE ---")
            print(f"Average movement: ${intraday_analysis['last_hour']['avg_move']:.2f}")
            print(f"Positive movements: {intraday_analysis['last_hour']['positive_days']} days "
                  f"({intraday_analysis['last_hour']['pct_positive']:.2f}%)")
            print(f"Negative movements: {intraday_analysis['last_hour']['negative_days']} days "
                  f"({intraday_analysis['last_hour']['pct_negative']:.2f}%)")
            
            enhanced_results['intraday_1h_analysis'] = intraday_analysis
            
            # Save intraday details
            intraday_df.to_csv('/workspace/sp500_intraday_details.csv')
            print("\nIntraday details saved to: sp500_intraday_details.csv")
    
    # Load the detailed data for additional statistics
    try:
        df_detailed = pd.read_csv('/workspace/sp500_detailed_data.csv', index_col=0, parse_dates=True)
        print("\n" + "=" * 80)
        print("ADDITIONAL GAP STATISTICS")
        print("=" * 80)
        
        summary_stats = create_summary_statistics(df_detailed)
        
        print("\nGaps by Size:")
        print(f"  Large gap up (>$50): {summary_stats['gaps_by_size']['large_gap_up_over_50']:,} days")
        print(f"  Medium gap up ($10-$50): {summary_stats['gaps_by_size']['medium_gap_up_10_to_50']:,} days")
        print(f"  Small gap up ($0-$10): {summary_stats['gaps_by_size']['small_gap_up_0_to_10']:,} days")
        print(f"  Small gap down ($0 to -$10): {summary_stats['gaps_by_size']['small_gap_down_0_to_minus_10']:,} days")
        print(f"  Medium gap down (-$10 to -$50): {summary_stats['gaps_by_size']['medium_gap_down_minus_10_to_minus_50']:,} days")
        print(f"  Large gap down (<-$50): {summary_stats['gaps_by_size']['large_gap_down_under_minus_50']:,} days")
        
        print("\nVolatility Events:")
        print(f"  Days with gap magnitude >$10: {summary_stats['volatility']['days_with_abs_gap_over_10']:,}")
        print(f"  Days with gap magnitude >$20: {summary_stats['volatility']['days_with_abs_gap_over_20']:,}")
        print(f"  Days with gap magnitude >$50: {summary_stats['volatility']['days_with_abs_gap_over_50']:,}")
        
        enhanced_results['gap_statistics'] = summary_stats
    except Exception as e:
        print(f"\nCould not load detailed data: {e}")
    
    # Save enhanced results
    with open('/workspace/sp500_enhanced_results.json', 'w') as f:
        json.dump(enhanced_results, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print("Enhanced results saved to: sp500_enhanced_results.json")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
