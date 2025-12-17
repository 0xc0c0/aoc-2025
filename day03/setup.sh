#!/usr/bin/env bash

# Get the directory where the script is located, handling symlinks and various invocation methods
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Change the current working directory to the script's directory
cd "$SCRIPT_DIR"

# Now, any subsequent commands in the script will run from the SCRIPT_DIR
echo "Executing setup in: $(pwd)"

echo "setting up venv..."
python -m venv venv

echo "activating venv..."
source venv/bin/activate

if [ -f requirements.txt ]; then
    echo "installing requirements from requirements.txt"
    python -m pip install -r requirements.txt
fi

echo "...complete"
