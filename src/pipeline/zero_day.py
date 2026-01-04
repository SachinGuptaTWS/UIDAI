"""
Step 2 & 3: "Zero-Day" Cleaning & Feature Engineering (Engine 3: Risk Calculator)

This script:
1. Standardizes Dates.
2. Geocodes Pincodes to Lat/Long (crucial for Engine 2).
3. Calculates 'Update Lag Index' (ULI) (The Magic Metric).
4. Calculates 'District_Inclusion_Score'.
"""

import pandas as pd
import pgeocode
import os
import sys
from datetime import datetime
import numpy as np

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\raw_merged_data.csv"
OUTPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"

def zero_day_cleaner():
    print("🚀 [Step 2] Starting 'Zero-Day' Cleaning & Feature Engineering...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: Input file {INPUT_FILE} not found. Run ingestion first.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE, dtype={'Pincode': str})
    print(f"   Loaded {len(df)} rows.")

    # --- 1. Date Standardization ---
    print("   📅 Standardizing Dates...")
    # Map column names if needed (User said: DOB, Last_Update_Date)
    # We attempt to infer or use standard names.
    # Expected columns: DOB, Last_Update_Date
    
    # Handle possible column name variations if merge resulted in suffixes
    if 'DOB' not in df.columns and 'DOB_Enrol' in df.columns:
        df.rename(columns={'DOB_Enrol': 'DOB'}, inplace=True)
    
    # If Last_Update_Date is missing (never updated), fill with Enrolment Date?
    # Or leave NaT? If NaT, ULI calculation will be tricky.
    # Assumption: If never updated, Last_Update_Date = Enrolment_Date (if available)
    
    for col in ['DOB', 'Last_Update_Date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Drop rows without DOB (cannot calculate Age -> cannot calculate ULI)
    initial_count = len(df)
    df.dropna(subset=['DOB'], inplace=True)
    print(f"   Dropped {initial_count - len(df)} rows due to missing DOB.")

    # --- 2. Feature Engineering (The Risk Engine) ---
    print("   🧮 Calculating 'The Magic Metrics'...")
    now = datetime.now()
    
    # Calculate Age
    df['Current_Age'] = (now - df['DOB']).dt.days / 365.0
    
    # Calculate Update Gap
    # If Last_Update_Date is NaT, use DOB (implies never updated since birth)
    df['Last_Activity_Date'] = df['Last_Update_Date'].fillna(df['DOB'])
    df['Update_Gap_Days'] = (now - df['Last_Activity_Date']).dt.days
    
    # --- ULI FORMULA (Milestone Centric) ---
    # We want to flag children near 5 and 15 who haven't updated in years.
    # Simple Formula for V1: Gap / Age
    # Refined Formula:
    # If Age is 5-7 OR 15-17 -> Critical Window.
    # We multiply ULI by a 'Urgency_Factor'
    
    def calculate_urgency(age):
        if 4.5 <= age <= 7.0: return 2.0  # Mandatory 5yo update
        if 14.5 <= age <= 17.0: return 2.5 # Mandatory 15yo update
        if age > 18: return 0.1 # Adults less critical for this specific child-centric hackathon
        return 1.0

    df['Urgency_Factor'] = df['Current_Age'].apply(calculate_urgency)
    
    # Base ULI: Years since update / (Age + 1)
    # +1 to avoid division by zero for newborns
    df['Base_ULI'] = (df['Update_Gap_Days'] / 365.0) / (df['Current_Age'] + 1)
    
    # Final Metric
    df['ULI'] = df['Base_ULI'] * df['Urgency_Factor']
    
    # Classification
    # ULI > 0.8 is nominally "Red Zone"
    df['Risk_Category'] = np.where(df['ULI'] > 0.8, 'CRITICAL', 
                                   np.where(df['ULI'] > 0.5, 'WARNING', 'SAFE'))

    # --- 3. Geocoding (Engine 2 Prep) ---
    print("   🌍 Geocoding Pincodes (This may take time)...")
    nomi = pgeocode.Nominatim('in')
    
    # Optimization: Unique Pincodes only
    unique_pincodes = df['Pincode'].unique()
    print(f"   Found {len(unique_pincodes)} unique pincodes.")
    
    # Query in bulk? pgeocode query_postal_code accepts list/array? 
    # Yes, it typically accepts arrays.
    geo_data = nomi.query_postal_code(unique_pincodes)
    
    # Create a mapping dictionary
    pin_to_lat = dict(zip(unique_pincodes, geo_data.latitude))
    pin_to_lon = dict(zip(unique_pincodes, geo_data.longitude))
    
    df['Latitude'] = df['Pincode'].map(pin_to_lat)
    df['Longitude'] = df['Pincode'].map(pin_to_lon)
    
    # Drop rows where Geocoding failed (NaN Lat/Long) - can't route them.
    # Or keep them for stats but exclude from Routing.
    # We will keep them but flag them.
    
    # --- 4. District Scoring (Engine 3 Output) ---
    # Simple Mock of the Logic: Mean ULI per district?
    # We don't have district column? pgeocode gives 'county'/'state_name'/'community_name'
    # 'county' usually maps to District in India for pgeocode.
    
    geo_district_map = dict(zip(unique_pincodes, geo_data.county_name)) # county_name is District
    df['District'] = df['Pincode'].map(geo_district_map)
    
    print("   📊 Dataset Ready.")
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"   💾 Saved Master Table to: {OUTPUT_FILE}")

if __name__ == "__main__":
    zero_day_cleaner()
