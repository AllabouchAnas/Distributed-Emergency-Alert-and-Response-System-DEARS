
import os
import re

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix == missing spaces
    new_content = re.sub(r"(unit\.status)==('ON_SCENE')", r"\1 == \2", content)
    
    # Fix != missing spaces
    new_content = re.sub(r"(unit\.status)!=(['\"]ON_SCENE['\"])", r"\1 != \2", new_content)
    
    # Also handle the !='ON_SCENE' case specifically if the quote is different or general
    new_content = new_content.replace("unit.status!='ON_SCENE'", "unit.status != 'ON_SCENE'")
    new_content = new_content.replace("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'")

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully fixed template syntax errors.")
    else:
        print("No changes needed or patterns not found.")

except Exception as e:
    print(f"Error: {e}")
