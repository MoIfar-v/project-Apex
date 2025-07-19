#!/bin/bash

# Set project root directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the venv
source "$VENV_DIR/bin/activate"

# Install dependencies if requirements.txt exists
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r "$PROJECT_DIR/requirements.txt"
fi

# Run the main Python script
echo "Running main.py..."
python "$PROJECT_DIR/src/main.py" "$@"