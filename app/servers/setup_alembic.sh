#!/bin/bash
# Setup Alembic and create migrations for all SQLAlchemy services

set -e

echo "========================================="
echo "Setting up Alembic for DEARS Services"
echo "========================================="

# Function to setup Alembic for a service
setup_alembic_for_service() {
    local service_path=$1
    local service_name=$2
    
    echo ""
    echo "Setting up Alembic for $service_name..."
    cd "$service_path"
    
    # Activate virtual environment if it exists
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    
    # Check if Alembic is installed
    if ! python -c "import alembic" 2>/dev/null; then
        echo "Installing Alembic..."
        pip install alembic
    fi
    
    # Initialize Alembic if not already done
    if [ ! -f "alembic.ini" ]; then
        echo "Initializing Alembic..."
        alembic init alembic
        
        # Update alembic.ini to use the correct database URL from config
        # This will need manual adjustment based on your config
        echo "Please update alembic.ini with your database URL"
    else
        echo "Alembic already initialized"
    fi
    
    # Create initial migration
    echo "Creating migration for $service_name..."
    alembic revision --autogenerate -m "Update models with enums and lat/lon fields"
    
    echo "$service_name setup complete!"
}

# Base path
BASE_PATH="/mnt/c/Users/Hamza/Desktop/distributed_system/Distributed-Emergency-Alert-and-Response-System-DEARS/app/servers"

# Setup for Dispatcher Service
setup_alembic_for_service "$BASE_PATH/dispatcher_service" "Dispatcher Service"

# Setup for Response Services
setup_alembic_for_service "$BASE_PATH/response_services/police_service" "Police Service"
setup_alembic_for_service "$BASE_PATH/response_services/fire_service" "Fire Service"
setup_alembic_for_service "$BASE_PATH/response_services/medical_service" "Medical Service"

echo ""
echo "========================================="
echo "Alembic setup complete for all services!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Review the generated migration files"
echo "2. Update alembic.ini files with correct database URLs"
echo "3. Run 'alembic upgrade head' in each service directory to apply migrations"
