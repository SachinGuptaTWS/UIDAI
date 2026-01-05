"""
Step 2: Risk Calculation & Geocoding (Aggregated Engine)
Reads 'master_pincode_risk.csv'.
Calculates ULI based on Exclusion Ratio (Enrolment vs Updates).
Geocodes Pincodes.
"""

import pandas as pd
import pgeocode
import os
import sys
import numpy as np

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_pincode_risk.csv"
OUTPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"

def zero_day_cleaner():
    print("🚀 [Step 2] Starting Risk Calculation (Aggregated)...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found. Run ingestion first.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE, dtype={'Pincode': str})
    
    # 1. Feature Engineering (The Risk Engine)
    # ULI = (Enrolled - Updated) / Enrolled
    # "What % of people in this pincode have NOT updated?"
    
    df['Enrolment_Count'] = df['Enrolment_Count'].fillna(0)
    df['Update_Count'] = df['Update_Count'].fillna(0)
    
    # Avoid div by zero
    df = df[df['Enrolment_Count'] > 0]
    
    df['Lag_Ratio'] = (df['Enrolment_Count'] - df['Update_Count']) / df['Enrolment_Count']
    # Cap between 0 and 1
    df['ULI'] = df['Lag_Ratio'].clip(0, 1)
    
    # Classification
    df['Risk_Category'] = np.where(df['ULI'] > 0.6, 'CRITICAL', 
                                   np.where(df['ULI'] > 0.3, 'WARNING', 'SAFE'))
    
    # 2. Geocoding (Bulk)
    print(f"   🌍 Geocoding {len(df)} Pincodes...")
    nomi = pgeocode.Nominatim('in')
    
    unique_pins = df['Pincode'].unique()
    geo_data = nomi.query_postal_code(unique_pins)
    
    pin_lat = dict(zip(unique_pins, geo_data.latitude))
    pin_lon = dict(zip(unique_pins, geo_data.longitude))
    pin_dist = dict(zip(unique_pins, geo_data.county_name)) # District
    
    df['Latitude'] = df['Pincode'].map(pin_lat)
    df['Longitude'] = df['Pincode'].map(pin_lon)
    df['District'] = df['Pincode'].map(pin_dist)
    
    # Drop where Geocoding failed (NaN)
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    
    print(f"   ✅ Processed {len(df)} valid geospatial points.")
    df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    zero_day_cleaner()
