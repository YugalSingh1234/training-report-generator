"""
Test Modules Package
===================
"""
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestModulesImport:
    """Test that all modules can be imported."""
    
    def test_import_document_utils(self):
        """Test document utils import."""
        from modules import document_utils
        assert hasattr(document_utils, 'save_uploaded_file')
        assert hasattr(document_utils, 'insert_paragraph_after')
        assert hasattr(document_utils, 'insert_table_after')
    
    def test_import_form_processing(self):
        """Test form processing import."""
        from modules import form_processing
        assert hasattr(form_processing, 'process_form_data')
        assert hasattr(form_processing, 'combine_person_list')
        assert hasattr(form_processing, 'process_gallery_images')
    
    def test_import_image_processing(self):
        """Test image processing import."""
        from modules import image_processing
        assert hasattr(image_processing, 'insert_gallery_table')
        assert hasattr(image_processing, 'insert_annexure_images')
        assert hasattr(image_processing, 'get_annexure_images_and_captions')

class TestFormProcessing:
    """Test form processing functions."""
    
    def test_combine_person_list_empty(self):
        """Test combining empty person list."""
        from modules.form_processing import combine_person_list
        result = combine_person_list([], [], [])
        assert result == ''
    
    def test_combine_person_list_single(self):
        """Test combining single person."""
        from modules.form_processing import combine_person_list
        result = combine_person_list(['Dr.'], ['John Smith'], ['Director'])
        assert result == 'Dr. John Smith (Director)'
    
    def test_combine_person_list_multiple(self):
        """Test combining multiple persons."""
        from modules.form_processing import combine_person_list
        result = combine_person_list(
            ['Dr.', 'Ms.'], 
            ['John Smith', 'Jane Doe'], 
            ['Director', 'Manager']
        )
        assert 'Dr. John Smith (Director)' in result
        assert 'Ms. Jane Doe (Manager)' in result
        assert ', ' in result
    
    def test_combine_person_list_no_designation(self):
        """Test combining person without designation."""
        from modules.form_processing import combine_person_list
        result = combine_person_list(['Mr.'], ['John Smith'], [''])
        assert result == 'Mr. John Smith'
        assert '()' not in result

class TestDocumentUtils:
    """Test document utilities."""
    
    def test_save_uploaded_file_none(self):
        """Test saving None file."""
        from modules.document_utils import save_uploaded_file
        result = save_uploaded_file(None)
        assert result is None
    
    def test_save_uploaded_file_no_filename(self):
        """Test saving file with no filename."""
        from modules.document_utils import save_uploaded_file
        
        class MockFile:
            filename = ''
        
        result = save_uploaded_file(MockFile())
        assert result is None
