
import re
import os

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Looking for template tag spacing issues...")

# Fix the specific longitude template issue: { { unit.longitude } }
old_patterns = [
    "{ { unit.longitude } }",
    "{  { unit.longitude }  }",
    "{ {unit.longitude} }",
]

for pattern in old_patterns:
    if pattern in content:
        print(f"Found: '{pattern}'")
        content = content.replace(pattern, "{{ unit.longitude }}")
        print(f"Replaced with: '{{{{ unit.longitude }}}}'")

# Also fix any other common spacing issues in template tags
content = re.sub(r'\{\s+\{', '{{', content)  # Fix { {  -> {{
content = re.sub(r'\}\s+\}', '}}', content)  # Fix } }  -> }}

# Fix ==  and != spacing issues
content = content.replace("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'")
content = content.replace("unit.status !='ON_SCENE'", "unit.status != 'ON_SCENE'")
content = content.replace("unit.status!='ON_SCENE'", "unit.status != 'ON_SCENE'")

print("\nWriting changes...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated successfully.")
