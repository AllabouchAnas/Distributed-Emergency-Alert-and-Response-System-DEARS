import rpyc
import time
import sys

def verify_service():
    try:
        print("Connecting to Police Service...")
        conn = rpyc.connect("localhost", 9005)
        print("Connected!")
        
        # Test data
        alert_id = 1
        description = "Test Emergency"
        location = "40.7128,-74.0060" # NYC
        emergency_type = "POLICE"
        
        print(f"Sending alert: {description} at {location}")
        response = conn.root.receive_alert(alert_id, description, location, emergency_type)
        
        print(f"Response: {response}")
        conn.close()
        
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    verify_service()
