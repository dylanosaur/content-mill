#!/bin/bash

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
