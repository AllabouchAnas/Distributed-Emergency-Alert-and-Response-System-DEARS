# Database Models Implementation Summary

## ✅ Completed Changes

### 1. Enumerations Created

All services now have consistent enumerations:

#### Alert Status
- `PENDING` - Alert received, awaiting processing
- `IN_PROGRESS` - Alert being actively handled  
- `RESOLVED` - Alert completed/closed

#### Emergency Type
- `POLICE` - Police emergency
- `FIRE` - Fire emergency
- `MEDICAL` - Medical emergency

#### Unit Status
- `AVAILABLE` - Unit ready for assignment
- `EN_ROUTE` - Unit traveling to scene
- `ON_SCENE` - Unit at emergency location
- `UNAVAILABLE` - Unit offline/unavailable

#### User Role
- `CITIZEN` - Regular user
- `ADMIN` - Administrator
- `RESPONDER` - Emergency responder

### 2. Models Updated

#### Dispatcher Service
**Location**: `app/servers/dispatcher_service/db/models.py`

- ✅ Added `latitude` and `longitude` to Alert model
- ✅ Added `latitude` and `longitude` to ResponseUnit model
- ✅ Updated all status fields to use SQLAlchemy Enum types
- ✅ User model now uses UserRole enum

#### Police Service
**Location**: `app/servers/response_services/police_service/db/models.py`

- ✅ Updated Alert model with proper enums
- ✅ Updated ResponseUnit model with proper enums
- ✅ User model uses UserRole enum
- ✅ Latitude/longitude already present, now with proper types

#### Fire Service
**Location**: `app/servers/response_services/fire_service/db/models.py`

- ✅ Updated Alert model with proper enums
- ✅ Updated ResponseUnit model with proper enums
- ✅ User model uses UserRole enum
- ✅ Latitude/longitude already present, now with proper types

#### Medical Service
**Location**: `app/servers/response_services/medical_service/db/models.py`

- ✅ Updated Alert model with proper enums
- ✅ Updated ResponseUnit model with proper enums
- ✅ User model uses UserRole enum  
- ✅ Latitude/longitude already present, now with proper types

#### Client (Django)
**Location**: `app/client/alerts/models.py`

- ✅ Updated Alert status: PENDING/IN_PROGRESS/RESOLVED
- ✅ Updated EmergencyReport status: PENDING/IN_PROGRESS/RESOLVED
- ✅ Updated ResponseUnit status: Changed `ON_SITE` to `ON_SCENE`
- ✅ Added `latitude` and `longitude` to ResponseUnit model
- ✅ Kept RESPONDER role as requested

### 3. Database Migrations

#### Django Client
- ✅ Migration created: `0007_alter_alert_status_alter_emergencyreport_status_and_more.py`
- ✅ Migration applied successfully to database

#### SQLAlchemy Services (Dispatcher & Response Services)
- ⏳ Alembic setup script created: `app/servers/setup_alembic.sh`
- ⏳ Requires manual execution in WSL to complete setup

## 📋 Next Steps

### To Complete Alembic Migrations:

1. **Run the Alembic setup script in WSL**:
   ```bash
   cd /mnt/c/Users/Hamza/Desktop/distributed_system/Distributed-Emergency-Alert-and-Response-System-DEARS/app/servers
   chmod +x setup_alembic.sh
   ./setup_alembic.sh
   ```

2. **Review generated migrations** in each service's `alembic/versions/` directory

3. **Update `alembic.ini`** in each service with correct database URL (if needed)

4. **Apply migrations** in each service:
   ```bash
   # For each service (dispatcher, police, fire, medical)
   cd /path/to/service
   source .venv/bin/activate
   alembic upgrade head
   ```

### Alternative: Manual Alembic Setup

If the script encounters issues, you can set up Alembic manually for each service:

```bash
cd /path/to/service
source .venv/bin/activate
pip install alembic
alembic init alembic
# Edit alembic/env.py to import your models and set target_metadata
alembic revision --autogenerate -m "Initial migration with updated models"
alembic upgrade head
```

## 🔍 Model Structure Summary

All services now follow this consistent structure:

### User Model
- `user_id` (Primary Key)
- `username` (Unique)
- `password_hash`
- `role` (UserRole enum)

### Alert Model
- `alert_id` (Primary Key)
- `user_id` (Foreign Key)
- `timestamp`
- `description`
- `location` (text address)
- `latitude` (Float/Decimal)
- `longitude` (Float/Decimal)
- `status` (AlertStatus enum)
- `emergency_type` (EmergencyType enum)
- `assigned_unit` (Foreign Key to ResponseUnit)

### ResponseUnit Model
- `unit_id` (Primary Key)
- `unit_name`
- `unit_type` (EmergencyType enum)
- `current_location` (text address)
- `latitude` (Float/Decimal)
- `longitude` (Float/Decimal)
- `status` (UnitStatus enum)

## ⚠️ Important Notes

1. **Status Value Changes**: Existing alerts in databases may have old status values (NEW, DISPATCHED, CANCELLED). These will need to be migrated to PENDING/IN_PROGRESS/RESOLVED.

2. **Enum Column Types**: SQLAlchemy creates CHECK constraints for enum columns. Existing databases may need adjustments.

3. **Testing Required**: After applying migrations, test:
   - Alert creation with latitude/longitude
   - Status updates with new values
   - Response unit location tracking
   - Cross-service communication

4. **Data Migration**: If you have existing data, create data migration scripts to:
   - Map `NEW` → `PENDING`
   - Map `DISPATCHED` or `ACTIVE` → `IN_PROGRESS`
   - Map `ON_SITE` → `ON_SCENE` for units
