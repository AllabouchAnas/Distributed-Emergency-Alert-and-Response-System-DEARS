"""
Dispatcher Service - Main Application Entry Point

This is the main FastAPI application that coordinates emergency alert dispatching.
The actual business logic is separated into different modules:
- api/routes.py: API endpoints
- services/rpc_service.py: RPC communication with response services
- db/crud.py: Database operations
"""
from fastapi import FastAPI
from .db.db import engine
from .db import models
from .api.routes import router



# Create FastAPI application
app = FastAPI(
    title="Dispatcher Service",
    description="Emergency Alert Dispatching System - Routes alerts to appropriate response services",
    version="1.0.0"
)

# Include API routes
app.include_router(router)
