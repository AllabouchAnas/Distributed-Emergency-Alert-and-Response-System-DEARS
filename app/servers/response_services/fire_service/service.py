import rpyc
from sqlalchemy import select
from .db.db import SessionLocal
from .db.models import ResponseUnit, Alert
from .utils.logger import logger

class FireService(rpyc.Service):
    def on_connect(self, conn):
        logger.info("New connection established.")
        from .db.db import check_connection
        check_connection()

    def on_disconnect(self, conn):
        logger.info("Connection closed.")

    def exposed_receive_alert(self, alert_id, user_id, description, location, emergency_type, latitude=None, longitude=None):
        """
        RPC method called by Dispatcher.
        """
        logger.info(f"Received alert: ID={alert_id}, Type={emergency_type}, Loc={location}, Lat={latitude}, Lon={longitude}")
        
        db = SessionLocal()
        try:
            # 1. Find or Create alert record in database
            # Check if alert already exists by UUID (alert_id arg)
            import uuid
            try:
                alert_uuid_obj = uuid.UUID(str(alert_id))
            except ValueError:
                logger.error(f"Invalid UUID format: {alert_id}")
                return "Invalid Alert ID"

            existing_alert = db.query(Alert).filter(Alert.alert_uuid == alert_uuid_obj).first()
            
            if existing_alert:
                new_alert = existing_alert
                logger.info(f"Found existing alert in database: ID={new_alert.alert_id} UUID={alert_id}")
            else:
                new_alert = Alert(
                    user_id=user_id,
                    description=description,
                    location=location,
                    emergency_type=emergency_type,
                    status="PENDING",
                    latitude=latitude,
                    longitude=longitude,
                    alert_uuid=alert_uuid_obj
                )
                db.add(new_alert)
                db.commit()
                db.refresh(new_alert)
                logger.info(f"Created new alert in database with ID: {new_alert.alert_id}")
            
            # 2. Find available FIRE units
            
            # 2. Find available FIRE units
            stmt = select(ResponseUnit).where(
                ResponseUnit.unit_type == "FIRE",
                ResponseUnit.status == "AVAILABLE"
            )
            available_units = db.execute(stmt).scalars().all()
            
            logger.info(f"Found {len(available_units)} available FIRE units.")

            if not available_units:
                logger.warning("No available FIRE units found.")
                db.commit()
                return "No available units"

            # 3. Assign nearest available unit based on proximity
            from .utils.distance import haversine_distance
            
            assigned_unit = None
            min_distance = float('inf')
            
            # If alert has coordinates, find nearest unit
            if latitude is not None and longitude is not None:
                for unit in available_units:
                    if unit.latitude is not None and unit.longitude is not None:
                        distance = haversine_distance(latitude, longitude, unit.latitude, unit.longitude)
                        logger.info(f"Unit {unit.unit_name} is {distance:.2f} km away")
                        if distance < min_distance:
                            min_distance = distance
                            assigned_unit = unit
                
                if assigned_unit:
                    logger.info(f"Selected nearest unit {assigned_unit.unit_name} at {min_distance:.2f} km away")
                else:
                    logger.warning("No units with coordinates found, using first available")
                    assigned_unit = available_units[0]
            else:
                logger.warning("Alert has no coordinates, using first available unit")
                assigned_unit = available_units[0]
            
            assigned_unit.status = "EN_ROUTE"
            
            # Update alert with assignment
            new_alert.assigned_unit = assigned_unit.unit_id
            new_alert.status = "ASSIGNED"
            
            db.commit()
            logger.info(f"Assigned Unit {assigned_unit.unit_name} (ID: {assigned_unit.unit_id}) to Alert {new_alert.alert_id}")
            return f"Unit {assigned_unit.unit_name} dispatched"

        except Exception as e:
            logger.error(f"Error processing alert: {e}")
            db.rollback()
            return f"Error: {str(e)}"
        finally:
            db.close()
