import rpyc
import math
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
            # 1. Parse location
            try:
                lat_str, lon_str = location.split(',')
                alert_lat = float(lat_str.strip())
                alert_lon = float(lon_str.strip())
            except ValueError:
                logger.error(f"Invalid location format: {location}")
                return "Error: Invalid location format"

            # 2. Find available Police units
            stmt = select(ResponseUnit).where(
                ResponseUnit.unit_type == "POLICE",
                ResponseUnit.status == "AVAILABLE"
            )
            available_units = db.execute(stmt).scalars().all()
            
            logger.info(f"DEBUG: Found {len(available_units)} available POLICE units.")
            all_units = db.query(ResponseUnit).all()
            logger.info(f"DEBUG: Total units in DB: {len(all_units)}")
            for u in all_units:
                logger.info(f"DEBUG: Unit {u.unit_id} ({u.unit_type}): {u.status}")

            if not available_units:
                logger.warning("No available POLICE units found.")
                return "No available units"

            # 3. Find nearest unit
            nearest_unit = None
            min_distance = float('inf')

            for unit in available_units:
                try:
                    u_lat, u_lon = unit.current_location.split(',')
                    u_lat = float(u_lat.strip())
                    u_lon = float(u_lon.strip())
                    
                    # Simple Euclidean distance (sufficient for MVP)
                    dist = math.sqrt((alert_lat - u_lat)**2 + (alert_lon - u_lon)**2)
                    
                    if dist < min_distance:
                        min_distance = dist
                        nearest_unit = unit
                except ValueError:
                    continue # Skip units with invalid location

            if nearest_unit:
                # 4. Assign unit
                nearest_unit.status = "EN_ROUTE"
                
                # Update Alert
                alert = db.get(Alert, alert_id)
                if alert:
                    alert.assigned_unit = nearest_unit.unit_id
                    alert.status = "ASSIGNED"
                
                db.commit()
                logger.info(f"Assigned Unit {nearest_unit.unit_name} (ID: {nearest_unit.unit_id}) to Alert {alert_id}")
                return f"Unit {nearest_unit.unit_name} dispatched"
            else:
                logger.warning("No units with valid location found.")
                return "No reachable units"

        except Exception as e:
            logger.error(f"Error processing alert: {e}")
            db.rollback()
            return f"Error: {str(e)}"
        finally:
            db.close()
