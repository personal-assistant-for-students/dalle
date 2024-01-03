#!/bin/bash

echo "Script execution started."
mkdir images
source setenv.sh
pytest
# Run the main Python script
uvicorn src.controller:app --host '0.0.0.0' --port 8000
# Deactivation is not strictly necessary for a script, as the environment changes
# do not persist when the script finishes
echo "Script execution finished."
