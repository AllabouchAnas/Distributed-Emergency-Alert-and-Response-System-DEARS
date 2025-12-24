import subprocess
import sys
import time
import os

def is_wsl():
    try:
        with open('/proc/version', 'r') as f:
            if 'microsoft' in f.read().lower():
                return True
    except FileNotFoundError:
        pass
    return False

def main():
    # Base directory where this script is located (app/servers)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List of service scripts to run
    # Paths are relative to base_dir
    services = [
        os.path.join(base_dir, "dispatcher_service", "run.py"),
        os.path.join(base_dir, "response_services", "fire_service", "run.py"),
        os.path.join(base_dir, "response_services", "medical_service", "run.py"),
        os.path.join(base_dir, "response_services", "police_service", "run.py"),
    ]

    processes = []
    
    wsl_mode = is_wsl()
    win_mode = sys.platform == 'win32'

    print(f"Starting {len(services)} services...")
    if wsl_mode:
        print("WSL detected. Spawning separate windows via cmd.exe...")

    try:
        for script in services:
            script_path = os.path.abspath(script)
            if not os.path.exists(script_path):
                print(f"Error: Script not found: {script_path}")
                continue

            print(f"Launching {script}...")
            
            if win_mode:
                # Windows: Use CREATE_NEW_CONSOLE
                p = subprocess.Popen(
                    [sys.executable, script_path],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                processes.append(p)
            elif wsl_mode:
                # WSL: Use cmd.exe start wsl.exe to open new window
                # We use sys.executable to ensure we use the same venv python
                # Note: This assumes 'cmd.exe' is in the PATH (standard for WSL)
                cmd = ['cmd.exe', '/c', 'start', 'wsl.exe', '-e', sys.executable, script_path]
                subprocess.Popen(cmd)
            else:
                # Standard Linux/Mac: Run in background in same console
                p = subprocess.Popen([sys.executable, script_path])
                processes.append(p)

            # Small delay to ensure they don't fight for resources immediately
            time.sleep(2) 

        print("All services launched.")
        print("Press Ctrl+C to stop all services (only works for same-console processes).")
        
        # Keep the main script running to monitor or wait for interrupt
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping services...")
        for p in processes:
            try:
                p.terminate()
            except Exception as e:
                print(f"Error stopping process: {e}")

if __name__ == "__main__":
    main()
