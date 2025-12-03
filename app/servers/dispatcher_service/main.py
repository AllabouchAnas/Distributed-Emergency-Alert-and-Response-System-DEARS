from fastapi import FastAPI
from .api.routes import router



# Create FastAPI application
app = FastAPI(
    title="Dispatcher Service",
    description="Emergency Alert Dispatching System - Routes alerts to appropriate response services",
    version="1.0.0"
)

# Include API routes
app.include_router(router)
