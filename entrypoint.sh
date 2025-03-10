#!/bin/sh

# Check if the command argument is provided
if [ -z "$1" ]; then
  echo "Error: No command provided. Please provide a time interval in seconds."
  exit 1
fi

# Get the time interval from the command argument
INTERVAL=$1

# Run the Python app at the specified interval
while true; do
  python -m UpdateNotifier
  echo "Waiting for $INTERVAL seconds..."
  sleep $INTERVAL
done