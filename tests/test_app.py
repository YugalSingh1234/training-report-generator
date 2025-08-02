"""
Test Suite for Training Report Generator
=======================================
"""
import pytest
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_clean import app

@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_page(client):
    """Test the main index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Training Report Generator' in response.data

def test_health_check():
    """Test basic application health."""
    # Test that the app can be imported without errors
    assert app is not None
    assert app.config is not None

def test_config():
    """Test application configuration."""
    with app.app_context():
        assert app.config['TESTING'] == True
        assert 'SECRET_KEY' in app.config

def test_routes_exist():
    """Test that required routes exist."""
    with app.test_request_context():
        # Test that main routes are registered
        rules = [str(rule) for rule in app.url_map.iter_rules()]
        assert '/' in rules
        assert '/generate' in rules or any('/generate' in rule for rule in rules)

def test_static_files():
    """Test static files are accessible."""
    with app.test_client() as client:
        # Test CSS file
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        
        # Test JS file
        response = client.get('/static/js/main.js')
        assert response.status_code == 200

def test_form_validation():
    """Test form validation."""
    with app.test_client() as client:
        # Test empty form submission
        response = client.post('/generate')
        # Should either redirect or show validation errors
        assert response.status_code in [200, 302, 400]

def test_file_upload_validation():
    """Test file upload validation."""
    # Test that security module can be imported
    try:
        from security import SecurityManager
        assert SecurityManager is not None
    except ImportError:
        pytest.skip("Security module not available")

def test_modules_import():
    """Test that all custom modules can be imported."""
    try:
        from modules import document_utils, form_processing, image_processing
        assert document_utils is not None
        assert form_processing is not None
        assert image_processing is not None
    except ImportError as e:
        pytest.fail(f"Failed to import modules: {e}")

def test_templates_exist():
    """Test that required templates exist."""
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    required_templates = ['index.html', 'success.html', 'error.html']
    
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        assert os.path.exists(template_path), f"Template {template} not found"

def test_word_templates_exist():
    """Test that Word templates exist."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    template_files = [
        'word_template_1.docx',
        'word_template_2.docx', 
        'word_template_3.docx',
        'word_template_4.docx',
        'word_template_5.docx'
    ]
    
    for template in template_files:
        template_path = os.path.join(project_root, template)
        assert os.path.exists(template_path), f"Word template {template} not found"

if __name__ == '__main__':
    pytest.main([__file__])
