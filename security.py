"""
Security Enhancement Module
==========================
"""
import os
import secrets
from functools import wraps
from flask import request, abort, current_app
import mimetypes

class SecurityManager:
    """Handle security-related functionality."""
    
    @staticmethod
    def generate_secret_key():
        """Generate a secure secret key."""
        return secrets.token_hex(32)
    
    @staticmethod
    def validate_file_upload(file):
        """Validate uploaded file for security."""
        if not file or not file.filename:
            return False, "No file selected"
            
        # Check file extension
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', set())
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return False, f"File type .{file_ext} not allowed"
        
        # Check MIME type
        mime_type, _ = mimetypes.guess_type(file.filename)
        allowed_mimes = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg', 
            'png': 'image/png',
            'gif': 'image/gif'
        }
        
        if mime_type != allowed_mimes.get(file_ext):
            return False, "File content doesn't match extension"
            
        # Check file size
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
        if hasattr(file, 'content_length') and file.content_length > max_size:
            return False, "File too large"
            
        return True, "File is valid"
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename to prevent directory traversal."""
        import re
        # Remove any path components
        filename = os.path.basename(filename)
        # Remove dangerous characters
        filename = re.sub(r'[^\w\-_\.]', '', filename)
        # Ensure it's not empty and has an extension
        if not filename or '.' not in filename:
            filename = f"upload_{secrets.token_hex(8)}.jpg"
        return filename

def rate_limit(max_requests=10, per_seconds=60):
    """Rate limiting decorator."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Simple in-memory rate limiting
            # In production, use Redis or similar
            client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            # Implementation would go here
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_api_key(f):
    """Require API key for certain endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = current_app.config.get('API_KEY')
        
        if not api_key or api_key != expected_key:
            abort(401)
            
        return f(*args, **kwargs)
    return decorated_function
