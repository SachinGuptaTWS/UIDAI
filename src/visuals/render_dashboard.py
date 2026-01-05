"""
VISUAL 4: Dynamic Dashboard Renderer
Stitches REAL Data into the HTML Template.
Consumes Aggregated Pincode Data.
"""

import pandas as pd
import json
import os
import sys
from datetime import datetime

# CONFIG
DATA_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\processed\master_table.csv"
CLUSTERS_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\outputs\route_clusters.json"
TEMPLATE_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\src\visuals\dashboard_template.html"
OUTPUT_FILE = r"C:\Users\SachinGupta\Downloads\SatatAadhar\src\visuals\dashboard_index.html"

def render_dashboard():
    print("🚀 Rendering Dynamic Dashboard (Real Data Injection)...")

    if not os.path.exists(DATA_FILE) or not os.path.exists(CLUSTERS_FILE):
        print(f"❌ Error: Data missing. Run pipeline first.")
        sys.exit(1)

    # 1. Load Real Data
    df = pd.read_csv(DATA_FILE)
    with open(CLUSTERS_FILE, 'r') as f:
        cluster_data = json.load(f)

    # 2. Calculate Real Metrics (Population Level)
    # Gap = Enrolment - Update
    df['Gap'] = (df['Enrolment_Count'] - df['Update_Count']).clip(lower=0)
    
    total_pending = int(df['Gap'].sum())
    
    # Critical Count = Gap in Pincodes marked as CRITICAL
    critical_df = df[df['Risk_Category'] == 'CRITICAL']
    critical_count = int(critical_df['Gap'].sum())
    
    # Inclusion Score
    # Weighted by Pincode Population? 
    # Let's derive it from % Update Compliance
    # Compliance = Total Updates / Total Enrolment
    total_enrol = df['Enrolment_Count'].sum()
    if total_enrol > 0:
        compliance_rate = df['Update_Count'].sum() / total_enrol
        inclusion_score = int(compliance_rate * 100)
    else:
        inclusion_score = 0
        
    score_color = "metric-red" if inclusion_score < 70 else "metric-green"

    active_vans = cluster_data.get('deployed_vans', 0)
    
    # 3. Generate Cluster Table Rows
    routes = cluster_data.get('routes', [])
    sorted_routes = sorted(routes, key=lambda x: x['demand_size'], reverse=True)[:3]
    
    table_html = ""
    for r in sorted_routes:
        table_html += f"""
        <tr>
            <td>C-{r['cluster_id']}</td>
            <td>{r['demand_size']} Families</td>
            <td style="color:#D32F2F; font-weight:bold;">PENDING</td>
        </tr>
        """

    # 4. Inject into Template (Using Regex for robustness against newlines/spaces)
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as t:
        html_content = t.read()

    import re
    html_content = re.sub(r'\{\{\s*timestamp\s*\}\}', datetime.now().strftime('%Y-%m-%d %H:%M'), html_content)
    html_content = re.sub(r'\{\{\s*inclusion_score\s*\}\}', str(inclusion_score), html_content)
    html_content = re.sub(r'\{\{\s*score_color_class\s*\}\}', score_color, html_content)
    html_content = re.sub(r'\{\{\s*total_pending\s*\}\}', f"{total_pending:,}", html_content)
    html_content = re.sub(r'\{\{\s*critical_count\s*\}\}', f"{critical_count:,}", html_content)
    html_content = re.sub(r'\{\{\s*active_vans\s*\}\}', str(active_vans), html_content)
    html_content = re.sub(r'\{\{\s*cluster_rows\s*\}\}', table_html, html_content)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"   ✅ Dashboard Rendered to: {OUTPUT_FILE}")

if __name__ == "__main__":
    render_dashboard()
