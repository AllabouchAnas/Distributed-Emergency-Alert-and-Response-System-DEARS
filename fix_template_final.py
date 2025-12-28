import os
import re

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

print("=== TEMPLATE SYNTAX FIX SCRIPT ===\n")

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Show current problems
print("BEFORE:")
matches = re.findall(r'unit\.status[!=]=.*ON_SCENE', content)
for i, match in enumerate(matches, 1):
    print(f"  {i}. {match}")

# Fix all variations
replacements = [
    ("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'"),
    ("unit.status !='ON_SCENE'", "unit.status != 'ON_SCENE'"),
    ("unit.status!='ON_SCENE'", "unit.status != 'ON_SCENE'"),
    ('unit.status=="ON_SCENE"', 'unit.status == "ON_SCENE"'),
    ('unit.status!="ON_SCENE"', 'unit.status != "ON_SCENE"'),
]

changes_made = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        changes_made += 1
        print(f"\nReplaced: {old} -> {new}")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("\nAFTER:")
matches = re.findall(r'unit\.status[!=]=.*ON_SCENE', content)
if matches:
    for i, match in enumerate(matches, 1):
        print(f"  {i}. {match}")
else:
    print("  ✓ All syntax errors fixed!")

print(f"\nTotal changes: {changes_made}")
print("\n=== DONE ===")
