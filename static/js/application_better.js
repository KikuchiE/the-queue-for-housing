// application_better.js
document.addEventListener('DOMContentLoaded', function() {
    // Form navigation
    const sections = document.querySelectorAll('.form-section');
    const navButtons = document.querySelectorAll('.nav-button');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const submitButton = document.getElementById('submit-button');
    const cancelButton = document.getElementById('cancel-button');
    
    let currentSectionIndex = 0;
    
    // Function to show current section
    function showSection(index) {
        sections.forEach((section, i) => {
            section.classList.toggle('hidden', i !== index);
            section.classList.toggle('active', i === index);
        });
        
        navButtons.forEach((button, i) => {
            button.classList.toggle('bg-blue-500', i === index);
            button.classList.toggle('text-white', i === index);
            button.classList.toggle('bg-gray-200', i !== index);
            button.classList.toggle('text-gray-700', i !== index);
        });
        
        // Update navigation buttons
        prevButton.classList.toggle('hidden', index === 0);
        nextButton.classList.toggle('hidden', index === sections.length - 1);
        submitButton.classList.toggle('hidden', index !== sections.length - 1);
        
        currentSectionIndex = index;
    }
    
    // Set up navigation button listeners
    navButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            showSection(index);
        });
    });
    
    // Previous button
    prevButton.addEventListener('click', () => {
        if (currentSectionIndex > 0) {
            showSection(currentSectionIndex - 1);
        }
    });
    
    // Next button
    nextButton.addEventListener('click', () => {
        if (validateCurrentSection(currentSectionIndex)) {
            if (currentSectionIndex < sections.length - 1) {
                showSection(currentSectionIndex + 1);
            }
            
            // If moving to last section, try to get application summary
            if (currentSectionIndex === sections.length - 2) {
                fetchApplicationSummary();
            }
        } else {
            alert('Please fill in all required fields before proceeding.');
        }
    });
    
    // Cancel button
    cancelButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to cancel? Your changes will not be saved.')) {
            window.location.href = '/dashboard/';
        }
    });
    
    // Form validation
    function validateCurrentSection(sectionIndex) {
        const currentSection = sections[sectionIndex];
        const requiredFields = currentSection.querySelectorAll('input[required], select[required], textarea[required]');
        
        for (const field of requiredFields) {
            if (!field.value.trim()) {
                field.focus();
                return false;
            }
        }
        
        // Special case: if has_disability is checked, ensure document is uploaded or details provided
        if (sectionIndex === 1) { // Family section
            const hasDisabilityCheckbox = document.getElementById('id_has_disability');
            if (hasDisabilityCheckbox && hasDisabilityCheckbox.checked) {
                const disabilityDocument = document.getElementById('id_disability_document');
                const disabilityDetails = document.getElementById('id_disability_details');
                
                if ((!disabilityDocument || !disabilityDocument.files || !disabilityDocument.files.length) && 
                    (!disabilityDetails || !disabilityDetails.value.trim())) {
                    alert('Please provide either a disability document or details about the disability.');
                    return false;
                }
            }
        }
        
        return true;
    }
    
    // Toggle disability document and details based on checkbox
    // const disabilityCheckbox = document.getElementById('id_has_disability');
    // const disabilityDocDiv = document.getElementById('disability-document-div');
    // const disabilityDetailsDiv = document.getElementById('disability-details-div');
    
    // if (disabilityCheckbox && disabilityDocDiv && disabilityDetailsDiv) {
    //     function updateDisabilityFields() {
    //         disabilityDocDiv.style.display = disabilityCheckbox.checked ? 'block' : 'none';
    //         disabilityDetailsDiv.style.display = disabilityCheckbox.checked ? 'block' : 'none';
    //     }
        
    //     updateDisabilityFields();
    //     disabilityCheckbox.addEventListener('change', updateDisabilityFields);
    // }
    
    // Initialize form validation on submit
    const form = document.getElementById('application-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Validate last section
            if (!validateCurrentSection(sections.length - 1)) {
                e.preventDefault();
                return false;
            }
            
            // Double-check the confirm checkbox
            const confirmCheckbox = document.getElementById('id_confirm_submission');
            if (!confirmCheckbox || !confirmCheckbox.checked) {
                alert('Please confirm that the information is accurate and complete.');
                e.preventDefault();
                return false;
            }
            
            return true;
        });
    }
});