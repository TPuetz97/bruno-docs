#!/usr/bin/env python3
"""
How to Use Available Intraday Data (Last 2 Years)
Shows best practices for analyzing the available 1-hour S&P 500 data
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, time
import json

def fetch_maximum_intraday_data():
    """Fetch the maximum available intraday data (last 2 years, 1h interval)"""
    print("=" * 80)
    print("Fetching Maximum Available Intraday Data")
    print("=" * 80)
    print("\nSymbol: ^GSPC (S&P 500)")
    print("Interval: 1 hour")
    print("Period: Maximum (730 days)\n")
    
    ticker = yf.Ticker("^GSPC")
    df = ticker.history(period="max", interval="1h")
    
    print(f"✓ Downloaded: {len(df):,} hourly candles")
    print(f"✓ From: {df.index.min()}")
    print(f"✓ To: {df.index.max()}")
    print(f"✓ Trading days: {len(pd.Series(df.index.date).unique())}")
    
    return df

def identify_market_hours(df):
    """Identify opening hour, closing hour, and intraday periods"""
    print("\n" + "=" * 80)
    print("Identifying Trading Hours")
    print("=" * 80)
    
    # Add time components
    df['Date'] = df.index.date
    df['Time'] = df.index.time
    df['Hour'] = df.index.hour
    
    # Market typically opens at 9:30 ET and closes at 16:00 ET
    # In our hourly data, this translates to specific hour markers
    
    # Group by date to identify session structure
    daily_groups = df.groupby('Date')
    
    session_info = []
    
    for date, day_data in daily_groups:
        day_data = day_data.sort_index()
        
        if len(day_data) > 0:
            first_candle = day_data.iloc[0]
            last_candle = day_data.iloc[-1]
            
            session_info.append({
                'date': date,
                'num_candles': len(day_data),
                'first_candle_time': first_candle.name.time(),
                'last_candle_time': last_candle.name.time(),
                'open_price': first_candle['Open'],
                'close_price': last_candle['Close'],
            })
    
    df_sessions = pd.DataFrame(session_info)
    
    print(f"\nTotal trading days: {len(df_sessions)}")
    print(f"Average candles per day: {df_sessions['num_candles'].mean():.1f}")
    print(f"\nMost common first candle time: {df_sessions['first_candle_time'].mode()[0]}")
    print(f"Most common last candle time: {df_sessions['last_candle_time'].mode()[0]}")
    
    return df, df_sessions

def analyze_first_hour_movement(df, df_sessions):
    """Analyze movement in the first hour after market open"""
    print("\n" + "=" * 80)
    print("First Hour Analysis")
    print("=" * 80)
    
    results = []
    
    for date in df_sessions['date']:
        day_data = df[df['Date'] == date].sort_index()
        
        if len(day_data) >= 2:
            # First candle (opening hour)
            first_hour = day_data.iloc[0]
            # Second candle (hour after opening)
            second_hour = day_data.iloc[1]
            
            open_price = first_hour['Open']
            first_hour_close = first_hour['Close']
            second_hour_close = second_hour['Close']
            
            # Movement during first hour
            first_hour_move = first_hour_close - open_price
            first_hour_pct = (first_hour_move / open_price) * 100
            
            # Movement from open to end of second hour
            two_hour_move = second_hour_close - open_price
            two_hour_pct = (two_hour_move / open_price) * 100
            
            results.append({
                'date': date,
                'open': open_price,
                'first_hour_close': first_hour_close,
                'second_hour_close': second_hour_close,
                'first_hour_move': first_hour_move,
                'first_hour_pct': first_hour_pct,
                'two_hour_move': two_hour_move,
                'two_hour_pct': two_hour_pct,
            })
    
    df_first_hour = pd.DataFrame(results)
    
    # Statistics
    print(f"\nAnalyzed {len(df_first_hour)} trading days\n")
    
    print("FIRST HOUR (Hour 1 only):")
    print(f"  Average movement: ${df_first_hour['first_hour_move'].mean():.2f} ({df_first_hour['first_hour_pct'].mean():.3f}%)")
    print(f"  Median movement: ${df_first_hour['first_hour_move'].median():.2f}")
    print(f"  Positive days: {(df_first_hour['first_hour_move'] > 0).sum()} ({(df_first_hour['first_hour_move'] > 0).mean()*100:.2f}%)")
    print(f"  Negative days: {(df_first_hour['first_hour_move'] < 0).sum()} ({(df_first_hour['first_hour_move'] < 0).mean()*100:.2f}%)")
    
    print("\nFIRST TWO HOURS (Hour 1-2 combined):")
    print(f"  Average movement: ${df_first_hour['two_hour_move'].mean():.2f} ({df_first_hour['two_hour_pct'].mean():.3f}%)")
    print(f"  Median movement: ${df_first_hour['two_hour_move'].median():.2f}")
    print(f"  Positive days: {(df_first_hour['two_hour_move'] > 0).sum()} ({(df_first_hour['two_hour_move'] > 0).mean()*100:.2f}%)")
    print(f"  Negative days: {(df_first_hour['two_hour_move'] < 0).sum()} ({(df_first_hour['two_hour_move'] < 0).mean()*100:.2f}%)")
    
    return df_first_hour

def analyze_last_hour_movement(df, df_sessions):
    """Analyze movement in the last hour before market close"""
    print("\n" + "=" * 80)
    print("Last Hour Analysis")
    print("=" * 80)
    
    results = []
    
    for date in df_sessions['date']:
        day_data = df[df['Date'] == date].sort_index()
        
        if len(day_data) >= 2:
            # Second-to-last candle
            second_last = day_data.iloc[-2]
            # Last candle (closing hour)
            last_hour = day_data.iloc[-1]
            
            second_last_close = second_last['Close']
            close_price = last_hour['Close']
            
            # Movement during last hour
            last_hour_move = close_price - second_last_close
            last_hour_pct = (last_hour_move / second_last_close) * 100
            
            results.append({
                'date': date,
                'second_last_close': second_last_close,
                'final_close': close_price,
                'last_hour_move': last_hour_move,
                'last_hour_pct': last_hour_pct,
            })
    
    df_last_hour = pd.DataFrame(results)
    
    # Statistics
    print(f"\nAnalyzed {len(df_last_hour)} trading days\n")
    
    print("LAST HOUR:")
    print(f"  Average movement: ${df_last_hour['last_hour_move'].mean():.2f} ({df_last_hour['last_hour_pct'].mean():.3f}%)")
    print(f"  Median movement: ${df_last_hour['last_hour_move'].median():.2f}")
    print(f"  Positive days: {(df_last_hour['last_hour_move'] > 0).sum()} ({(df_last_hour['last_hour_move'] > 0).mean()*100:.2f}%)")
    print(f"  Negative days: {(df_last_hour['last_hour_move'] < 0).sum()} ({(df_last_hour['last_hour_move'] < 0).mean()*100:.2f}%)")
    
    return df_last_hour

def compare_opening_gap_with_first_hour(df_sessions, df_first_hour):
    """Compare overnight gap with first hour performance"""
    print("\n" + "=" * 80)
    print("Opening Gap vs First Hour Performance")
    print("=" * 80)
    
    # Merge session info with first hour data
    df_combined = pd.merge(
        df_sessions[['date', 'open_price', 'close_price']],
        df_first_hour[['date', 'first_hour_move', 'two_hour_move']],
        on='date'
    )
    
    # Calculate overnight gap (open vs previous close)
    df_combined = df_combined.sort_values('date')
    df_combined['prev_close'] = df_combined['close_price'].shift(1)
    df_combined['overnight_gap'] = df_combined['open_price'] - df_combined['prev_close']
    
    # Remove first row (no previous close)
    df_combined = df_combined.dropna(subset=['overnight_gap'])
    
    # Categorize by gap direction
    df_combined['gap_direction'] = 'neutral'
    df_combined.loc[df_combined['overnight_gap'] > 0, 'gap_direction'] = 'gap_up'
    df_combined.loc[df_combined['overnight_gap'] < 0, 'gap_direction'] = 'gap_down'
    
    print("\nPerformance after GAP UP days:")
    gap_up = df_combined[df_combined['gap_direction'] == 'gap_up']
    print(f"  Count: {len(gap_up)}")
    print(f"  Avg overnight gap: ${gap_up['overnight_gap'].mean():.2f}")
    print(f"  Avg first hour move: ${gap_up['first_hour_move'].mean():.2f}")
    print(f"  Avg two hour move: ${gap_up['two_hour_move'].mean():.2f}")
    print(f"  First hour continues up: {(gap_up['first_hour_move'] > 0).mean()*100:.1f}%")
    
    print("\nPerformance after GAP DOWN days:")
    gap_down = df_combined[df_combined['gap_direction'] == 'gap_down']
    print(f"  Count: {len(gap_down)}")
    print(f"  Avg overnight gap: ${gap_down['overnight_gap'].mean():.2f}")
    print(f"  Avg first hour move: ${gap_down['first_hour_move'].mean():.2f}")
    print(f"  Avg two hour move: ${gap_down['two_hour_move'].mean():.2f}")
    print(f"  First hour reverses (moves up): {(gap_down['first_hour_move'] > 0).mean()*100:.1f}%")
    
    return df_combined

def main():
    print("=" * 80)
    print("S&P 500 Intraday Data Analysis (Maximum Available)")
    print("Using Last 2 Years of Hourly Data")
    print("=" * 80)
    print()
    
    # Fetch data
    df = fetch_maximum_intraday_data()
    
    # Identify market structure
    df, df_sessions = identify_market_hours(df)
    
    # Analyze first hour
    df_first_hour = analyze_first_hour_movement(df, df_sessions)
    
    # Analyze last hour
    df_last_hour = analyze_last_hour_movement(df, df_sessions)
    
    # Compare gaps with first hour
    df_combined = compare_opening_gap_with_first_hour(df_sessions, df_first_hour)
    
    # Save detailed results
    print("\n" + "=" * 80)
    print("Saving Results")
    print("=" * 80)
    
    df_first_hour.to_csv('/workspace/first_hour_analysis.csv', index=False)
    print("✓ Saved: first_hour_analysis.csv")
    
    df_last_hour.to_csv('/workspace/last_hour_analysis.csv', index=False)
    print("✓ Saved: last_hour_analysis.csv")
    
    df_combined.to_csv('/workspace/gap_vs_first_hour.csv', index=False)
    print("✓ Saved: gap_vs_first_hour.csv")
    
    # Summary statistics
    summary = {
        'analysis_date': datetime.now().isoformat(),
        'data_range': {
            'from': str(df.index.min()),
            'to': str(df.index.max()),
            'trading_days': len(df_sessions),
            'hourly_candles': len(df),
        },
        'first_hour': {
            'avg_move_dollars': float(df_first_hour['first_hour_move'].mean()),
            'avg_move_percent': float(df_first_hour['first_hour_pct'].mean()),
            'positive_days': int((df_first_hour['first_hour_move'] > 0).sum()),
            'negative_days': int((df_first_hour['first_hour_move'] < 0).sum()),
            'pct_positive': float((df_first_hour['first_hour_move'] > 0).mean() * 100),
        },
        'last_hour': {
            'avg_move_dollars': float(df_last_hour['last_hour_move'].mean()),
            'avg_move_percent': float(df_last_hour['last_hour_pct'].mean()),
            'positive_days': int((df_last_hour['last_hour_move'] > 0).sum()),
            'negative_days': int((df_last_hour['last_hour_move'] < 0).sum()),
            'pct_positive': float((df_last_hour['last_hour_move'] > 0).mean() * 100),
        }
    }
    
    with open('/workspace/intraday_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("✓ Saved: intraday_summary.json")
    
    print("\n" + "=" * 80)
    print("Analysis Complete!")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
