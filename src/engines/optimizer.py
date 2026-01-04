"""
Engine 2: The "Route Optimizer" (Geospatial Machine Learning)
Goal: Figure out exactly where to park the "Aadhaar on Wheels" vans.
Model: K-Means Clustering (Unsupervised Learning)
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
    print("🚀 [Engine 2] Starting 'Route Optimizer' (K-Means)...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: processed data not found.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    
    # 1. Filter: Isolate "High Risk" (Red Zone)
    # We only want to send vans to where ULI is high
    red_zone_df = df[df['Risk_Category'] == 'CRITICAL'].copy()
    
    # Needs Lat/Long
    red_zone_df = red_zone_df.dropna(subset=['Latitude', 'Longitude'])
    
    count = len(red_zone_df)
    print(f"   🎯 Found {count} High-Risk Households with Geocodes.")
    
    if count < 10:
        print("   ⚠️ Not enough data points for Clustering. Need at least 10.")
        return

    # 2. Vectorize
    X = red_zone_df[['Latitude', 'Longitude']].values
    
    # 3. Cluster
    # How many vans? Let's say 1 Van per 500 households? 
    # Or fixed number of clusters?
    # Logic: n_clusters = count / 100 (capped at 50, min 1)
    n_clusters = max(1, min(50, int(count / 100)))
    if n_clusters == 0: n_clusters = 1
    
    print(f"   🚚 Optimizing for {n_clusters} Service Clusters...")
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    # 4. Output Generation
    # We want a JSON that Mapbox/Leaflet can read.
    # List of Cluster Centers
    
    clusters_output = []
    
    for i, center in enumerate(centers):
        # Count points in this cluster
        size = np.sum(labels == i)
        
        clusters_output.append({
            "cluster_id": int(i),
            "lat": float(center[0]),
            "lng": float(center[1]),
            "demand_size": int(size),
            "status": "busiest" if size > 200 else "normal"
        })
        
    full_payload = {
        "algorithm": "K-Means Clustering",
        "timestamp": pd.Timestamp.now().isoformat(),
        "total_demand": int(count),
        "deployed_vans": int(n_clusters),
        "routes": clusters_output
    }
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(full_payload, f, indent=4)
        
    print(f"   💾 Saved Route Clusters to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_route_optimizer()
