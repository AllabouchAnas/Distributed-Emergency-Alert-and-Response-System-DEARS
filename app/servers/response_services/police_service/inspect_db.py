from .db.db import SessionLocal
from .db.models import ResponseUnit

def inspect_db():
    db = SessionLocal()
    try:
        units = db.query(ResponseUnit).all()
        print(f"Total units: {len(units)}")
        for u in units:
            print(f"ID: {u.unit_id}, Name: {u.unit_name}, Type: {u.unit_type}, Status: {u.status}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inspect_db()
