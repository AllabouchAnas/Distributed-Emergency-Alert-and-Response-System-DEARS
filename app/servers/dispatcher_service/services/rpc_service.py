"""
RPC Service for forwarding alerts to response services.
"""
import rpyc
from ..schemas import AlertCreate
from ..config import RPC_SERVICES
from ..utils.logger import logger


def forward_alert_to_response_service(alert_data: AlertCreate, alert_id: int) -> tuple[bool, str]:

    service_info = RPC_SERVICES.get(alert_data.emergency_type.value)
    if not service_info:
        logger.error(f"No RPC service configured for type: {alert_data.emergency_type}")
        return False, "Service not configured"

    try:
        logger.info(f"Connecting to {alert_data.emergency_type} service at {service_info['host']}:{service_info['port']}")
        
        # Connect to the remote service
        conn = rpyc.connect(service_info['host'], service_info['port'])
        
        # Call the remote method
        # Assuming the remote service exposes a 'receive_alert' method
        response = conn.root.receive_alert(
            alert_id,
            alert_data.description,
            alert_data.location,
            alert_data.emergency_type.value
        )
        
        conn.close()
        logger.info(f"RPC call successful: {response}")
        return True, response
        
    except Exception as e:
        logger.exception(f"Failed to connect to {alert_data.emergency_type} service")
        return False, str(e)
