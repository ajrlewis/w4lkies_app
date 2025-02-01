#! /usr/bin/env bash

usage() {
   echo "Script to start a WSGI server for a Flask app."
   echo
   echo "Syntax: install.sh [-d|h]"
   echo "options:"
   echo "h     Initialize gandi and github remote repositories."
   echo "p     Push to remote repositories."
   echo "u     Print this usage."
   echo
}

host="0.0.0.0"
port="5000"

while getopts ":h:p:u" option; do
    case $option in
        h) #
            host=${OPTARG};;
        p) #
            port=${OPTARG};;
        u) # display usage
            usage;
            exit;;
        \?) # Invalid option
            echo "Error: Invalid option";
            exit;;
   esac
done

source venv/bin/activate
python3 wsgi.py "$host" "$port"
deactivate
