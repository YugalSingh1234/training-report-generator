"""
Training Report Generator - Clean Modular Application
====================================================

FUNCTION: Clean copy of the modular Flask application for training report generation.

PURPOSE:
This is a clean, working version of the modular application that can be used as a backup
or reference implementation. It contains the same functionality as app_modular.py but
serves as a stable version for production use or deployment.

FUNCTIONALITY:
- Web interface for training report data input
- Document generation from Word templates
- Image processing for logos, galleries, and annexures
- Form data processing with dynamic person lists
- Modular architecture with separated concerns

ARCHITECTURE:
- Uses modular imports from the modules/ package
- Follows Flask application factory pattern
- Clean separation of document, form, and image processing
- Configuration management through config.py

USAGE:
Run this file for a stable version of the Training Report Generator:
    python app_clean.py

A Flask web application for generating training report documents.
"""
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, abort
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches, Cm

# Import our custom modules
from config import Config
from modules.document_utils import find_and_replace_text, find_and_replace_image, save_uploaded_file
from modules.image_processing import insert_gallery_table, get_annexure_images_and_captions, insert_annexure_images
from modules.form_processing import process_form_data, process_gallery_images


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    
    # File size and upload validation
    @app.before_request
    def limit_remote_addr():
        """Check file upload limits and validate requests."""
        if request.content_length and request.content_length > app.config['MAX_CONTENT_LENGTH']:
            abort(413)  # Request Entity Too Large
    
    return app


def register_routes(app):
    """Register routes with the Flask application instance."""
    
    @app.route('/')
    def index():
        """Main page with the form."""
        print("📋 Index page accessed")
        return render_template('index.html')

    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

    @app.route('/test')
    def test_form():
        """Simple test form for debugging."""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Form</title>
        </head>
        <body>
            <h2>Quick Test Form</h2>
            <form action="/generate" method="post">
                <label>Event Date:</label>
                <input type="date" name="event_date" value="2023-05-29" required><br><br>
                
                <label>Organization Name:</label>
                <input type="text" name="cell_name" value="RRECL" required><br><br>
                
                <label>Address Line 1:</label>
                <input type="text" name="address_line1" value="Test Address" required><br><br>
                
                <input type="hidden" name="selected_template" value="1">
                
                <button type="submit" style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px;">
                    Test Generate Report
                </button>
            </form>
            
            <script>
            document.querySelector('form').addEventListener('submit', function() {
                console.log('Test form submitted');
                document.querySelector('button').innerHTML = 'Generating...';
            });
            </script>
        </body>
        </html>
        '''

    @app.route('/charts')
    def chart_demo():
        """Chart demo page (for future use)."""
        return render_template('chart_demo.html')

    @app.route('/download/<filename>')
    def download_file(filename):
        """Download generated document."""
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

    @app.route('/generate', methods=['POST'])
    def generate_report():
        """Generate the Word document based on form data."""
        try:
            print("🎯 Generate route accessed")
            print(f"📝 Form data received: {dict(request.form)}")
            
            # Get the selected template number
            selected_template = request.form.get('selected_template', '1')
            organization = request.form.get('cell_name', 'Unknown')
            
            print(f"DEBUG: Selected template: {selected_template}")
            print(f"DEBUG: Organization: {organization}")
            print(f"DEBUG: All form data keys: {list(request.form.keys())}")
            
            # Map template numbers to file names
            template_mapping = {
                '1': 'word_template_1.docx',  # RRECL
                '2': 'word_template_2.docx',  # GEDA
                '3': 'word_template_3.docx',  # HAREDA
                '4': 'word_template_4.docx',  # UREDA
                '5': 'word_template_5.docx'   # SDA Odisha
            }
            
            # Get the template file name
            template_file = template_mapping.get(selected_template, 'word_template_1.docx')
            
            print(f"DEBUG: Using template file: {template_file}")
            
            # Check if template file exists
            if not os.path.exists(template_file):
                return f"Error: Template file '{template_file}' not found. Please ensure all template files are present.", 400
            
            # Load the Word template
            doc = Document(template_file)

            # Process uploaded logos
            logo1_path = save_uploaded_file(request.files.get('logo1'))
            logo2_path = save_uploaded_file(request.files.get('logo2'))

            # Process form data
            text_replacements = process_form_data(request)
            
            # Apply text replacements
            for placeholder, value in text_replacements.items():
                if value:
                    find_and_replace_text(doc, placeholder, value)

            # Process and insert logo images
            if logo1_path:
                find_and_replace_image(doc, '{{LOGO_1}}', logo1_path, width=Inches(1.5))
            if logo2_path:
                find_and_replace_image(doc, '{{LOGO_2}}', logo2_path, width=Inches(1.5))

            # Process gallery images
            gallery_images_clean, gallery_captions_clean = process_gallery_images(request)
            
            # Insert the gallery table if images exist
            if gallery_images_clean:
                insert_gallery_table(doc, gallery_images_clean, gallery_captions_clean)

            # Process annexure images
            annexure_placeholders = [
                ('annexure1', '{{ANNEXURE1_TABLE}}'),
                ('annexure2', '{{ANNEXURE2_TABLE}}'),
                ('annexure3', '{{ANNEXURE3_TABLE}}'),
                ('annexure4', '{{ANNEXURE4_TABLE}}'),
                ('annexure5', '{{ANNEXURE5_TABLE}}'),
            ]

            for prefix, placeholder in annexure_placeholders:
                images, captions = get_annexure_images_and_captions(prefix, request)
                if images:
                    insert_annexure_images(doc, images, captions, placeholder, 
                                         image_width=Cm(12), image_height=Cm(20))

            # Generate output filename
            event_date = request.form.get('event_date', '').replace('-', '')
            cell_name = request.form.get('cell_name', '').replace(' ', '_')
            filename = f"{event_date}_{cell_name}_report.docx"
            output_path = os.path.join(Config.OUTPUT_FOLDER, filename)
            
            # Save the document
            doc.save(output_path)
            
            # After successful generation, redirect to success page
            return redirect(url_for('success', filename=os.path.basename(output_path)))
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return render_template('error.html', error=str(e))

    @app.route('/success')
    def success():
        """Display success page with download option."""
        filename = request.args.get('filename')
        if not filename:
            return redirect(url_for('index'))
        
        return render_template('success.html', filename=filename)


# Create Flask application instance
app = create_app()


@app.route('/')
def index():
    """Main page with the form."""
    print("📋 Index page accessed")
    return render_template('index.html')


@app.route('/test')
def test():
    """Test route to verify server is working."""
    return "Server is working! ✅"


@app.route('/test-form')
def test_form():
    """Simple test form to verify form submission."""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Test Form</title></head>
    <body>
        <h2>Test Form Submission</h2>
        <form action="/generate" method="post" enctype="multipart/form-data">
            <label>Organization:</label>
            <select name="cell_name" required>
                <option value="RRECL">RRECL</option>
            </select><br><br>
            
            <label>Event Title:</label>
            <input type="text" name="event_title" value="Test Event" required><br><br>
            
            <label>Event Details:</label>
            <input type="text" name="event_details_line1" value="Test Details" required><br><br>
            
            <label>Event Date:</label>
            <input type="date" name="event_date" value="2023-05-29" required><br><br>
            
            <label>Address Line 1:</label>
            <input type="text" name="address_line1" value="Test Address" required><br><br>
            
            <input type="hidden" name="selected_template" value="1">
            
            <button type="submit" style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px;">
                Test Generate Report
            </button>
        </form>
        
        <script>
        document.querySelector('form').addEventListener('submit', function() {
            console.log('Test form submitted');
            document.querySelector('button').innerHTML = 'Generating...';
        });
        </script>
    </body>
    </html>
    '''


