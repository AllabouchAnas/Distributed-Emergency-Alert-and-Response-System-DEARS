import sys
import os
import runpy

if __name__ == "__main__":
    # Add project root to sys.path so we can import 'app'
    # path: .../app/servers/response_services/police_service/run.py
    # root: .../ (4 levels up)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../../.."))
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Change working directory to project root so relative paths (like sqlite db) work consistently
    os.chdir(project_root)

    print(f"Starting Police Service (Project Root: {project_root})...")
    
    # Run the main module
    try:
        runpy.run_module("app.servers.response_services.police_service.main", run_name="__main__", alter_sys=True)
    except KeyboardInterrupt:
        pass
