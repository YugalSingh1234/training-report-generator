"""
Training Report Generator - Multi-Type Application
=================================================

Main Flask application that serves as entry point for all training types.
Provides landing page with training type selection and registers blueprints
for each training type.
"""
from flask import Flask, render_template, send_file
import os
from config import Config

# Import training type blueprints
from trainings.type_a.routes import type_a_bp
from trainings.type_b.routes import type_b_bp
from trainings.type_c.routes import type_c_bp
from trainings.type_d.routes import type_d_bp

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Register blueprints for each training type
app.register_blueprint(type_a_bp, url_prefix='/type-a')
app.register_blueprint(type_b_bp, url_prefix='/type-b')
app.register_blueprint(type_c_bp, url_prefix='/type-c')
app.register_blueprint(type_d_bp, url_prefix='/type-d')

# File size and upload validation
@app.before_request
def limit_remote_addr():
    """Check file upload limits and validate requests."""
    from flask import request, abort
    if request.content_length and request.content_length > app.config['MAX_CONTENT_LENGTH']:
        abort(413)  # Request Entity Too Large

# Register error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

@app.errorhandler(413)
def file_too_large(error):
    return render_template('error.html', error="File too large"), 413

# Add security headers for production
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/')
def home():
    """Main landing page with training type selection."""
    print("📋 Home page accessed")
    return render_template('home.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    from flask import jsonify
    from datetime import datetime
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated reports."""
    try:
        output_dir = Config.OUTPUT_FOLDER
        file_path = os.path.join(output_dir, filename)
        
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        else:
            return "File not found", 404
            
    except Exception as e:
        print(f"❌ Download error: {str(e)}")
        return f"Error downloading file: {str(e)}", 500

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
