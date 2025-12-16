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
        
        # Prepare payload for dispatcher
        payload = {
            'emergency_type': alert_data.get('emergency_type'),
            'description': alert_data.get('description'),
            'location': alert_data.get('location'),
            'latitude': float(alert_data.get('latitude')) if alert_data.get('latitude') else None,
            'longitude': float(alert_data.get('longitude')) if alert_data.get('longitude') else None,
            'contact_name': alert_data.get('name'),
            'contact_info': alert_data.get('contact_info'),
            'report_id': str(alert_data.get('id')),
        }
        
        logger.info(f"Sending alert to dispatcher: {dispatcher_url}")
        
        # Make POST request to dispatcher service
        response = requests.post(
            dispatcher_url,
            json=payload,
            timeout=10,  # 10 second timeout
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200 or response.status_code == 201:
            logger.info(f"Alert successfully sent to dispatcher for report {alert_data.get('id')}")
            return True, "Alert successfully dispatched to emergency services"
        else:
            logger.error(f"Dispatcher returned error: {response.status_code} - {response.text}")
            return False, f"Dispatcher service error: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to connect to dispatcher service at {dispatcher_url}")
        return False, "Unable to connect to dispatcher service. Alert saved locally."
        
    except requests.exceptions.Timeout:
        logger.error("Request to dispatcher service timed out")
        return False, "Dispatcher service timeout. Alert saved locally."
        
    except Exception as e:
        logger.error(f"Unexpected error sending alert to dispatcher: {str(e)}")
        return False, f"Error communicating with dispatcher: {str(e)}"
