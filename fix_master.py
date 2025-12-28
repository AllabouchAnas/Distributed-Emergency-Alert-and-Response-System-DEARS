
import os

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

print("=== MASTER FIX SCRIPT ===\n")

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

fixes = []

# 1. Fix comparison operators
if "unit.status=='ON_SCENE'" in content:
    content = content.replace("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'")
    fixes.append("Fixed unit.status=='ON_SCENE'")

if "unit.status !='ON_SCENE'" in content:
    content = content.replace("unit.status !='ON_SCENE'", "unit.status != 'ON_SCENE'")
    fixes.append("Fixed unit.status !='ON_SCENE'")

# 2. Fix template tag spacing
if "active_alert .longitude" in content:
    content = content.replace("active_alert .longitude", "active_alert.longitude")
    fixes.append("Fixed active_alert .longitude")

# 3. Fix corrupted JavaScript
if "uer.bindPopup" in content:
    content = content.replace("uer.bindPopup", "unitMarker.bindPopup")
    fixes.append("Fixed uer.bindPopup -> unitMarker.bindPopup")

# 4. Fix missing closing brace for try block
# Pattern: } catch (error) -> } } catch (error) 
# verifying context to ensure we don't double fix
if "} catch (error)" in content and "} } catch (error)" not in content:
    # We need to be careful. The current state is:
    #         } else {
    #             map.setView([0, 0], 2); // Default fallback
    #         }
    #     } catch (error) {
    
    # We want:
    #         } else {
    #             map.setView([0, 0], 2); // Default fallback
    #         }
    #     } <--- Close 'if (bounds.length > 0)'
    # } <--- Close 'try' block
    # catch (error) {
    
    # Let's target the catch line specifically
    content = content.replace("} catch (error) {", "} } catch (error) {")
    fixes.append("Fixed missing closing brace before catch")

# Apply changes
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Applied {len(fixes)} fixes:")
for fix in fixes:
    print(f" - {fix}")

print("\n=== DONE ===")
