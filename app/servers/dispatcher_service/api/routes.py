"""
API routes for the dispatcher service.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..db.db import get_db
from ..db import crud
from ..schemas import AlertCreate, AlertResponse
from ..services.rpc_service import forward_alert_to_response_service
from ..utils.logger import logger

router = APIRouter()


@router.post("/submit-alert", response_model=AlertResponse)
def submit_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """
    Receives an alert via HTTP, saves it to DB, and forwards it via RPC.
    
    Args:
        alert: Alert data from the request
        db: Database session
        
    Returns:
        AlertResponse: Created alert details
        
    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    logger.info(f"Received alert: {alert}")
    
    # 1. Save to Database
    try:
        db_alert = crud.create_alert(db, alert)
    except ValueError as e:
        # Validation errors (user not found, invalid data, etc.)SSS
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Database or other unexpected errors
        logger.exception("Unexpected error creating alert")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    # 2. Forward to Response Service (RPC)
    success, message = forward_alert_to_response_service(alert, db_alert.alert_id)
    
    if success:
        logger.info(f"Alert {db_alert.alert_id} successfully forwarded to response service")
    else:
        logger.warning(f"Failed to forward alert {db_alert.alert_id}: {message}")
        # We don't fail the HTTP request because the alert IS saved. 
        # But we might want to mark it as 'FAILED_TO_SEND' in a real app.

    return db_alert


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
