"""
Simple runner script for the Dispatcher Service
"""
import os
import sys
import uvicorn

# Change to parent directory so dispatcher_service can be imported as a package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(parent_dir)
sys.path.insert(0, parent_dir)

from dispatcher_service.config import DISPATCHER_HOST, DISPATCHER_PORT

if __name__ == "__main__":
    uvicorn.run(
        "dispatcher_service.main:app",
        host=DISPATCHER_HOST,
        port=DISPATCHER_PORT,
        reload=False
    )