
import os
import re

file_path = r"c:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client\alerts\templates\responder_dashboard_minimal.html"

print("=== FINAL ATOMIC FIX SCRIPT ===\n")

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. FIX TEMPLATE SYNTAX (Comparison Operators)
# Regex to find unspaced operators in template tags
# Matches: unit.status=='ON_SCENE' -> unit.status == 'ON_SCENE'
content = content.replace("unit.status=='ON_SCENE'", "unit.status == 'ON_SCENE'")
content = content.replace("unit.status !='ON_SCENE'", "unit.status != 'ON_SCENE'")
content = content.replace("unit.status!='ON_SCENE'", "unit.status != 'ON_SCENE'")

print("- Applied Template Operator Fixes")

# 2. FIX TEMPLATE TAG SPACING
# Matches: active_alert .longitude -> active_alert.longitude
content = content.replace("active_alert .longitude", "active_alert.longitude")
content = content.replace("active_alert .latitude", "active_alert.latitude")
content = content.replace("{ {", "{{") # General fix for double braces
content = content.replace("} }", "}}") 

print("- Applied Template Tag Spacing Fixes")

# 3. FIX JAVASCRIPT CORRUPTION & LOGIC
# Ensure unitMarker.bindPopup is correct
if "uer.bindPopup" in content:
    content = content.replace("uer.bindPopup", "unitMarker.bindPopup")
    print("- Fixed corrupted JS variable 'uer'")

# 4. FIX MAP ZOOM LOGIC & TRY-CATCH STRUCTURE
# We will identify the specific block and REWRITE it completely to be safe.
# This avoids context matching errors.

script_start_marker = "if (bounds.length > 0) {"
script_end_marker = "});"

# We look for the block inside the script tag
if script_start_marker in content:
    # We'll rely on a known unique string to target replacement if possible, 
    # but regex is safer for the logic block replacement.
    
    # Target: The bounds logic block
    # We want to replace the logic that handles fitBounds and closes the try/catch
    
    # Old/Broken patterns might vary, so let's construct the DESIRED block
    desired_logic_block = """        if (bounds.length > 0) {
            map.fitBounds(bounds, { padding: [50, 50] });
            if (bounds.length === 1) {
                map.setZoom(15);
            }
        } else {
            map.setView([0, 0], 2); // Default fallback
        }
    } catch (error) {
        console.error('Map initialization error:', error);
    }"""
    
    # We need to find where the bounds logic starts and replace until the end of the try/catch
    # This is tricky with regex if the file state varies. 
    # Let's use a simpler marker replacement if we can identify the specific broken block.
    
    # REPLACEMENT STRATEGY:
    # Find the chunk starting from "map.fitBounds" until the end of the catch block.
    
    pattern = r"map\.fitBounds\(bounds, \{ padding: \[50, 50\] \}\);[\s\S]*?catch \(error\) \{[\s\S]*?\}"
    
    # Check if we find it
    match = re.search(pattern, content)
    if match:
         replacement = """map.fitBounds(bounds, { padding: [50, 50] });
            if (bounds.length === 1) {
                map.setZoom(15);
            }
        } else {
            map.setView([0, 0], 2); // Default fallback
        }
    } catch (error) {
        console.error('Map initialization error:', error);
    }"""
         # We need to match the indentation of the file roughly, 
         # but HTML/JS is forgiving on indentation.
         # However, we need to be careful about the braces proceeding it.
         # The 'match' includes the closing braces.
         
         # The matched text is likely:
         # map.fitBounds(...) 
         # ...
         # } catch(error) { ... }
         
         # Note: Our desired block assumes the 'if (bounds.length > 0) {' IS ALREADY THERE.
         # So we only replace the BODY of that if and the subsequent closure.
         
         content = re.sub(pattern, replacement, content)
         print("- Rewrote Map Zoom Logic & Try/Catch Block")
    else:
        print("! WARNING: Could not find map logic block to replace via Regex. Checking for specific broken strings...")
        # Fallback: Fix specific syntax errors if regex failed (e.g. extra braces)
        content = content.replace("} } catch (error)", "} catch (error)")
        content = content.replace("} } } catch (error)", "} catch (error)")


# 5. ATOMIC WRITE
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== VERIFICATION ===")
# Quick verify
if "unit.status=='ON_SCENE'" in content:
    print("FATAL: Template Syntax Error fixed but still present in memory?")
else:
    print("✓ Template Syntax (==) Looks Good")

if "active_alert .longitude" in content:
    print("FATAL: Template Tag Spacing ( .longitude) still present")
else:
    print("✓ Template Tag Spacing Looks Good")

print("\nScript Completed.")
