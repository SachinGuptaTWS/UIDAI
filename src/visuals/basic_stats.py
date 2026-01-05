"""
MANDATORY STATISTICAL ANALYSIS (Compliance Requirement)
Generates Univariate and Bivariate charts.
Input: Aggregated Pincode Data.
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
    print("🚀 Generating Stats (Aggregated)...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: processed data not found.")
        sys.exit(1)

    df = pd.read_csv(INPUT_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'sans-serif'
    
    # 1. UNIVARIATE: Distribution of Lag Index (ULI)
    # Answers: "How many pincodes are in Critcal Zone?"
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='ULI', bins=20, color='#003366', edgecolor='black')
    plt.title('Univariate Analysis: Distribution of Update Lag Index (ULI)', fontsize=14, fontweight='bold')
    plt.xlabel('ULI (0.0 = Perfect, 1.0 = High Exclusion)', fontsize=12)
    plt.ylabel('Frequency (Number of Pincodes)', fontsize=12)
    plt.axvline(x=0.6, color='red', linestyle='--', label='Critical Threshold (0.6)')
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig1_univariate_uli.png'), dpi=300, bbox_inches='tight')
    print("   ✅ Generated Fig 1 (ULI Hist)")

    # 2. BIVARIATE: Enrolment Density vs ULI
    # Answers: "Do big cities have more exclusion?"
    plt.figure(figsize=(10, 6))
    plot_df = df.sample(min(5000, len(df))) if len(df) > 5000 else df
    
    sns.scatterplot(data=plot_df, x='Enrolment_Count', y='ULI', hue='Risk_Category', 
                    palette={'CRITICAL': '#D32F2F', 'WARNING': '#FFA000', 'SAFE': '#388E3C'}, alpha=0.6)
    
    plt.title('Bivariate Analysis: Population Density vs. Exclusion Risk', fontsize=14, fontweight='bold')
    plt.xlabel('Enrolment Volume (Density)', fontsize=12)
    plt.ylabel('Update Lag Index (ULI)', fontsize=12)
    # Log scale if density varies wildy? 
    # plt.xscale('log') 
    plt.legend(title='Risk Category')
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig2_bivariate_density.png'), dpi=300, bbox_inches='tight')
    print("   ✅ Generated Fig 2 (Density vs Risk)")

if __name__ == "__main__":
    generate_stats()
