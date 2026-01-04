"""
Engine 1: The "Time Machine" (Forecasting Engine)
Goal: Predict the "Surge" in workload for the next 6-12 months.
Model: ARIMA (Auto-Regressive Integrated Moving Average)
"""

import pandas as pd
import json
import os
import sys
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
OUTPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\outputs\forecast_data.json"

def run_time_machine():
    print("🚀 [Engine 1] Starting 'Time Machine' Forecast...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: processed data not found. Run pipeline first.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    
    # 1. Resample Data
    # We need a time series: Count of updates per month.
    # We rely on 'Last_Update_Date' to see historical trends of WHEN people updated.
    df['Last_Update_Date'] = pd.to_datetime(df['Last_Update_Date'])
    
    # Drop NaT
    ts_df = df.dropna(subset=['Last_Update_Date'])
    
    # Group by Month
    # Set index
    ts_df.set_index('Last_Update_Date', inplace=True)
    monthly_counts = ts_df.resample('M').size()
    
    print(f"   📈 Historical Data points: {len(monthly_counts)}")
    
    if len(monthly_counts) < 12:
        print("   ⚠️ Not enough data for robust ARIMA. Need > 12 months. Will attempt anyway.")

    # 2. Train ARIMA
    # Order (p,d,q) - (5,1,0) is a standard starting point for seasonality-ish data
    try:
        model = ARIMA(monthly_counts, order=(5,1,0))
        model_fit = model.fit()
        print("   ✅ ARIMA Model Trained.")
        
        # 3. Forecast
        # Predict next 12 months
        forecast_result = model_fit.forecast(steps=12)
        
        # Format for Dashboard (JSON)
        # Structure: [{date: '2026-01', value: 1200}, ...]
        
        history_data = []
        for date, value in monthly_counts.tail(24).items(): # Last 2 years matches
            history_data.append({
                "date": date.strftime('%Y-%m'),
                "value": int(value),
                "type": "historical"
            })
            
        forecast_data_list = []
        # forecast_result is a Series, index needs handling
        # ARIMA forecast index usually continues from last date
        
        current_date = monthly_counts.index[-1]
        for val in forecast_result:
            current_date += timedelta(days=30) # Approx month add
            forecast_data_list.append({
                "date": current_date.strftime('%Y-%m'),
                "value": int(val),
                "type": "forecast"
            })
            
        full_payload = {
            "title": "Biometric Update Surge Forecast",
            "model": "ARIMA(5,1,0)",
            "data": history_data + forecast_data_list
        }
        
        # Ensure output dir
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(full_payload, f, indent=4)
            
        print(f"   💾 Saved Forecast JSON to: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ ARIMA Failure: {e}")

if __name__ == "__main__":
    run_time_machine()
