from .db.db import SessionLocal
from .db.models import ResponseUnit

def reset_units():
    db = SessionLocal()
    try:
        units = db.query(ResponseUnit).all()
        for u in units:
            u.status = "AVAILABLE"
        db.commit()
        print(f"Reset {len(units)} units to AVAILABLE.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_units()
