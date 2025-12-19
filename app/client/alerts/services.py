import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_alert_to_dispatcher(alert_data):
    """
    Send emergency alert to the dispatcher service via REST API.
    
    Args:
        alert_data (dict): Dictionary containing alert information
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        dispatcher_url = settings.DISPATCHER_SERVICE_URL
        
        # Prepare payload for dispatcher (matches dispatcher schemas.py)
        payload = {
            'user_id': alert_data.get('user_id'),
            'emergency_type': alert_data.get('emergency_type'),
            'description': alert_data.get('description'),
            'location': alert_data.get('location'),
        }
        
        logger.info(f"Sending alert to dispatcher: {dispatcher_url}")
        logger.debug(f"Payload: {payload}")
        
        # Make POST request to dispatcher service
        response = requests.post(
            dispatcher_url,
            json=payload,
            timeout=10,  # 10 second timeout
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            alert_id = response_data.get('alert_id')
            logger.info(f"Alert successfully sent to dispatcher, alert_id: {alert_id}")
            return True, alert_id
        else:
            logger.error(f"Dispatcher returned error: {response.status_code} - {response.text}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to connect to dispatcher service at {dispatcher_url}")
        return False, None
        
    except requests.exceptions.Timeout:
        logger.error("Request to dispatcher service timed out")
        return False, None
        
    except Exception as e:
        logger.error(f"Unexpected error sending alert to dispatcher: {str(e)}")
        return False, None
