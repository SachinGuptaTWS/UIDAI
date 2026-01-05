"""
Engine 1: The "Time Machine" (Forecasting Engine)
Input: master_time_series.csv (Date | Enrolment | Update)
Model: ARIMA
"""

import pandas as pd
import json
import os
import sys
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_time_series.csv"
OUTPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\outputs\forecast_data.json"

def run_time_machine():
    print("🚀 [Engine 1] Starting 'Time Machine' Forecast...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    # Fix Date Parsing (DD-MM-YYYY) - Explicit Format
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    df.dropna(subset=['date'], inplace=True)
    df.set_index('date', inplace=True)
    
    # Resample to Monthly (sum) in case it's daily
    monthly_data = df['update_count'].resample('M').sum()
    
    print(f"   📈 Time points: {len(monthly_data)}")
    
    # Train ARIMA
    try:
        model = ARIMA(monthly_data, order=(5,1,0)) # Simple non-seasonal auto-regressive
        model_fit = model.fit()
        
        forecast = model_fit.forecast(steps=12)
        
        # Prepare JSON Structure
        history = []
        for d, v in monthly_data.tail(24).items():
            history.append({"date": d.strftime('%Y-%m'), "value": int(v), "type": "historical"})
            
        future = []
        # forecast index is usually offset
        last_date = monthly_data.index[-1]
        for val in forecast:
            last_date += timedelta(days=30)
            future.append({"date": last_date.strftime('%Y-%m'), "value": int(val), "type": "forecast"})
            
        payload = {
            "title": "Biometric Update Surge Forecast",
            "model": "ARIMA(5,1,0)",
            "data": history + future
        }
        
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(payload, f, indent=4)
        
        print(f"   ✅ Saved Forecast JSON.")

    except Exception as e:
        print(f"❌ ARIMA Error: {e}")
        # Fallback for dashboard (Empty/Mock structure if model fails?)
        # No, better to fail loud or output empty.

if __name__ == "__main__":
    run_time_machine()
