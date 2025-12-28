
import os

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the specific error: active_alert .longitude
new_content = content.replace("active_alert .longitude", "active_alert.longitude")

# Also check for active_alert .latitude just in case
new_content = new_content.replace("active_alert .latitude", "active_alert.latitude")

if content != new_content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed space in template tags.")
else:
    print("No 'active_alert .longitude' found.")
