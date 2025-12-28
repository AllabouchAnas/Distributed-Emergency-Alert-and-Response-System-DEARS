"""
Debug script to check if the alert has coordinates
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, r'C:\Users\amine\OneDrive\Desktop\ProjetBi\Distributed-Emergency-Alert-and-Response-System-DEARS\app\client')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_response.settings')
django.setup()

from alerts.models import Alert, ResponseUnit, AlertStatus

print("=== CHECKING ALERT AND UNIT COORDINATES ===\n")

# Get active alerts (ASSIGNED or IN_PROGRESS)
active_alerts = Alert.objects.filter(status__in=[AlertStatus.ASSIGNED, AlertStatus.IN_PROGRESS])

print(f"Found {active_alerts.count()} active alert(s)\n")

for alert in active_alerts:
    print(f"Alert ID: {alert.alert_id}")
    print(f"  UUID: {alert.alert_uuid}")
    print(f"  Type: {alert.get_emergency_type_display()}")
    print(f"  Location: {alert.location}")
    print(f"  Latitude: {alert.latitude}")
    print(f"  Longitude: {alert.longitude}")
    print(f"  Has coordinates: {bool(alert.latitude and alert.longitude)}")
    
    if alert.assigned_unit:
        print(f"\n  Assigned Unit: {alert.assigned_unit.unit_name}")
        print(f"    Unit Location: {alert.assigned_unit.current_location}")
        print(f"    Unit Latitude: {alert.assigned_unit.latitude}")
        print(f"    Unit Longitude: {alert.assigned_unit.longitude}")
        print(f"    Unit has coordinates: {bool(alert.assigned_unit.latitude and alert.assigned_unit.longitude)}")
    print()

# Also check all response units
print("\n=== ALL RESPONSE UNITS ===\n")
units = ResponseUnit.objects.all()
for unit in units:
    print(f"Unit: {unit.unit_name} ({unit.get_unit_type_display()})")
    print(f"  Lat/Lng: {unit.latitude}, {unit.longitude}")
    print(f"  Has coords: {bool(unit.latitude and unit.longitude)}")
    print()
