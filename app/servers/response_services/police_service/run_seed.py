import sys
import os
import runpy

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../../.."))
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    os.chdir(project_root)
    print(f"Seeding DB from: {os.getcwd()}")
    
    runpy.run_module("app.servers.response_services.police_service.seed_data", run_name="__main__", alter_sys=True)
