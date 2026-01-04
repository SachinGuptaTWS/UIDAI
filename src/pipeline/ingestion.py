"""
Step 1: Ingestion & Merging (Engine 3: Ingestion Layer)
This script loads the raw 'Enrolment.csv' and 'Update.csv' provided by the user.
It performs a Left Join on 'Enrolment_ID' to create a raw master dataset.
"""

import pandas as pd
import os
import sys

# CONFIG
RAW_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\raw"
OUTPUT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed"
ENROLMENT_FILE = os.path.join(RAW_DIR, "Enrolment.csv")
UPDATE_FILE = os.path.join(RAW_DIR, "Update.csv")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_merged_data.csv")

def ingest_data():
    print("🚀 [Step 1] Starting Data Ingestion...")

    # Validation: Check if files exist
    if not os.path.exists(ENROLMENT_FILE) or not os.path.exists(UPDATE_FILE):
        print(f"❌ CRITICAL ERROR: Input files not found in {RAW_DIR}")
        print("Please ensure 'Enrolment.csv' and 'Update.csv' are present.")
        sys.exit(1)

    try:
        # Load Enrolment Data (The Base)
        # Using chunksize is safer for massive files, but for the join we might need full load
        # For this hackathon scope, we'll try loading fully, but with specified dtypes to save RAM.
        print(f"   Reading {ENROLMENT_FILE}...")
        df_enrol = pd.read_csv(ENROLMENT_FILE, dtype={'Enrolment_ID': str, 'Pincode': str})
        
        print(f"   Reading {UPDATE_FILE}...")
        df_update = pd.read_csv(UPDATE_FILE, dtype={'Enrolment_ID': str})

        # Perform Left Join
        # We want ALL enrolments, matched with their latest update info
        print("   Merging Datasets (Left Join on Enrolment_ID)...")
        # Assuming Update file might have multiple entries, we want the LATEST one?
        # The PRD implies a simple join, but let's be smart: sort by update date and keep last?
        # For now, let's assume 1-to-1 or just simple merge as per user instruction.
        
        master_df = pd.merge(df_enrol, df_update, on='Enrolment_ID', how='left', suffixes=('_Enrol', '_Update'))
        
        print(f"   ✅ Merge Complete. Total Rows: {len(master_df)}")
        
        # Save Raw Merged
        master_df.to_csv(OUTPUT_FILE, index=False)
        print(f"   💾 Saved merged file to: {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ingest_data()
