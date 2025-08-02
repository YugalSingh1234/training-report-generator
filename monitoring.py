"""
Monitoring and Health Check Module
=================================
"""
from flask import Blueprint, jsonify, current_app
import os
import psutil
from datetime import datetime

monitoring = Blueprint('monitoring', __name__)

@monitoring.route('/health')
def health_check():
    """Application health check endpoint."""
    try:
        # Check if critical directories exist
        upload_dir = current_app.config.get('UPLOAD_FOLDER')
        output_dir = current_app.config.get('OUTPUT_FOLDER')
        
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'upload_directory': os.path.exists(upload_dir),
                'output_directory': os.path.exists(output_dir),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            }
        }
        
        # Check if any critical checks failed
        critical_checks = ['upload_directory', 'output_directory']
        if not all(health_status['checks'][check] for check in critical_checks):
            health_status['status'] = 'unhealthy'
            return jsonify(health_status), 503
            
        return jsonify(health_status), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@monitoring.route('/metrics')
def metrics():
    """Application metrics endpoint."""
    try:
        return jsonify({
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent
            },
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count()
            },
            'disk': {
                'total': psutil.disk_usage('/').total if os.name != 'nt' else psutil.disk_usage('C:').total,
                'used': psutil.disk_usage('/').used if os.name != 'nt' else psutil.disk_usage('C:').used,
                'percent': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
