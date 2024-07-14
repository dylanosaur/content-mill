#!/bin/bash

# Get the current hour in CST (Central Standard Time)
current_hour=$(date +%H --date="$(TZ='America/Chicago' date)")

# Define the start and end hour for the allowed time range
start_hour=8
end_hour=21

# Check if the current hour is outside the allowed range
if (( current_hour < start_hour || current_hour >= end_hour )); then
  echo "Current time is outside the allowed range. Exiting the script."
  exit 1
else
  echo "current time inside working interval, proceeding with script."
fi

# Generate a random number between 0 and 30
sleep_time=$((RANDOM % 1800))

# Print the sleep time
echo "Sleeping for $sleep_time seconds..."

# Sleep for the generated random time
sleep $sleep_time

# Continue with the rest of your script
echo "Woke up after $sleep_time seconds."



cd /home/ubuntu/content-mill
. .env
source content-venv/bin/activate
python3 generate_cron.py
