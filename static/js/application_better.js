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
        // Simplified validation - could be enhanced as needed
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
    
    // Fetch application summary for the final section (if available)
    function fetchApplicationSummary() {
        // This would typically be an AJAX call to get current application data
        // For now, let's just populate with sample data
        document.getElementById('summary-application-number').textContent = 'APP000123';
        document.getElementById('summary-status').textContent = 'SUBMITTED';
        document.getElementById('summary-priority-score').textContent = 'Calculating...';
        document.getElementById('summary-queue-position').textContent = 'N/A';
        
        // In a real implementation, you'd make an AJAX call like:
        /*
        fetch('/api/application-summary/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('summary-application-number').textContent = data.application_number;
                document.getElementById('summary-status').textContent = data.status;
                document.getElementById('summary-priority-score').textContent = data.priority_score;
                document.getElementById('summary-queue-position').textContent = data.queue_position;
                
                // Populate history table
                const historyTable = document.getElementById('history-table');
                if (data.history && data.history.length > 0) {
                    historyTable.innerHTML = '';
                    data.history.forEach(entry => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td class="border p-2">${entry.change_date}</td>
                            <td class="border p-2">${entry.previous_status}</td>
                            <td class="border p-2">${entry.new_status}</td>
                            <td class="border p-2">${entry.changed_by}</td>
                        `;
                        historyTable.appendChild(row);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching application summary:', error);
            });
        */
    }
    
    // Handle special fields dependencies
    
    // Toggle disability document and details based on checkbox
    const disabilityCheckbox = document.getElementById('id_has_disability');
    const disabilityDocDiv = document.getElementById('disability-document-div');
    const disabilityDetailsDiv = document.getElementById('disability-details-div');
    
    if (disabilityCheckbox && disabilityDocDiv && disabilityDetailsDiv) {
        function updateDisabilityFields() {
            disabilityDocDiv.style.display = disabilityCheckbox.checked ? 'block' : 'none';
            disabilityDetailsDiv.style.display = disabilityCheckbox.checked ? 'block' : 'none';
        }
        
        updateDisabilityFields(); // Initial state
        disabilityCheckbox.addEventListener('change', updateDisabilityFields);
    }
    
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