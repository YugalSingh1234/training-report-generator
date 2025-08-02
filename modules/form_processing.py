"""
Form Data Processing Utilities Module
====================================

FUNCTION: Processes and structures form data from the web interface for document generation.

RESPONSIBILITIES:
- Dynamic person list processing (RRECL people, guest trainers, chief guests)
- Form data extraction and validation
- Text placeholder mapping and preparation
- Gallery image data processing
- Address field combination and formatting
- Data structure preparation for document replacement

KEY FUNCTIONS:
- combine_person_list(): Formats person data with prefixes, names, and designations
- process_form_data(): Main form processing function that returns all text replacements
- process_gallery_images(): Handles gallery image uploads and captions

DATA PROCESSING:
- Combines multiple form fields into formatted strings
- Creates placeholder-to-value mappings for document replacement
- Handles dynamic person lists with proper formatting
- Processes image uploads with caption pairing
- Validates and cleans form input data

OUTPUT FORMAT:
- Returns dictionary of {placeholder: value} pairs
- Handles empty/None values appropriately
- Formats person lists as comma-separated strings with proper titles

Form data processing utilities.
"""


def combine_person_list(prefixes, names, designations):
    """Combine person data into formatted strings."""
    people = []
    for p, n, d in zip(prefixes, names, designations):
        if n.strip():
            entry = f"{p} {n.strip()}"
            if d.strip():
                entry += f" ({d.strip()})"
            people.append(entry)
    return ', '.join(people)


def process_form_data(request):
    """Process all form data and return structured data."""
    # Dynamic Person Lists
    rrecl_people = combine_person_list(
        request.form.getlist('rrecl_prefix[]'),
        request.form.getlist('rrecl_name[]'),
        request.form.getlist('rrecl_designation[]')
    )
    guest_trainers = combine_person_list(
        request.form.getlist('guest_prefix[]'),
        request.form.getlist('guest_name[]'),
        request.form.getlist('guest_designation[]')
    )
    chief_guests = combine_person_list(
        request.form.getlist('chief_prefix[]'),
        request.form.getlist('chief_name[]'),
        request.form.getlist('chief_designation[]')
    )
    guidance_person = combine_person_list(
        request.form.getlist('guidance_prefix[]'),
        request.form.getlist('guidance_name[]'),
        request.form.getlist('guidance_designation[]')
    )

    # Text replacements
    text_replacements = {
        '{{EVENT_TITLE}}': request.form.get('event_title'),
        '{{EVENT_DETAILS}}': request.form.get('event_details_line1'),
        '{{EVENT_DATE}}': request.form.get('event_date'),
        '{{ADDRESS}}': '\n'.join([
            request.form.get('address_line1', ''),
            request.form.get('address_line2', ''),
            request.form.get('address_line3', '')
        ]).strip(),
        '{{RRECL_PEOPLE}}': rrecl_people,
        '{{WORKSHOP_TYPE}}': request.form.get('workshop_type'),
        '{{GUEST_TRAINERS}}': guest_trainers,
        '{{ORGANIZER}}': request.form.get('organizer'),
        '{{VENUE}}': request.form.get('venue'),
        '{{DATETIME}}': request.form.get('date', ''),
        '{{CELL_NAME}}': request.form.get('cell_name'),
        '{{CHIEF_GUESTS}}': chief_guests,
        '{{GUIDANCE_PERSON}}': guidance_person
    }
    
    return text_replacements


def process_gallery_images(request):
    """Process gallery images and captions."""
    from .document_utils import save_uploaded_file
    
    gallery_images = [save_uploaded_file(request.files.get(f'gallery_image_{i}')) for i in range(1, 11)]
    gallery_captions = [request.form.get(f'gallery_caption_{i}', '') for i in range(1, 11)]

    # Remove empty images/captions (keep pairs)
    gallery_pairs = [(img, cap) for img, cap in zip(gallery_images, gallery_captions) if img]
    gallery_images_clean = [img for img, _ in gallery_pairs]
    gallery_captions_clean = [cap for _, cap in gallery_pairs]
    
    return gallery_images_clean, gallery_captions_clean
