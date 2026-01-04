"""
VISUAL 3: Sankey Diagram Generator (The Attrition Funnel)
Visualizes the flow: Birth Enrolment -> Age 5 Update -> Age 15 Update.
Shows where the "Leakage" happens.
Style: Professional, Clean.
"""

import pandas as pd
import plotly.graph_objects as go
import os
import sys

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
OUTPUT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\visuals"

def generate_sankey():
    print("🚀 Generating Sankey Diagram (Attrition Funnel)...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: processed data not found.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    
    # LOGIC:
    # 1. Total Population (Source)
    # 2. Flow to "Completed Age 5 Update" vs "Missed Age 5"
    # 3. From "Completed Age 5", flow to "Completed Age 15" vs "Missed Age 15"
    
    # We need to approximate this logic from the snapshot data.
    # Logic:
    # - "Missed Age 5": Age > 7 AND Last_Update_Date < (DOB + 6 years)
    # - "Missed Age 15": Age > 17 AND Last_Update_Date < (DOB + 16 years)
    
    # For a snapshot, let's look at the cohorts > 18 to see their history.
    base_cohort = df[df['Current_Age'] >= 18]
    
    if len(base_cohort) == 0:
        print("   ⚠️ No Adult cohort (>18) found to trace full history. Using full dataset approximations.")
        base_cohort = df

    total = len(base_cohort)
    
    # Simulate counts based on "Update_Gap" logic
    # If gap > 10 years -> Likely missed intermediate updates
    
    # Simplifying for the Visual (Logic usually complex):
    # Step 1: Enrolled (100%)
    # Step 2: Updated in Childhood (Last_Update < 10 years ago)
    # Step 3: Updated in Teens (Last_Update < 5 years ago)
    
    # This is a heuristic for the visual.
    
    step1_count = total
    # Count who updated at least once after birth
    step2_count = len(base_cohort[base_cohort['Update_Gap_Days'] < (base_cohort['Current_Age']*365 - 365)]) # Updated at least once
    
    # Count who updated recently (last 5 years)
    step3_count = len(base_cohort[base_cohort['Update_Gap_Days'] < 1825])
    
    # Define Nodes
    # 0: Total Enrolled
    # 1: Completed Childhood Update
    # 2: Dropped Out (Childhood)
    # 3: Completed Teen Update
    # 4: Dropped Out (Teen)
    
    # Flows
    # 0 -> 1 (Success)
    # 0 -> 2 (Fail)
    # 1 -> 3 (Success)
    # 1 -> 4 (Fail)
    
    val_0_1 = step2_count
    val_0_2 = step1_count - step2_count
    
    val_1_3 = step3_count
    val_1_4 = step2_count - step3_count
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = ["Total Enrolled", "Completed Age 5 Update", "Dropout (No Update)", "Completed Age 15 Update", "Dropout (Teen)"],
          color = ["#003366", "#388E3C", "#D32F2F", "#388E3C", "#D32F2F"] # NIC Blue, Green, Red
        ),
        link = dict(
          source = [0, 0, 1, 1], 
          target = [1, 2, 3, 4],
          value = [val_0_1, val_0_2, val_1_3, val_1_4],
          color = ["#A5D6A7", "#FFCDD2", "#A5D6A7", "#FFCDD2"] # Light Green, Light Red
      ))])

    fig.update_layout(title_text="Attrition Funnel: The 'Silent Exclusion' Lifecycle", font_size=12)
    
    out_path = os.path.join(OUTPUT_DIR, 'fig3_sankey.html') # Plotly saves HTML best
    fig.write_html(out_path)
    # Also try static if possible (needs kaleidoscope), else HTML is fine for screenshot
    print(f"   ✅ Saved Sankey Diagram to: {out_path}")

if __name__ == "__main__":
    generate_sankey()
