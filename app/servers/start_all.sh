#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Error: .venv not found. Please run ./setup_env.sh first."
    exit 1
fi

# Run the python script using the linux venv
echo "Starting all services..."
.venv/bin/python3 run_all_services.py
