import re

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

print("=== COMPREHENSIVE TEMPLATE FIX ===\n")

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

fixes_applied = []

# Fix 1: Template tag spacing for comparison operators
patterns_to_fix = [
    ("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'"),
    ("unit.status !='ON_SCENE'", "unit.status != 'ON_SCENE'"),
    ("unit.status!='ON_SCENE'", "unit.status != 'ON_SCENE'"),
]

for old, new in patterns_to_fix:
    if old in content:
        content = content.replace(old, new)
        fixes_applied.append(f"Fixed: {old} -> {new}")

# Fix 2: Unit longitude template tag spacing
template_tag_fixes = [
    ("{ { unit.longitude } }", "{{ unit.longitude }}"),
    ("{  {unit.longitude}  }", "{{ unit.longitude }}"),
    ("{ {unit.longitude} }", "{{ unit.longitude }}"),
]

for old, new in template_tag_fixes:
    if old in content:
        content = content.replace(old, new)
        fixes_applied.append(f"Fixed longitude tag: {old} -> {new}")

# Fix 3: Corrupted JavaScript - unrkeopup should be unitMarker.bindPopup
if "unrkeopup" in content:
    content = content.replace("unrkeopup", "unitMarker.bindPopup")
    fixes_applied.append("Fixed corrupted JavaScript: unrkeopup -> unitMarker.bindPopup")

# Fix 4: General template tag spacing (regex)
content = re.sub(r'\{\s+\{', '{{', content)
content = re.sub(r'\}\s+\}', '}}', content)

print(f"Fixes applied: {len(fixes_applied)}")
for fix in fixes_applied:
    print(f"  - {fix}")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify key issues are fixed
print("\n=== VERIFICATION ===")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []
if "unit.status=='ON_SCENE'" in content:
    errors.append("Still has: unit.status=='ON_SCENE'")
if "unit.status !='ON_SCENE'" in content:
    errors.append("Still has: unit.status !='ON_SCENE'")
if "{ { unit.longitude" in content:
    errors.append("Still has spaced template tags")
if "unrkeopup" in content:
    errors.append("Still has corrupted JavaScript")

if errors:
    print("ERRORS REMAINING:")
    for err in errors:
        print(f"  ✗ {err}")
else:
    print("✓ All fixes verified successfully!")

print("\n=== DONE ===")
