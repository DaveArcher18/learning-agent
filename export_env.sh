#!/bin/bash
# Simple script to load environment variables from .env file

if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    set -a
    source .env
    set +a
    echo "Done! Environment variables are now available in this shell session."
else
    echo "Error: .env file not found."
    echo "Please create .env file based on env.sample"
    exit 1
fi 