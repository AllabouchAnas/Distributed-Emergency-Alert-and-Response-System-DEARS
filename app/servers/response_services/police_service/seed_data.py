from .db.db import SessionLocal
from .db.models import ResponseUnit

def seed_data():
    from .db.db import engine, Base
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if we need to seed
        existing_units = db.query(ResponseUnit).all()
        existing_types = set(u.unit_type for u in existing_units)
        
        print(f"Existing unit types: {existing_types}")

        units_to_add = []

        if "POLICE" not in existing_types:
            units_to_add.extend([
                ResponseUnit(unit_name="Police Unit 1", unit_type="POLICE", current_location="40.7128,-74.0060", status="AVAILABLE"),
                ResponseUnit(unit_name="Police Unit 2", unit_type="POLICE", current_location="40.7300,-74.0000", status="AVAILABLE"),
            ])
        
        if "FIRE" not in existing_types:
            units_to_add.append(
                ResponseUnit(unit_name="Fire Unit 1", unit_type="FIRE", current_location="40.7100,-74.0100", status="AVAILABLE")
            )

        if "MEDICAL" not in existing_types:
            units_to_add.append(
                ResponseUnit(unit_name="Medical Unit 1", unit_type="MEDICAL", current_location="40.7200,-74.0200", status="AVAILABLE")
            )

        if units_to_add:
            print(f"Adding {len(units_to_add)} new units...")
            db.add_all(units_to_add)
            db.commit()
            print("Database seeded with missing units.")
        else:
            print("All unit types already exist.")

    except Exception as e:
        print(f"Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
