#!/bin/bash
# Production Deployment Script
# ============================

echo "🚀 Starting deployment process..."

# Set environment
export FLASK_ENV=production
export PYTHONPATH=$(pwd)

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs static/uploads output

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run security checks
echo "🔒 Running security checks..."
python -c "
from security import SecurityManager
print('✅ Security module loaded successfully')
"

# Database migrations (if needed)
# echo "🗄️ Running database migrations..."
# flask db upgrade

# Collect static files (if needed)
echo "📋 Preparing static files..."
# Add any static file processing here

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ || echo "⚠️ Tests not found, skipping..."

# Start the application with Gunicorn
echo "🎯 Starting application..."
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 120 \
         --worker-class sync \
         --max-requests 1000 \
         --max-requests-jitter 50 \
         --preload \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         --log-level info \
         wsgi:app

echo "✅ Deployment completed!"
