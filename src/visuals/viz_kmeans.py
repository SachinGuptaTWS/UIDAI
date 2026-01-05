"""
VISUAL 4: Geospatial Route Optimization Map
Model: Plotly/Matplotlib Overlay.
Visual: High-Risk Pincodes (Red Bubbles) + Optimized Van Stops (Black Xs).
Size of Bubble = Enrolment Density.
"""

import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import sys

# CONFIG
DATA_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
CLUSTERS_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\outputs\route_clusters.json"
OUTPUT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\visuals"

def generate_map():
    print("🚀 Generating Route Map (Aggregated)...")

    if not os.path.exists(DATA_FILE) or not os.path.exists(CLUSTERS_FILE):
        print(f"❌ Error: processed data not found.")
        return # Soft fail

    df = pd.read_csv(DATA_FILE)
    with open(CLUSTERS_FILE, 'r') as f:
        cluster_data = json.load(f)
        
    routes = cluster_data['routes']
    
    plt.figure(figsize=(10, 8))
    
    # 1. Plot Background (All Pincodes)
    # Scale bubble size
    s = df['Enrolment_Count'] / df['Enrolment_Count'].max() * 100
    
    plt.scatter(df['Longitude'], df['Latitude'], 
                c='#90A4AE', alpha=0.3, s=s, label='Safe Zones')
                
    # 2. Plot Critical Zones (Red)
    crit = df[df['Risk_Category'] == 'CRITICAL']
    if not crit.empty:
        s_crit = crit['Enrolment_Count'] / df['Enrolment_Count'].max() * 100
        plt.scatter(crit['Longitude'], crit['Latitude'], 
                    c='#D32F2F', alpha=0.7, s=s_crit, label='Critical Hotspots')
    
    # 3. Plot Optimized Routes (X)
    rx = [r['lng'] for r in routes]
    ry = [r['lat'] for r in routes]
    plt.scatter(rx, ry, marker='X', s=200, c='black', label='Mobile Van Stop')
    
    # Annotate Route IDs
    for r in routes:
        plt.annotate(f"C-{r['cluster_id']}", (r['lng'], r['lat']), 
                     xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')

    plt.title(f"AI-Optimized Mobile Aadhaar Routes ({len(routes)} Vans Deployed)", fontsize=14)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    out_path = os.path.join(OUTPUT_DIR, 'fig4_route_map.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved Route Map to: {out_path}")

if __name__ == "__main__":
    generate_map()
