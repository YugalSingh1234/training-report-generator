"""
Application Factory for Production Deployment
===========================================
Simple application factory for production deployment.

NOTE: This file is for advanced deployment scenarios only.
For normal development and deployment, use app_clean.py directly.

The main application with all routes is in app_clean.py.
This factory is provided for containerized deployments that
require application factory pattern.
"""
import os
from flask import Flask, render_template, jsonify
from config_production import config

def create_app(config_name=None):
    """
    Simple application factory function for production.
    
    For full application functionality, use app_clean.py instead.
    This factory provides minimal configuration for containerized deployments.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Basic health check route
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "app": "Training Report Generator"})
    
    # Redirect to main application notice
    @app.route('/')
    def index():
        return '''
        <h2>Training Report Generator</h2>
        <p>This is the factory deployment version.</p>
        <p>For full functionality, deploy using app_clean.py</p>
        <p><a href="/health">Health Check</a></p>
        '''
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', error_message="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html', error_message="Internal server error"), 500
    
    @app.errorhandler(413)
    def file_too_large(error):
        return render_template('error.html', error_message="File too large. Maximum size is 30MB."), 413
    
    return app
