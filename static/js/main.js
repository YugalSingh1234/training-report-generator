// Training Report Generator - JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    const multiStepForm = document.getElementById('multiStepForm');
    const steps = [...document.querySelectorAll('.step')];
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    let currentStep = 0;

    // --- Multi-step Form Navigation ---
    function showStep(stepIndex) {
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === stepIndex);
        });
        
        // Update progress indicators
        updateProgressIndicators(stepIndex);
        
        // Update button visibility
        if (prevBtn) prevBtn.style.display = stepIndex === 0 ? 'none' : 'inline-block';
        if (nextBtn) nextBtn.style.display = stepIndex === steps.length - 1 ? 'none' : 'inline-block';
    }

    // Progress indicator updates
    function updateProgressIndicators(currentIndex) {
        const progressSteps = document.querySelectorAll('.progress-step');
        progressSteps.forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index < currentIndex) {
                step.classList.add('completed');
            } else if (index === currentIndex) {
                step.classList.add('active');
            }
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    }

    // Initialize first step
    showStep(0);

    // --- Form Submission Handling ---
    if (multiStepForm) {
        multiStepForm.addEventListener('submit', function(e) {
            console.log('🎯 Form submission attempted');
            
            // Check if all required fields are filled
            const requiredFields = document.querySelectorAll('input[required], select[required]');
            let missingFields = [];
            
            requiredFields.forEach(field => {
                if (!field.value || field.value.trim() === '') {
                    missingFields.push(field);
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (missingFields.length > 0) {
                e.preventDefault();
                
                // Go to step 1 to show missing fields
                if (currentStep !== 0) {
                    currentStep = 0;
                    showStep(currentStep);
                }
                
                // Focus on first missing field
                missingFields[0].focus();
                missingFields[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                alert(`Please fill in all required fields. Missing ${missingFields.length} field(s).`);
                return false;
            }
            
            // Show loading state
            const generateBtn = document.querySelector('button[type="submit"]');
            if (generateBtn) {
                generateBtn.innerHTML = '<span class="material-icons">hourglass_empty</span> Generating Report...';
                generateBtn.disabled = true;
            }
            
            // Show loading overlay
            showLoadingOverlay();
        });
    }

    function showLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <h3>Generating Your Report</h3>
                <p>Please wait while we process your training report...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    // --- Image Preview Functionality ---
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    // Helper function to add file input listeners
    function addFileInputListener(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const previewId = e.target.getAttribute('data-preview-id');
            const previewImg = document.getElementById(`preview_${previewId}`);
            const plusIcon = document.getElementById(`plus_${previewId}`);
            
            if (file && previewImg) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    previewImg.style.display = 'block';
                    if (plusIcon) plusIcon.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Initialize existing file inputs
    fileInputs.forEach(input => {
        addFileInputListener(input);
    });

    // --- Dynamic Image Management ---
    let galleryCount = 1;
    let annexureCounters = {
        annexure1: 1,
        annexure2: 1,
        annexure3: 1,
        annexure4: 1,
        annexure5: 1
    };

    // Add Gallery Image
    window.addGalleryImage = function() {
        galleryCount++;
        const galleryGrid = document.getElementById('gallery-grid');
        const newBox = document.createElement('div');
        newBox.className = 'gallery-box';
        newBox.innerHTML = `
            <button type="button" class="btn-remove-image" onclick="removeImageBox(this)">×</button>
            <label for="gallery_image_${galleryCount}" class="image-upload-label">
                <span id="plus_${galleryCount}" class="plus-icon">📸</span>
                <div class="upload-text">Gallery Image ${galleryCount}</div>
                <div class="upload-hint">Click to upload or drag & drop</div>
                <img id="preview_${galleryCount}" src="" alt="Image preview" class="preview-img">
            </label>
            <input type="file" id="gallery_image_${galleryCount}" name="gallery_image_${galleryCount}" accept="image/*" data-preview-id="${galleryCount}">
            <input type="text" name="gallery_caption_${galleryCount}" placeholder="Enter image caption" style="width:90%; margin-top:0.5em;">
        `;
        galleryGrid.appendChild(newBox);
        
        // Add event listener for the new file input
        const newInput = newBox.querySelector('input[type="file"]');
        addFileInputListener(newInput);
    };

    // Add Annexure Image
    window.addAnnexureImage = function(annexureType) {
        annexureCounters[annexureType]++;
        const count = annexureCounters[annexureType];
        const grid = document.getElementById(`${annexureType}-grid`);
        const newBox = document.createElement('div');
        newBox.className = 'gallery-box';
        newBox.innerHTML = `
            <button type="button" class="btn-remove-image" onclick="removeImageBox(this)">×</button>
            <label>${annexureType.charAt(0).toUpperCase() + annexureType.slice(1)} Image ${count}</label>
            <label for="${annexureType}_image_${count}" class="image-upload-label">
                <span id="plus_${annexureType}_${count}" class="plus-icon">+</span>
                <img id="preview_${annexureType}_${count}" src="" alt="Image preview" class="preview-img">
            </label>
            <input type="file" id="${annexureType}_image_${count}" name="${annexureType}_image_${count}" accept="image/*" data-preview-id="${annexureType}_${count}">
            <input type="text" name="${annexureType}_caption_${count}" placeholder="Enter image caption" style="width:90%; margin-top:0.5em;">
        `;
        grid.appendChild(newBox);
        
        // Add event listener for the new file input
        const newInput = newBox.querySelector('input[type="file"]');
        addFileInputListener(newInput);
    };

    // Remove Image Box
    window.removeImageBox = function(button) {
        button.closest('.gallery-box').remove();
    };

    // --- Dynamic Person Lists ---
    function initializePersonList(listId, prefix) {
        const list = document.getElementById(listId);
        if (!list) return;

        function createPersonRow(index) {
            const row = document.createElement('div');
            row.className = 'name-row';
            row.innerHTML = `
                <select name="${prefix}_prefix[]">
                    <option value="Mr.">Mr.</option>
                    <option value="Ms.">Ms.</option>
                    <option value="Dr.">Dr.</option>
                    <option value="Prof.">Prof.</option>
                    <option value="">None</option>
                </select>
                <input type="text" name="${prefix}_name[]" placeholder="Enter name" style="flex: 1;">
                <input type="text" name="${prefix}_designation[]" placeholder="Enter designation" style="flex: 1;">
                <button type="button" class="btn-dynamic btn-dynamic-remove" onclick="removePersonRow(this)">Remove</button>
            `;
            return row;
        }

        function addPersonRow() {
            const index = list.children.length + 1;
            const row = createPersonRow(index);
            list.appendChild(row);
        }

        // Add initial row and Add button
        addPersonRow();
        
        const addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.className = 'btn-dynamic btn-dynamic-add';
        addButton.textContent = `Add ${prefix.toUpperCase()} Person`;
        addButton.onclick = addPersonRow;
        
        list.parentNode.insertBefore(addButton, list.nextSibling);
    }

    // Global function for removing rows
    window.removePersonRow = function(button) {
        button.closest('.name-row').remove();
    };

    // Initialize person lists
    initializePersonList('rrecl-people-list', 'rrecl');
    initializePersonList('guest-people-list', 'guest');
    initializePersonList('chief-people-list', 'chief');
    initializePersonList('guidance-people-list', 'guidance');

    // --- Template Selection Functionality ---
    const cellSelect = document.getElementById('cell_name');
    const templateInfo = document.getElementById('template-info');
    const templateText = document.getElementById('template-text');

    if (cellSelect && templateInfo && templateText) {
        cellSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            
            if (this.value) {
                const templateNumber = selectedOption.getAttribute('data-template');
                const organizationName = this.value;
                
                templateText.textContent = `Using Template ${templateNumber} for ${organizationName}`;
                templateInfo.classList.add('show');
                templateInfo.style.display = 'flex';
                
                // Add hidden input for template selection
                let templateInput = document.getElementById('selected_template');
                if (!templateInput) {
                    templateInput = document.createElement('input');
                    templateInput.type = 'hidden';
                    templateInput.id = 'selected_template';
                    templateInput.name = 'selected_template';
                    cellSelect.parentNode.appendChild(templateInput);
                }
                templateInput.value = templateNumber;
            } else {
                templateInfo.classList.remove('show');
                templateInfo.style.display = 'none';
            }
        });
    }
});