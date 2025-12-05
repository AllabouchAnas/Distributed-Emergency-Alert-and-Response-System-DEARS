import rpyc
from sqlalchemy import select
from .db.db import SessionLocal
from .db.models import ResponseUnit, Alert
from .utils.logger import logger

class PoliceService(rpyc.Service):
    def on_connect(self, conn):
        logger.info("New connection established.")

    def on_disconnect(self, conn):
        logger.info("Connection closed.")

    def exposed_receive_alert(self, alert_id, description, location, emergency_type):
        """
        RPC method called by Dispatcher.
        """
        logger.info(f"Received alert: ID={alert_id}, Type={emergency_type}, Loc={location}")
        
        db = SessionLocal()
        try:
            # 1. Create alert record in database
            new_alert = Alert(
                user_id=1,  # Default user_id since dispatcher doesn't send it
                description=description,
                location=location,
                emergency_type=emergency_type,
                status="PENDING"
            )
            db.add(new_alert)
            db.flush()  # Get the auto-generated alert_id
            
            logger.info(f"Created alert in database with ID: {new_alert.alert_id}")
            
            # 2. Find available Police units
            stmt = select(ResponseUnit).where(
                ResponseUnit.unit_type == "POLICE",
                ResponseUnit.status == "AVAILABLE"
            )
            available_units = db.execute(stmt).scalars().all()
            
            logger.info(f"Found {len(available_units)} available POLICE units.")

            if not available_units:
                logger.warning("No available POLICE units found.")
                db.commit()
                return "No available units"

            # 3. Assign first available unit
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
