#!/bin/bash
# Startup script for MyNaksh Personalization Engine

set -e

echo "===================================================="
echo " Starting MyNaksh Personalized AI Context Engine    "
echo "===================================================="

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

echo "Running unit test suite..."
./venv/bin/pytest -v

echo "Starting FastAPI Server on http://localhost:8000 ..."
echo "API Docs: http://localhost:8000/docs"
echo "Web Dashboard: http://localhost:8000/"

./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
