#!/bin/bash

# Fake Review Detection API - Quick Start Script

echo "🚀 Starting Fake Review Detection API..."

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 -U user -d fake_reviews > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running. Starting with Docker..."
    docker compose up -d postgres redis
    echo "⏳ Waiting for PostgreSQL to be ready..."
    
    # Wait for PostgreSQL to be ready with better health check
    echo "Waiting for PostgreSQL container to be healthy..."
    timeout=60
    elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if docker compose exec postgres pg_isready -U user -d fake_reviews > /dev/null 2>&1; then
            echo "✅ PostgreSQL is ready!"
            break
        fi
        sleep 2
        elapsed=$((elapsed + 2))
        echo "Still waiting... (${elapsed}s)"
    done
    
    if [ $elapsed -ge $timeout ]; then
        echo "❌ PostgreSQL failed to start within ${timeout} seconds"
        exit 1
    fi
fi

# Create database if it doesn't exist
echo "📊 Setting up database..."
source new_venv/bin/activate
alembic revision --autogenerate -m "Initial migration" || true
alembic upgrade head || true

# Start the application
echo "🌐 Starting FastAPI application..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
