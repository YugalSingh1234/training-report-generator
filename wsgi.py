"""
WSGI Entry Point for Production Deployment
=========================================
"""
import os
from app_clean import app

if __name__ == "__main__":
    # For development
    app.run(debug=False, host='0.0.0.0', port=5000)
else:
    # For production WSGI servers (Gunicorn, uWSGI)
    application = app
