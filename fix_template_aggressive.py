
import re
import os

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Initial content around line 143:")
start_idx = content.find("btn-on-scene")
if start_idx != -1:
    print(content[start_idx:start_idx+100])

# Regex to fix missing spaces around == and != in django tags
# Matches: {% if something==something %} -> {% if something == something %}
# We look for == or != that are NOT surrounded by spaces, inside {% ... %}
# This is hard to regex perfectly in one go, so we will be specific for the known error

# Fix unit.status=='ON_SCENE'
content = content.replace("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'")
content = content.replace('unit.status=="ON_SCENE"', 'unit.status == "ON_SCENE"')
content = content.replace("unit.status !='ON_SCENE'", "unit.status != 'ON_SCENE'")
content = content.replace("unit.status!='ON_SCENE'", "unit.status != 'ON_SCENE'")
content = content.replace('unit.status!="ON_SCENE"', 'unit.status != "ON_SCENE"')

# General fix for any checks
content = re.sub(r"==('|\")", r" == \1", content)
content = re.sub(r"!=('|\")", r" != \1", content)

# Fix double spaces we might have created
content = content.replace("  == ", " == ")
content = content.replace("  != ", " != ")

print("\nModified content around line 143:")
start_idx = content.find("btn-on-scene")
if start_idx != -1:
    print(content[start_idx:start_idx+100])

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFile updated successfully.")
