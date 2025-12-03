"""
Simple runner script for the Dispatcher Service
"""
import os
import sys
import uvicorn

# Change to project root so we share the same CWD (and thus same SQLite DB path) as police service
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
os.chdir(project_root)

# Add app/servers to sys.path so 'dispatcher_service' package can be found
servers_dir = os.path.join(project_root, "app", "servers")
sys.path.insert(0, servers_dir)

from dispatcher_service.config import DISPATCHER_HOST, DISPATCHER_PORT

if __name__ == "__main__":
    print(f"Starting Dispatcher Service (Project Root: {project_root})...")
    uvicorn.run(
        "dispatcher_service.main:app",
        host=DISPATCHER_HOST,
        port=DISPATCHER_PORT,
        reload=False
    )
