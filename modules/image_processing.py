"""
Image Processing Utilities Module
================================

FUNCTION: Specialized utilities for handling gallery and annexure images in Word documents.

RESPONSIBILITIES:
- Gallery image table creation with multiple images per row
- Annexure image processing and insertion
- Image caption management
- Form data extraction for image-related fields
- Image layout and positioning in document tables
- Page break insertion after image sections

KEY FUNCTIONS:
- insert_gallery_table(): Creates photo gallery tables with images and captions
- get_annexure_images_and_captions(): Extracts annexure data from form
- insert_annexure_images(): Inserts annexure sections with proper formatting

FEATURES:
- Configurable images per row in gallery tables
- Automatic image resizing to specified dimensions
- Caption text placement below images
- Support for multiple annexure sections (Annexure I, II, III, etc.)
- Proper table cell formatting and structure
- Page break management after image sections

Image processing utilities for gallery and annexure images.
"""
from docx.shared import Inches, Pt, Cm
import docx
import docx.oxml.shared
from .document_utils import insert_paragraph_after, insert_table_after, save_uploaded_file


def insert_gallery_table(doc, images, captions, images_per_row=2, image_width=Inches(2.5), placeholder='{{GALLERY_TABLE}}'):
    """
    Inserts a table at the given placeholder with images and captions.
    Each row has images_per_row images.
    """
    for para in doc.paragraphs:
        if placeholder in para.text:
            # Remove placeholder text
            para.text = para.text.replace(placeholder, '')
            
            num_images = len(images)
            if num_images == 0:
                return  # No images to insert
                
            # Calculate number of rows needed
            num_rows = (num_images + images_per_row - 1) // images_per_row
            
            # Insert table after the placeholder paragraph
            table = insert_table_after(para, num_rows, images_per_row)
            
            # Insert images and captions into the table
            img_idx = 0
            for row in table.rows:
                for cell in row.cells:
                    if img_idx < num_images and images[img_idx]:
                        # Clear cell and add image
                        cell.text = ''
                        p_img = cell.paragraphs[0]
                        run = p_img.add_run()
                        run.add_picture(images[img_idx], width=image_width)
                        
                        # Add caption if exists
                        if captions[img_idx]:
                            p_caption = cell.add_paragraph(captions[img_idx])
                            p_caption.alignment = 1  # Center alignment
                            p_caption.runs[0].font.size = Pt(10)
                        
                        img_idx += 1
            
            # Insert page break after the table by finding the table's parent and adding a paragraph
            # Get the table element and insert a paragraph after it
            table_element = table._element
            parent = table_element.getparent()
            new_para_element = docx.oxml.shared.OxmlElement('w:p')
            new_run_element = docx.oxml.shared.OxmlElement('w:r')
            new_break_element = docx.oxml.shared.OxmlElement('w:br')
            new_break_element.set(docx.oxml.shared.qn('w:type'), 'page')
            new_run_element.append(new_break_element)
            new_para_element.append(new_run_element)
            parent.insert(parent.index(table_element) + 1, new_para_element)
            return


def get_annexure_images_and_captions(prefix, request):
    """Get annexure images and captions from form data."""
    images = []
    captions = []
    i = 1
    while True:
        img = save_uploaded_file(request.files.get(f'{prefix}_image_{i}'))
        cap = request.form.get(f'{prefix}_caption_{i}', '')
        if not img:
            break
        images.append(img)
        captions.append(cap)
        i += 1
    return images, captions


def insert_annexure_images(doc, images, captions, placeholder, image_width=Cm(26), image_height=Cm(20)):
    """
    Inserts each image (with caption) at the given placeholder, one per paragraph, sized to fit within page margins.
    Always inserts a page break after the last annexure image.
    """
    for para in doc.paragraphs:
        if placeholder in para.text:
            para.text = para.text.replace(placeholder, '')
            insert_after = para
            for i, img_path in enumerate(images):
                # Insert image
                p_img = insert_paragraph_after(insert_after)
                run = p_img.add_run()
                run.add_picture(img_path, width=image_width, height=image_height)
                # Insert caption if present
                if captions[i]:
                    p_cap = insert_paragraph_after(p_img)
                    p_cap.add_run(captions[i])
                    p_cap.paragraph_format.alignment = 1  # Center
                    p_cap.runs[0].font.size = Pt(10)
                    insert_after = p_cap
                else:
                    insert_after = p_img
                # Page break after each image except the last
                if i < len(images) - 1:
                    p_break = insert_paragraph_after(insert_after)
                    p_break.add_run().add_break(docx.text.run.WD_BREAK.PAGE)
                    insert_after = p_break
            # Always insert a page break after the last annexure image/caption
            final_break = insert_paragraph_after(insert_after)
            final_break.add_run().add_break(docx.text.run.WD_BREAK.PAGE)
            break  # Only replace the first occurrence
