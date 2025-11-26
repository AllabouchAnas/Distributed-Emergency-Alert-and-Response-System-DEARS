from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from ..enums.alert_status import AlertStatus
from ..enums.emergency_type import EmergencyType
from .models import Alert, User
from ..utils.logger import logger


def create_alert(db: Session, data):
    # Validate emergency type
    if data.emergency_type not in EmergencyType._value2member_map_:
        logger.error(f"Invalid EmergencyType '{data.emergency_type}'")
        raise ValueError(f"Invalid EmergencyType: {data.emergency_type}")

    # Check if user exists
    user = db.query(User).filter(User.user_id == data.user_id).first()
    if not user:
        logger.error(f"User {data.user_id} not found")
        raise ValueError(f"User with ID {data.user_id} does not exist")

    try:
        alert = Alert(
            user_id=data.user_id,
            description=data.description,
            location=data.location,
            emergency_type=data.emergency_type,
            status=AlertStatus.PENDING.value
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)

        logger.info(f"Alert {alert.alert_id} created with status PENDING for user {data.user_id}")
        return alert

    except IntegrityError as e:
        db.rollback()
        logger.exception("Database integrity error on create_alert()")
        # Check if it's a foreign key violation
        if "foreign key constraint" in str(e).lower():
            raise ValueError(f"Invalid user_id: {data.user_id}") from e
        raise RuntimeError("Database integrity error") from e
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error on create_alert()")
        raise RuntimeError("Database error") from e


def update_alert_status(db: Session, alert_id: int, new_status: str):
    if new_status not in AlertStatus._value2member_map_:
        logger.error(f"Invalid AlertStatus '{new_status}'")
        raise ValueError(f"Invalid AlertStatus: {new_status}")

    try:
        alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()

        if not alert:
            logger.error(f"Alert {alert_id} not found")
            raise LookupError(f"Alert {alert_id} does not exist")

        old_status = alert.status
        alert.status = new_status

        db.commit()
        db.refresh(alert)

        logger.info(f"Alert {alert_id} updated from '{old_status}' to '{new_status}'")
        return alert

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error on update_alert_status()")
        raise RuntimeError("Database error") from e
