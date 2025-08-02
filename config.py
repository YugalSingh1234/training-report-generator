"""
Configuration Settings Module
============================

FUNCTION: Central configuration management for the Training Report Generator application.

RESPONSIBILITIES:
- Defines application-wide configuration settings
- Sets up file upload restrictions and size limits
- Configures directory paths for uploads, outputs, templates, and static files
- Manages allowed file extensions for security
- Provides initialization methods for Flask app setup
- Creates necessary directories automatically

CONFIGURATION AREAS:
- Flask settings (SECRET_KEY, MAX_CONTENT_LENGTH)
- Directory structure (UPLOAD_FOLDER, OUTPUT_FOLDER, etc.)
- File security (ALLOWED_EXTENSIONS)
- Application initialization hooks

USAGE:
- Import Config class and apply to Flask app
- Use Config.init_app(app) to initialize directories
- Access settings via Config.SETTING_NAME

Configuration settings for the Training Report Generator.
"""
import os

class Config:
    """Application configuration class."""
    
    # Flask settings
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024  # 30MB max file size
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Directory settings
    UPLOAD_FOLDER = 'static/uploads'
    OUTPUT_FOLDER = 'output'
    TEMPLATE_FOLDER = 'templates'
    STATIC_FOLDER = 'static'
    
    # File settings
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    @staticmethod
    def init_app(app):
        """Initialize application with config."""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
