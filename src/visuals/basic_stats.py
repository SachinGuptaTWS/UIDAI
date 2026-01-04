"""
MANDATORY STATISTICAL ANALYSIS (Compliance Requirement)
Generates Univariate and Bivariate charts for the PDF.
Style: Academic, Clean, White Background (No flashy themes).
Data: STRICTLY Real Data from 'master_table.csv'.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# CONFIG
INPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
OUTPUT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\visuals"

def generate_stats():
    print("🚀 Generating Mandatory Statistical Analysis (Academic Style)...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: processed data not found in {INPUT_FILE}.")
        print("   Cannot generate stats without REAL data.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Set Style: Government/Academic (White grid, dark text)
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    
    # 1. UNIVARIATE: Age Distribution (Histogram)
    # Proof of "Age 5/15" peaks or gaps
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Current_Age', bins=20, color='#003366', edgecolor='black') # NIC Blue
    plt.title('Univariate Analysis: Beneficiary Age Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Age (Years)', fontsize=12)
    plt.ylabel('Frequency (Count)', fontsize=12)
    plt.axvline(x=5, color='red', linestyle='--', label='Mandatory Update (Age 5)')
    plt.axvline(x=15, color='red', linestyle='--', label='Mandatory Update (Age 15)')
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig1_univariate_age.png'), dpi=300, bbox_inches='tight')
    print("   ✅ Generated Fig 1: Age Distribution")

    # 2. BIVARIATE: Age vs Update Lag (Scatter Plot)
    # Proof of "The Silent Exclusion" (High lag in teen years)
    plt.figure(figsize=(10, 6))
    # Sample down if too large for clean scatter
    plot_df = df.sample(n=min(5000, len(df)), random_state=42) if len(df) > 5000 else df
    
    sns.scatterplot(data=plot_df, x='Current_Age', y='Update_Gap_Days', hue='Risk_Category', 
                    palette={'CRITICAL': '#D32F2F', 'WARNING': '#FFA000', 'SAFE': '#388E3C'}, alpha=0.6)
    
    plt.title('Bivariate Analysis: Age vs. Update Lag', fontsize=14, fontweight='bold')
    plt.xlabel('Current Age (Years)', fontsize=12)
    plt.ylabel('Days Since Last Update', fontsize=12)
    plt.axhline(y=1825, color='gray', linestyle=':', label='5 Year Gap') # 5 years
    plt.legend(title='Risk Status')
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig2_bivariate_lag.png'), dpi=300, bbox_inches='tight')
    print("   ✅ Generated Fig 2: Age vs Lag Scatter")

    print(f"   💾 Saved charts to: {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_stats()
