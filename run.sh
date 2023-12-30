#!/bin/bash

echo "Script execution started."

# Run the main Python script
uvicorn src.controller:app

# Deactivation is not strictly necessary for a script, as the environment changes
# do not persist when the script finishes
echo "Script execution finished."
