import sys
import os
import runpy

if __name__ == "__main__":
    # Change to project root so we share the same CWD (and thus same SQLite DB path)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../../.."))
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    os.chdir(project_root)

    print(f"Starting Medical Service (Project Root: {project_root})...")
    
    # Run the main module
    try:
        runpy.run_module("app.servers.response_services.medical_service.main", run_name="__main__", alter_sys=True)
    except KeyboardInterrupt:
        pass
