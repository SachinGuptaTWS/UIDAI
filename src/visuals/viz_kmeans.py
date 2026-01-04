"""
VISUAL 4: Route Optimizer Map (Figure 2)
Plots the "Red Zone" families and the "Optimized Van Hubs".
Uses Matplotlib for a clean, scientific, government-report style.
"""

import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import sys

# CONFIG
DATA_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
CLUSTERS_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\outputs\route_clusters.json"
OUTPUT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\visuals"

def generate_kmeans_map():
    print("🚀 Generating Route Optimizer Map (Gov Style)...")

    if not os.path.exists(DATA_FILE) or not os.path.exists(CLUSTERS_FILE):
        print(f"❌ Error: Data or Clusters not found. Run pipeline + optimizer first.")
        sys.exit(1)

    df = pd.read_csv(DATA_FILE)
    with open(CLUSTERS_FILE, 'r') as f:
        cluster_data = json.load(f)

    # Extract Cluster Centers
    centers_x = [c['lat'] for c in cluster_data['routes']]
    centers_y = [c['lng'] for c in cluster_data['routes']]

    # Filter for Background Data (The "Scattered Demand")
    # Only plot High Risk for clarity
    red_zone = df[df['Risk_Category'] == 'CRITICAL']
    
    if len(red_zone) == 0:
        print("   ⚠️ No Critical Risk data found. Plotting all for demo.")
        red_zone = df

    plt.figure(figsize=(10, 8))
    
    # Plot Households (Small dots)
    plt.scatter(red_zone['Latitude'], red_zone['Longitude'], 
                c='#B0BEC5', s=10, alpha=0.5, label='High-Lag Households') # Gray-Blue dots
    
    # Plot Centers (Big Red X)
    plt.scatter(centers_x, centers_y, 
                c='#D32F2F', s=150, marker='X', edgecolors='white', linewidth=1.5,
                label='Optimized Van Deployment')
    
    plt.title('Geospatial Optimization: Demand Aggregation Clusters', fontsize=14, fontweight='bold')
    plt.xlabel('Latitude', fontsize=10)
    plt.ylabel('Longitude', fontsize=10)
    plt.legend(frameon=True, facecolor='white', framealpha=1)
    
    # Remove "Scientific" ticks? No, Keep lat/long ticks for technical rigor.
    plt.grid(True, linestyle=':', alpha=0.6)
    
    out_path = os.path.join(OUTPUT_DIR, 'fig4_route_map.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved Route Map to: {out_path}")

if __name__ == "__main__":
    generate_kmeans_map()
