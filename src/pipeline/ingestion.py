"""
Step 1: Ingestion & Aggregation (Engine 3: Ingestion Layer)
Handles Real OGD Aggregated Data (Enrolment, Biometric, Demographic).
Outputs:
1. master_pincode_risk.csv -> For Map, Route Optimizer, Sankey.
2. master_time_series.csv -> For ARIMA.
"""

import pandas as pd
import glob
import os
from datetime import datetime

# CONFIG
ROOT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar"
OUT_DIR = os.path.join(ROOT_DIR, "data", "processed")
os.makedirs(OUT_DIR, exist_ok=True)

def aggregate_data():
    print("🚀 [Step 1] Starting Aggregated Data Ingestion...")

    # Pattern Matching
    enrol_files = glob.glob(os.path.join(ROOT_DIR, "api_data_aadhar_enrolment", "**", "*.csv"), recursive=True)
    bio_files = glob.glob(os.path.join(ROOT_DIR, "api_data_aadhar_biometric", "**", "*.csv"), recursive=True)
    demo_files = glob.glob(os.path.join(ROOT_DIR, "api_data_aadhar_demographic", "**", "*.csv"), recursive=True)

    print(f"   found {len(enrol_files)} Enrolment files")
    print(f"   found {len(bio_files)} Biometric files")
    print(f"   found {len(demo_files)} Demographic files")

    # --- 1. Time Series Aggregation (For ARIMA) ---
    print("   ⏳ Building Time Series Data...")
    
    daily_stats = {} # date -> {enrol:0, update:0}

    def process_time(file_list, type_key):
        for f in file_list:
            try:
                # Read chunks, assuming 'date' column exists. Sum counts.
                # Inspect columns dynamically
                df = pd.read_csv(f, usecols=lambda c: 'date' in c.lower() or 'count' in c.lower() or 'age' in c.lower())
                
                # Normalize columns
                df.columns = [c.lower() for c in df.columns]
                
                if 'date' not in df.columns: 
                    # Try parsing filename date if inside? Unlikely. Skip.
                    continue

                # Identify Count Columns (all numeric except date/pincode)
                count_cols = [c for c in df.columns if c not in ['date', 'pincode', 'state', 'district']]
                
                # Group by Date
                grouped = df.groupby('date')[count_cols].sum().sum(axis=1) # Sum all age buckets
                
                for date, count in grouped.items():
                    if date not in daily_stats: daily_stats[date] = {'enrol': 0, 'update': 0}
                    key = 'enrol' if type_key == 'enrol' else 'update'
                    daily_stats[date][key] += count
                    
            except Exception as e:
                print(f"     Skipping {os.path.basename(f)}: {e}")

    process_time(enrol_files, 'enrol')
    process_time(bio_files, 'update') # Bio is update
    process_time(demo_files, 'update') # Demo is update

    ts_data = []
    for date, val in daily_stats.items():
        ts_data.append({'date': date, 'enrolment_count': val['enrol'], 'update_count': val['update']})
    
    df_ts = pd.DataFrame(ts_data)
    df_ts.to_csv(os.path.join(OUT_DIR, "master_time_series.csv"), index=False)
    print("   ✅ Saved master_time_series.csv")

    # --- 2. Pincode Risk Aggregation (For Map/K-Means) ---
    print("   🌍 Building Pincode Risk Data...")
    
    pin_stats = {} # pin -> {enrol:0, update:0}

    def process_pin(file_list, type_key):
        for f in file_list:
            try:
                df = pd.read_csv(f, usecols=lambda c: 'pincode' in c.lower() or 'count' in c.lower() or 'age' in c.lower())
                df.columns = [c.lower() for c in df.columns]
                
                if 'pincode' not in df.columns: continue

                count_cols = [c for c in df.columns if c not in ['date', 'pincode', 'state', 'district']]
                
                # Group by Pincode
                grouped = df.groupby('pincode')[count_cols].sum().sum(axis=1)
                
                for pin, count in grouped.items():
                    if pin not in pin_stats: pin_stats[pin] = {'enrol': 0, 'update': 0}
                    key = 'enrol' if type_key == 'enrol' else 'update'
                    pin_stats[pin][key] += count
            except: pass

    process_pin(enrol_files, 'enrol')
    process_pin(bio_files, 'update')
    process_pin(demo_files, 'update')

    pin_data = []
    for pin, val in pin_stats.items():
        pin_data.append({'Pincode': pin, 'Enrolment_Count': val['enrol'], 'Update_Count': val['update']})
        
    df_pin = pd.DataFrame(pin_data)
    df_pin.to_csv(os.path.join(OUT_DIR, "master_pincode_risk.csv"), index=False)
    print("   ✅ Saved master_pincode_risk.csv")

if __name__ == "__main__":
    aggregate_data()
