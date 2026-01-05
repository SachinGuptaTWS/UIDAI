"""
Engine 2: The "Route Optimizer" (Geospatial Machine Learning)
Model: Weighted K-Means Clustering.
Input: Aggregated Pincode Data.
Logic: Clusters Pincodes, weighted by the number of missing updates.
"""

import pandas as pd
import json
import os
import sys
from sklearn.cluster import KMeans
import numpy as np

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
OUTPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\outputs\route_clusters.json"

def run_route_optimizer():
    print("🚀 [Engine 2] Starting 'Route Optimizer' (Weighted K-Means)...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: processed data not found.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    
    # Filter for Critical Zones only? 
    # Or cluster everyone but prioritize Critical?
    # Let's focus on Critical + Warning to find "Hotspots"
    risk_df = df[df['Risk_Category'].isin(['CRITICAL', 'WARNING'])].copy()
    
    # Calculate Weight: Number of people lagging
    # Lag_Count ~ Enrolment * ULI (approx) or Enrolment - Update
    # Let's use exact difference from previous step if available, or recompute
    risk_df['Missing_Updates'] = risk_df['Enrolment_Count'] - risk_df['Update_Count']
    risk_df['Weight'] = risk_df['Missing_Updates'].clip(lower=1) # Min weight 1
    
    # Check if enough data
    if len(risk_df) < 5:
        print("   ⚠️ Not enough risk points. Using raw df.")
        risk_df = df.copy()
        risk_df['Weight'] = 1

    coord = risk_df[['Latitude', 'Longitude']].values
    weights = risk_df['Weight'].values
    
    # Number of Vans
    # Heuristic: 1 Van per 10,000 missing updates? Or fixed 10 vans for District?
    total_lag = weights.sum()
    n_clusters = max(3, min(20, int(total_lag / 5000))) 
    
    print(f"   🚚 Clustering {len(risk_df)} Pincodes (Total Lag: {int(total_lag)}) into {n_clusters} Routes...")
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    # Weighted K-Means!
    kmeans.fit(coord, sample_weight=weights)
    
    centers = kmeans.cluster_centers_
    # Labels for each pincode
    risk_df['Cluster'] = kmeans.predict(coord)
    
    # Aggregate stats per cluster
    clusters_output = []
    
    for i in range(n_clusters):
        cluster_grp = risk_df[risk_df['Cluster'] == i]
        total_demand = cluster_grp['Weight'].sum()
        
        clusters_output.append({
            "cluster_id": int(i + 101), # ID 101, 102...
            "lat": float(centers[i][0]),
            "lng": float(centers[i][1]),
            "demand_size": int(total_demand),
            "status": "CRITICAL" if total_demand > 10000 else "HIGH"
        })
        
    full_payload = {
        "algorithm": "Weighted K-Means",
        "timestamp": pd.Timestamp.now().isoformat(),
        "total_demand": int(total_lag),
        "deployed_vans": int(n_clusters),
        "routes": clusters_output
    }
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(full_payload, f, indent=4)
        
    print(f"   💾 Saved Route Clusters.")

if __name__ == "__main__":
    run_route_optimizer()
