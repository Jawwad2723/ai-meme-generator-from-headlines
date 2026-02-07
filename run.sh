#!/bin/bash

# Startup script for AI Meme Generator

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
