#!/usr/bin/env python3
"""
Weekend Gap Analysis: Friday Close to Monday Open
Analyzes the special behavior of gaps over the weekend
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

def load_existing_data():
    """Load the previously generated detailed data"""
    print("=" * 80)
    print("Loading Existing S&P 500 Data (1990-2026)")
    print("=" * 80)
    
    df = pd.read_csv('/workspace/sp500_detailed_data.csv', index_col=0)
    
    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, utc=True)
    
    # Convert to timezone-naive for easier handling
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    
    print(f"\n✓ Loaded {len(df):,} trading days")
    print(f"✓ From: {df.index.min().date()}")
    print(f"✓ To: {df.index.max().date()}")
    
    return df

def identify_day_transitions(df):
    """Identify transitions between specific days of the week"""
    print("\n" + "=" * 80)
    print("Identifying Day-to-Day Transitions")
    print("=" * 80)
    
    # Add day of week information
    df['DayOfWeek'] = df.index.dayofweek
    df['DayName'] = df.index.day_name()
    
    # Shift to get previous day info
    df['Prev_DayOfWeek'] = df['DayOfWeek'].shift(1)
    df['Prev_DayName'] = df['DayName'].shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    
    # Calculate overnight gap (already exists, but let's be explicit)
    df['Overnight_Gap'] = df['Open'] - df['Prev_Close']
    
    # Identify specific transitions
    df['Transition'] = df['Prev_DayName'].fillna('') + ' → ' + df['DayName']
    
    # Remove first row (no previous day)
    df_transitions = df[1:].copy()
    
    print(f"\n✓ Identified {len(df_transitions):,} day-to-day transitions")
    
    return df_transitions

def analyze_weekend_gap(df):
    """Analyze Friday Close to Monday Open specifically"""
    print("\n" + "=" * 80)
    print("WEEKEND GAP ANALYSIS: Friday Close → Monday Open")
    print("=" * 80)
    
    # Filter for Monday openings (where previous day was Friday)
    # Monday is day 0, Friday is day 4
    weekend_gaps = df[(df['DayOfWeek'] == 0) & (df['Prev_DayOfWeek'] == 4)].copy()
    
    print(f"\n✓ Found {len(weekend_gaps)} Friday → Monday transitions")
    
    if len(weekend_gaps) == 0:
        print("⚠️  No weekend transitions found!")
        return None
    
    # Calculate statistics
    gap_stats = {
        'total_transitions': len(weekend_gaps),
        'gap_higher': (weekend_gaps['Overnight_Gap'] > 0).sum(),
        'gap_lower': (weekend_gaps['Overnight_Gap'] < 0).sum(),
        'gap_same': (weekend_gaps['Overnight_Gap'] == 0).sum(),
        'pct_higher': (weekend_gaps['Overnight_Gap'] > 0).mean() * 100,
        'pct_lower': (weekend_gaps['Overnight_Gap'] < 0).mean() * 100,
        'pct_same': (weekend_gaps['Overnight_Gap'] == 0).mean() * 100,
        'avg_gap': weekend_gaps['Overnight_Gap'].mean(),
        'median_gap': weekend_gaps['Overnight_Gap'].median(),
        'std_gap': weekend_gaps['Overnight_Gap'].std(),
        'min_gap': weekend_gaps['Overnight_Gap'].min(),
        'max_gap': weekend_gaps['Overnight_Gap'].max(),
    }
    
    print(f"\nTotal Friday → Monday transitions: {gap_stats['total_transitions']:,}")
    print(f"\nMonday HÖHER als Freitag-Close: {gap_stats['gap_higher']:,} ({gap_stats['pct_higher']:.2f}%)")
    print(f"Monday NIEDRIGER als Freitag-Close: {gap_stats['gap_lower']:,} ({gap_stats['pct_lower']:.2f}%)")
    print(f"Monday GLEICH wie Freitag-Close: {gap_stats['gap_same']:,} ({gap_stats['pct_same']:.2f}%)")
    
    print(f"\nDurchschnittlicher Weekend-Gap: ${gap_stats['avg_gap']:.2f}")
    print(f"Median Weekend-Gap: ${gap_stats['median_gap']:.2f}")
    print(f"Standardabweichung: ${gap_stats['std_gap']:.2f}")
    print(f"Größter positiver Gap: ${gap_stats['max_gap']:.2f}")
    print(f"Größter negativer Gap: ${gap_stats['min_gap']:.2f}")
    
    return weekend_gaps, gap_stats

def analyze_all_weekday_transitions(df):
    """Analyze gaps for all weekday-to-weekday transitions"""
    print("\n" + "=" * 80)
    print("ALL WEEKDAY TRANSITIONS")
    print("=" * 80)
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Define expected transitions (consecutive trading days)
    expected_transitions = [
        (0, 4, 'Friday → Monday'),  # Weekend
        (1, 0, 'Monday → Tuesday'),
        (2, 1, 'Tuesday → Wednesday'),
        (3, 2, 'Wednesday → Thursday'),
        (4, 3, 'Thursday → Friday'),
    ]
    
    transition_stats = {}
    
    for current_day, prev_day, label in expected_transitions:
        transitions = df[(df['DayOfWeek'] == current_day) & 
                        (df['Prev_DayOfWeek'] == prev_day)].copy()
        
        if len(transitions) > 0:
            stats = {
                'label': label,
                'count': len(transitions),
                'gap_higher': (transitions['Overnight_Gap'] > 0).sum(),
                'gap_lower': (transitions['Overnight_Gap'] < 0).sum(),
                'pct_higher': (transitions['Overnight_Gap'] > 0).mean() * 100,
                'pct_lower': (transitions['Overnight_Gap'] < 0).mean() * 100,
                'avg_gap': transitions['Overnight_Gap'].mean(),
                'median_gap': transitions['Overnight_Gap'].median(),
                'std_gap': transitions['Overnight_Gap'].std(),
            }
            
            transition_stats[label] = stats
            
            print(f"\n{label}:")
            print(f"  Anzahl: {stats['count']:,}")
            print(f"  Höher: {stats['gap_higher']:,} ({stats['pct_higher']:.2f}%)")
            print(f"  Niedriger: {stats['gap_lower']:,} ({stats['pct_lower']:.2f}%)")
            print(f"  Durchschn. Gap: ${stats['avg_gap']:.2f}")
    
    return transition_stats

def analyze_weekend_gap_by_decade(weekend_gaps):
    """Break down weekend gaps by decade"""
    print("\n" + "=" * 80)
    print("WEEKEND GAP BY DECADE")
    print("=" * 80)
    
    weekend_gaps['Year'] = weekend_gaps.index.year
    weekend_gaps['Decade'] = (weekend_gaps['Year'] // 10) * 10
    
    decade_stats = {}
    
    for decade in sorted(weekend_gaps['Decade'].unique()):
        decade_data = weekend_gaps[weekend_gaps['Decade'] == decade]
        
        stats = {
            'count': len(decade_data),
            'gap_higher': (decade_data['Overnight_Gap'] > 0).sum(),
            'gap_lower': (decade_data['Overnight_Gap'] < 0).sum(),
            'pct_higher': (decade_data['Overnight_Gap'] > 0).mean() * 100,
            'pct_lower': (decade_data['Overnight_Gap'] < 0).mean() * 100,
            'avg_gap': decade_data['Overnight_Gap'].mean(),
        }
        
        decade_stats[f"{decade}s"] = stats
        
        print(f"\n{decade}s:")
        print(f"  Anzahl: {stats['count']:,}")
        print(f"  Höher: {stats['gap_higher']:,} ({stats['pct_higher']:.2f}%)")
        print(f"  Niedriger: {stats['gap_lower']:,} ({stats['pct_lower']:.2f}%)")
        print(f"  Durchschn. Gap: ${stats['avg_gap']:.2f}")
    
    return decade_stats

def compare_weekend_vs_other_days(transition_stats):
    """Compare weekend gap with other weekday gaps"""
    print("\n" + "=" * 80)
    print("WEEKEND vs. OTHER WEEKDAYS COMPARISON")
    print("=" * 80)
    
    if 'Friday → Monday' not in transition_stats:
        print("⚠️  No weekend data available for comparison")
        return
    
    weekend = transition_stats['Friday → Monday']
    
    # Calculate average for other weekdays
    other_transitions = [k for k in transition_stats.keys() if k != 'Friday → Monday']
    
    other_avg_gap = np.mean([transition_stats[k]['avg_gap'] for k in other_transitions])
    other_avg_pct_higher = np.mean([transition_stats[k]['pct_higher'] for k in other_transitions])
    
    print(f"\nWEEKEND (Friday → Monday):")
    print(f"  Durchschnittlicher Gap: ${weekend['avg_gap']:.2f}")
    print(f"  Prozent höher: {weekend['pct_higher']:.2f}%")
    
    print(f"\nANDERE WOCHENTAGE (Durchschnitt):")
    print(f"  Durchschnittlicher Gap: ${other_avg_gap:.2f}")
    print(f"  Prozent höher: {other_avg_pct_higher:.2f}%")
    
    print(f"\nUNTERSCHIED:")
    gap_diff = weekend['avg_gap'] - other_avg_gap
    pct_diff = weekend['pct_higher'] - other_avg_pct_higher
    
    print(f"  Gap-Differenz: ${gap_diff:.2f} ({'höher' if gap_diff > 0 else 'niedriger'})")
    print(f"  Prozent-Differenz: {pct_diff:+.2f} Prozentpunkte")
    
    if gap_diff > 0:
        print(f"\n✓ Weekend-Gaps sind im Durchschnitt POSITIVER als Wochentags-Gaps")
    elif gap_diff < 0:
        print(f"\n✓ Weekend-Gaps sind im Durchschnitt NEGATIVER als Wochentags-Gaps")
    else:
        print(f"\n✓ Weekend-Gaps und Wochentags-Gaps sind ähnlich")
    
    comparison = {
        'weekend': {
            'avg_gap': weekend['avg_gap'],
            'pct_higher': weekend['pct_higher'],
        },
        'other_weekdays': {
            'avg_gap': other_avg_gap,
            'pct_higher': other_avg_pct_higher,
        },
        'difference': {
            'gap_diff': gap_diff,
            'pct_diff': pct_diff,
        }
    }
    
    return comparison

def analyze_monday_performance_after_weekend_gap(df, weekend_gaps):
    """Analyze how Monday performs based on weekend gap direction"""
    print("\n" + "=" * 80)
    print("MONDAY PERFORMANCE AFTER WEEKEND GAP")
    print("=" * 80)
    
    # Calculate Monday's intraday performance
    weekend_gaps['Monday_Close'] = weekend_gaps['Close']
    weekend_gaps['Monday_Open'] = weekend_gaps['Open']
    weekend_gaps['Monday_Intraday_Move'] = weekend_gaps['Monday_Close'] - weekend_gaps['Monday_Open']
    weekend_gaps['Monday_Total_From_Fri'] = weekend_gaps['Monday_Close'] - weekend_gaps['Prev_Close']
    
    # Categorize by gap direction
    gap_up = weekend_gaps[weekend_gaps['Overnight_Gap'] > 0]
    gap_down = weekend_gaps[weekend_gaps['Overnight_Gap'] < 0]
    
    print(f"\nNach WEEKEND GAP UP ({len(gap_up)} Tage):")
    print(f"  Durchschn. Weekend-Gap: ${gap_up['Overnight_Gap'].mean():.2f}")
    print(f"  Durchschn. Montag Intraday: ${gap_up['Monday_Intraday_Move'].mean():.2f}")
    print(f"  Montag schließt höher: {(gap_up['Monday_Intraday_Move'] > 0).sum()} ({(gap_up['Monday_Intraday_Move'] > 0).mean()*100:.1f}%)")
    print(f"  Montag schließt niedriger: {(gap_up['Monday_Intraday_Move'] < 0).sum()} ({(gap_up['Monday_Intraday_Move'] < 0).mean()*100:.1f}%)")
    print(f"  Gesamt-Move von Freitag: ${gap_up['Monday_Total_From_Fri'].mean():.2f}")
    
    print(f"\nNach WEEKEND GAP DOWN ({len(gap_down)} Tage):")
    print(f"  Durchschn. Weekend-Gap: ${gap_down['Overnight_Gap'].mean():.2f}")
    print(f"  Durchschn. Montag Intraday: ${gap_down['Monday_Intraday_Move'].mean():.2f}")
    print(f"  Montag schließt höher: {(gap_down['Monday_Intraday_Move'] > 0).sum()} ({(gap_down['Monday_Intraday_Move'] > 0).mean()*100:.1f}%)")
    print(f"  Montag schließt niedriger: {(gap_down['Monday_Intraday_Move'] < 0).sum()} ({(gap_down['Monday_Intraday_Move'] < 0).mean()*100:.1f}%)")
    print(f"  Gesamt-Move von Freitag: ${gap_down['Monday_Total_From_Fri'].mean():.2f}")
    
    monday_performance = {
        'gap_up': {
            'count': len(gap_up),
            'avg_weekend_gap': float(gap_up['Overnight_Gap'].mean()),
            'avg_monday_intraday': float(gap_up['Monday_Intraday_Move'].mean()),
            'pct_monday_up': float((gap_up['Monday_Intraday_Move'] > 0).mean() * 100),
            'avg_total_from_friday': float(gap_up['Monday_Total_From_Fri'].mean()),
        },
        'gap_down': {
            'count': len(gap_down),
            'avg_weekend_gap': float(gap_down['Overnight_Gap'].mean()),
            'avg_monday_intraday': float(gap_down['Monday_Intraday_Move'].mean()),
            'pct_monday_up': float((gap_down['Monday_Intraday_Move'] > 0).mean() * 100),
            'avg_total_from_friday': float(gap_down['Monday_Total_From_Fri'].mean()),
        }
    }
    
    return monday_performance

def main():
    print("=" * 80)
    print("S&P 500 Weekend Gap Analysis")
    print("Friday Close → Monday Open (1990-2026)")
    print("=" * 80)
    print()
    
    # Load data
    df = load_existing_data()
    
    # Identify transitions
    df_transitions = identify_day_transitions(df)
    
    # Analyze weekend gap
    weekend_gaps, weekend_stats = analyze_weekend_gap(df_transitions)
    
    # Analyze all weekday transitions
    transition_stats = analyze_all_weekday_transitions(df_transitions)
    
    # Decade breakdown
    decade_stats = analyze_weekend_gap_by_decade(weekend_gaps)
    
    # Compare weekend vs other days
    comparison = compare_weekend_vs_other_days(transition_stats)
    
    # Monday performance after gap
    monday_perf = analyze_monday_performance_after_weekend_gap(df_transitions, weekend_gaps)
    
    # Save results
    print("\n" + "=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    
    all_results = {
        'analysis_date': datetime.now().isoformat(),
        'period': '1990-01-01 to 2026-10-22',
        'weekend_gap_stats': weekend_stats,
        'all_transitions': {k: v for k, v in transition_stats.items()},
        'weekend_by_decade': decade_stats,
        'weekend_vs_weekdays': comparison,
        'monday_performance': monday_perf,
    }
    
    with open('/workspace/weekend_gap_analysis.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print("\n✓ Saved: weekend_gap_analysis.json")
    
    weekend_gaps.to_csv('/workspace/weekend_gaps_detailed.csv')
    print("✓ Saved: weekend_gaps_detailed.csv")
    
    print("\n" + "=" * 80)
    print("Analysis Complete!")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
