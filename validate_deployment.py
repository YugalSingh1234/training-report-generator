"""
Production Readiness Validation Script
====================================
Comprehensive validation for industry-level deployment.
"""
import os
import sys
import importlib
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def check_module_imports():
    """Check if all modules can be imported."""
    modules_to_test = [
        'app_clean',
        'config',
        'config_production', 
        'security',
        'monitoring',
        'modules.document_utils',
        'modules.form_processing',
        'modules.image_processing'
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    print("\n🔍 Module Import Tests:")
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
    
    print(f"\n📊 Module Import Summary: {success_count}/{total_count} successful")
    return success_count == total_count

def check_required_files():
    """Check if all required files exist."""
    print("\n📁 Required Files Check:")
    
    files_to_check = [
        ('app_clean.py', 'Main application file'),
        ('wsgi.py', 'WSGI entry point'),
        ('requirements.txt', 'Dependencies'),
        ('Dockerfile', 'Docker configuration'),
        ('deploy.sh', 'Deployment script'),
        ('DEPLOYMENT.md', 'Deployment documentation'),
        ('.env.example', 'Environment template'),
        ('pytest.ini', 'Test configuration'),
        ('security-report.json', 'Security scan report'),
    ]
    
    success_count = 0
    for filepath, description in files_to_check:
        if check_file_exists(filepath, description):
            success_count += 1
    
    return success_count == len(files_to_check)

def check_directories():
    """Check if required directories exist."""
    print("\n📂 Required Directories Check:")
    
    directories = [
        ('templates', 'HTML templates'),
        ('static', 'Static files'),
        ('static/css', 'CSS files'),
        ('static/js', 'JavaScript files'),
        ('modules', 'Python modules'),
        ('tests', 'Test files'),
        ('output', 'Generated documents'),
        ('static/uploads', 'File uploads'),
        ('.github/workflows', 'CI/CD pipeline')
    ]
    
    success_count = 0
    for dirpath, description in directories:
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            print(f"✅ {description}: {dirpath}")
            success_count += 1
        else:
            print(f"❌ {description}: {dirpath} - NOT FOUND")
    
    return success_count == len(directories)

def check_templates():
    """Check if required templates exist."""
    print("\n📄 Template Files Check:")
    
    templates = [
        'templates/index.html',
        'templates/success.html', 
        'templates/error.html'
    ]
    
    word_templates = [
        'word_template_1.docx',
        'word_template_2.docx',
        'word_template_3.docx',
        'word_template_4.docx',
        'word_template_5.docx'
    ]
    
    success_count = 0
    total_count = len(templates) + len(word_templates)
    
    for template in templates:
        if check_file_exists(template, 'HTML template'):
            success_count += 1
    
    for template in word_templates:
        if check_file_exists(template, 'Word template'):
            success_count += 1
    
    return success_count == total_count

def run_production_checks():
    """Run all production readiness checks."""
    print("🏭 Production Readiness Validation")
    print("=" * 50)
    
    checks = [
        ("Files", check_required_files),
        ("Directories", check_directories), 
        ("Templates", check_templates),
        ("Modules", check_module_imports)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_function in checks:
        try:
            if check_function():
                print(f"\n✅ {check_name} check: PASSED")
                passed_checks += 1
            else:
                print(f"\n❌ {check_name} check: FAILED")
        except Exception as e:
            print(f"\n❌ {check_name} check: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Overall Results: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 ALL CHECKS PASSED - Ready for production deployment!")
        return True
    else:
        print("⚠️  Some checks failed - Review and fix issues before deployment")
        return False

if __name__ == "__main__":
    success = run_production_checks()
    sys.exit(0 if success else 1)
