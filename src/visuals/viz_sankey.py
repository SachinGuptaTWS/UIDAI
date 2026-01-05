"""
VISUAL 3: Sankey Diagram Generator (The Attrition Funnel)
Visualizes Aggregated Flow: Total Enrolment -> Updated vs Gap.
"""

import pandas as pd
import plotly.graph_objects as go
import os
import sys

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
OUTPUT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\visuals"

def generate_sankey():
    print("🚀 Generating Sankey Diagram (Aggregated)...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: processed data not found.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    
    # Calculate Totals
    total_enrol = df['Enrolment_Count'].sum()
    total_updates = df['Update_Count'].sum()
    total_gap = (total_enrol - total_updates)
    if total_gap < 0: total_gap = 0 # Updates > Enrolment possible in edge cases?
    
    # Simple flow: Enrolled -> [Updated, Dropout]
    
    labels = ["Total Enrolments", "Biometric/Demo Updated", "Exclude/Gap"]
    colors = ["#003366", "#388E3C", "#D32F2F"]
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15, thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = labels,
          color = colors
        ),
        link = dict(
          source = [0, 0], 
          target = [1, 2],
          value = [total_updates, total_gap],
          color = ["#A5D6A7", "#FFCDD2"]
      ))])

    fig.update_layout(title_text="Attrition Funnel: Enrolment Compliance Gap", font_size=12)
    
    out_path = os.path.join(OUTPUT_DIR, 'fig3_sankey.html')
    fig.write_html(out_path)
    print(f"   ✅ Saved Sankey Diagram to: {out_path}")

if __name__ == "__main__":
    generate_sankey()
