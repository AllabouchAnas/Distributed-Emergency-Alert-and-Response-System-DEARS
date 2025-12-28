file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []
if "unit.status=='ON_SCENE'" in content:
    errors.append("unit.status=='ON_SCENE'")
if "unit.status !='ON_SCENE'" in content:
    errors.append("unit.status !='ON_SCENE'")
if "{ { unit.longitude" in content:
    errors.append("spaced template tag")
if "unrkeopup" in content:
    errors.append("corrupted JavaScript")

print(f"Errors found: {len(errors)}")
if errors:
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL FIXED!")