@app.route('/charts')
def chart_demo():
    """Chart demo page (for future use)."""
    return render_template('chart_demo.html')


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated document."""
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


# Update the generate route to redirect to success page
@app.route('/generate', methods=['POST'])
def generate_report():
    """Generate the Word document based on form data."""
    try:
        print("🎯 Generate route accessed")
        print(f"📝 Form data received: {dict(request.form)}")
        
        # Get the selected template number
        selected_template = request.form.get('selected_template', '1')
        organization = request.form.get('cell_name', 'Unknown')
        
        print(f"DEBUG: Selected template: {selected_template}")
        print(f"DEBUG: Organization: {organization}")
        print(f"DEBUG: All form data keys: {list(request.form.keys())}")
        
        # Map template numbers to file names
        template_mapping = {
            '1': 'word_template_1.docx',  # RRECL
            '2': 'word_template_2.docx',  # GEDA
            '3': 'word_template_3.docx',  # HAREDA
            '4': 'word_template_4.docx',  # UREDA
            '5': 'word_template_5.docx'   # SDA Odisha
        }
        
        # Get the template file name
        template_file = template_mapping.get(selected_template, 'word_template_1.docx')
        
        print(f"DEBUG: Using template file: {template_file}")
        
        # Check if template file exists
        if not os.path.exists(template_file):
            return f"Error: Template file '{template_file}' not found. Please ensure all template files are present.", 400
        
        # Load the Word template
        doc = Document(template_file)

        # Process uploaded logos
        logo1_path = save_uploaded_file(request.files.get('logo1'))
        logo2_path = save_uploaded_file(request.files.get('logo2'))

        # Process form data
        text_replacements = process_form_data(request)
        
        # Apply text replacements
        for placeholder, value in text_replacements.items():
            if value:
                find_and_replace_text(doc, placeholder, value)

        # Process and insert logo images
        if logo1_path:
            find_and_replace_image(doc, '{{LOGO_1}}', logo1_path, width=Inches(1.5))
        if logo2_path:
            find_and_replace_image(doc, '{{LOGO_2}}', logo2_path, width=Inches(1.5))

        # Process gallery images
        gallery_images_clean, gallery_captions_clean = process_gallery_images(request)
        
        # Insert the gallery table if images exist
        if gallery_images_clean:
            insert_gallery_table(doc, gallery_images_clean, gallery_captions_clean)

        # Process annexure images
        annexure_placeholders = [
            ('annexure1', '{{ANNEXURE1_TABLE}}'),
            ('annexure2', '{{ANNEXURE2_TABLE}}'),
            ('annexure3', '{{ANNEXURE3_TABLE}}'),
            ('annexure4', '{{ANNEXURE4_TABLE}}'),
            ('annexure5', '{{ANNEXURE5_TABLE}}'),
        ]

        for prefix, placeholder in annexure_placeholders:
            images, captions = get_annexure_images_and_captions(prefix, request)
            if images:
                insert_annexure_images(doc, images, captions, placeholder, 
                                     image_width=Cm(12), image_height=Cm(20))

        # Generate output filename
        event_date = request.form.get('event_date', '').replace('-', '')
        cell_name = request.form.get('cell_name', '').replace(' ', '_')
        filename = f"{event_date}_{cell_name}_report.docx"
        output_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        
        # Save the document
        doc.save(output_path)
        
        # After successful generation, redirect to success page
        return redirect(url_for('success', filename=os.path.basename(output_path)))
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return render_template('error.html', error=str(e))


@app.route('/success')
def success():
    """Display success page with download option."""
    filename = request.args.get('filename')
    if not filename:
        return redirect(url_for('index'))
    
    return render_template('success.html', filename=filename)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
