#!/bin/bash

echo "Script execution started."

# Source the environment setup script
source setenv.sh

# Run the main Python script
uvicorn src.controller:app

# Deactivation is not strictly necessary for a script, as the environment changes
# do not persist when the script finishes
echo "Script execution finished."
