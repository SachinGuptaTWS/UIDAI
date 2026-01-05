"""
VISUAL 5: Vicious Cycle Flowchart Generator
Visualizes the problem: Age 5 -> Bio Change -> Auth Fail -> Exclusion.
Output: HTML Flowchart (Gov Standard).
"""

import os

# CONFIG
OUTPUT_DIR = r"C:\Users\SachinGupta\Downloads\SatatAadhar\data\visuals"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: 'Arial', sans-serif; background: white; padding: 40px; display: flex; justify-content: center; }
  .flow-container { display: flex; flex-direction: column; align-items: center; gap: 20px; }
  
  .box {
    background: #fff;
    border: 2px solid #003366;
    color: #003366;
    padding: 20px;
    width: 220px;
    text-align: center;
    font-weight: bold;
    border-radius: 4px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    position: relative;
  }
  
  .box.danger {
    background: #FFEBEE;
    border-color: #D32F2F;
    color: #D32F2F;
  }
  
  .arrow {
    font-size: 24px;
    color: #555;
    font-weight: bold;
  }
  
  h2 { text-align: center; color: #333; margin-bottom: 30px; text-transform: uppercase; border-bottom: 2px solid #F39C12; display: inline-block; padding-bottom: 5px; }
</style>
</head>
<body>

<div>
    <h2>The Vicious Cycle of Silent Exclusion</h2>

    <div class="flow-container">
        <div class="box">Child Turns 5 / 15<br><small>(Mandatory Update Age)</small></div>
        
        <div class="arrow">↓</div>
        
        <div class="box">Biometrics Change<br><small>(Natural Growth)</small></div>
        
        <div class="arrow">↓</div>
        
        <div class="box danger">Authentication Fails<br><small>(Mismatch in Database)</small></div>
        
        <div class="arrow">↓</div>
        
        <div class="box danger">Service Denial<br><small>(Scholarship/Admission Rejected)</small></div>
        
        <div class="arrow">↓</div>
        
        <div class="box danger" style="background:#D32F2F; color:white;">School Dropout &<br>Identity Crisis</div>
    </div>
</div>

</body>
</html>
"""

def generate_cycle():
    print("🚀 Generating Vicious Cycle Flowchart...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    out_path = os.path.join(OUTPUT_DIR, 'fig5_vicious_cycle.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE)
        
    print(f"   ✅ Saved Vicious Cycle to: {out_path}")

if __name__ == "__main__":
    generate_cycle()
