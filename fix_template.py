import re

file_path = r'app\client\alerts\templates\responder_dashboard_minimal.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the syntax errors
content = content.replace("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'")
content = content.replace("unit.status !='ON_SCENE'", "unit.status != 'ON_SCENE'")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template syntax fixed successfully!")
