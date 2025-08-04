"""
Production Configuration Module
==============================
Industry-level configuration with environment-based settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 30 * 1024 * 1024))  # 30MB
    
    # Directory paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'static', 'uploads')
    OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER') or os.path.join(BASE_DIR, 'output')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    
    # Security
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 3600))
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration."""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(Config.BASE_DIR, 'logs'), exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    ENV = 'production'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific setup
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Setup logging
        if not app.debug:
            file_handler = RotatingFileHandler(
                'logs/app.log', maxBytes=10240000, backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Application startup')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
