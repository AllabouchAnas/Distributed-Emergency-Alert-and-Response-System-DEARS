"""
API routes for the dispatcher service.
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid

from ..schemas import AlertCreate, AlertResponse
from ..services.rpc_service import forward_alert_to_response_service
from ..utils.logger import logger

router = APIRouter()


@router.post("/submit-alert", response_model=AlertResponse)
def submit_alert(alert: AlertCreate):
    """
    Receives an alert via HTTP and forwards it via RPC.
    
    Args:
        alert: Alert data from the request
        
    Returns:
        AlertResponse: Alert details with generated ID
        
    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    logger.info(f"Received alert: {alert}")
    
    # Generate unique alert ID
    alert_id = str(uuid.uuid4())
    timestamp = datetime.now()
    
    # Forward to Response Service (RPC)
    success, message = forward_alert_to_response_service(alert, alert_id)
    
    if success:
        logger.info(f"Alert {alert_id} successfully forwarded to response service")
        status = "forwarded"
    else:
        logger.warning(f"Failed to forward alert {alert_id}: {message}")
        status = "failed_to_forward"

    # Return response
    return AlertResponse(
        alert_id=alert_id,
        status=status,
        timestamp=timestamp
    )


@router.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Dispatcher Service is running", "status": "healthy"}


@router.get("/health")
def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "dispatcher",
        "version": "1.0.0"
    }