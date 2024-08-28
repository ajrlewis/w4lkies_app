#!/bin/bash

# wsgi.sh - a script to start a WSGI server for a Flask app
#
# Usage: bash wsgi.sh <host> <port>
# Example: bash wsgi.sh 127.0.0.1 5000
#

# Print the current date and time, followed by the name of the script being called
echo "$(date +"%a %b %d %T %Y") - Running script: $0"

# Set the host, and port from the command line arguments

host=$1
port=$2

# Activate the virtual environment
source venv/bin/activate

# Start the WSGI server using the specified host and port
python3 wsgi.py "$host" "$port"

deactivate