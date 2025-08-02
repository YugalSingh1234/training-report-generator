#!/bin/bash
# Render.com startup script

# Create necessary directories
mkdir -p static/uploads
mkdir -p output
mkdir -p logs

# Set permissions
chmod 755 static/uploads
chmod 755 output
chmod 755 logs

# Start the application
exec gunicorn app_clean:app --host 0.0.0.0 --port $PORT --workers 2 --timeout 120
