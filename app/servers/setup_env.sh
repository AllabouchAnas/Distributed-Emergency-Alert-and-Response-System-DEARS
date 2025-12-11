#!/bin/bash

# Exit on error
set -e

echo "Creating Python virtual environment (.venv)..."
python3 -m venv .venv

echo "Activating environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! You can now run ./start_all.sh"
