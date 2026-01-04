"""
VISUAL 4: Dynamic Dashboard Renderer
Stitches REAL Data into the HTML Template.
Ensures NO MOCK DATA exists in the final visual.
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

    # 2. Calculate Real Metrics
    total_pending = len(df[df['ULI'] > 0.0]) # Any update needed?
    # Or strict definition: ULI > 0.5
    critical_count = len(df[df['Risk_Category'] == 'CRITICAL'])
    
    # Inclusion Score = 100 - (Critical/Total * 100 * Weight)
    # Simple logic for now:
    # 100 - (Avg ULI * 50)?
    avg_uli = df['ULI'].mean()
    inclusion_score = max(0, min(100, int(100 - (avg_uli * 40))))
    
    score_color = "metric-red" if inclusion_score < 70 else "metric-green"

    active_vans = cluster_data.get('deployed_vans', 0)
    
    # 3. Generate Cluster Table Rows
    routes = cluster_data.get('routes', [])
    # Sort by demand size desc
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

    # 4. Inject into Template
    with open(TEMPLATE_FILE, 'r') as t:
        html_content = t.read()

    # Simple string replacement (No Jinja2 dependency needed for simplicity)
    html_content = html_content.replace('{{ timestamp }}', datetime.now().strftime('%Y-%m-%d %H:%M'))
    html_content = html_content.replace('{{ inclusion_score }}', str(inclusion_score))
    html_content = html_content.replace('{{ score_color_class }}', score_color)
    html_content = html_content.replace('{{ total_pending }}', f"{total_pending:,}")
    html_content = html_content.replace('{{ critical_count }}', f"{critical_count:,}")
    html_content = html_content.replace('{{ active_vans }}', str(active_vans))
    html_content = html_content.replace('{{ cluster_rows }}', table_html)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(html_content)

    print(f"   ✅ Dashboard Rendered to: {OUTPUT_FILE}")
    print("   Open this file in a browser to take the Final Screenshot.")

if __name__ == "__main__":
    render_dashboard()
