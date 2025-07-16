#!/bin/sh

set -e

# Start the Ollama server in the background
ollama serve &

# Wait for it to become ready
echo "Waiting for Ollama to become ready..."
sleep 5  # could be replaced with a curl-based healthcheck

# Pull your model(s)
echo "Pulling phi3 model..."
ollama pull phi3

# Keep the container alive
wait
