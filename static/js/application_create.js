document.addEventListener("DOMContentLoaded", function () {
    let householdMembers = [];
    let memberIdCounter = 1;
	const memberForm = document.getElementById("member-form");
	const memberRelationship = document.getElementById("member-relationship");

    // Modified form submission function
    function handleFormSubmission() {
        const confirmCheckbox = document.querySelector('[name="confirm_submission"]');

        if (!confirmCheckbox.checked) {
            alert("Пожалуйста, подтвердите, что вся информация верна и полна.");
            return;
        }

        // Collect all form data
        const formData = new FormData();

        // Applicant data
        formData.append("full_name", document.querySelector('[name="full_name"]').value);
        formData.append(
            "current_residence_condition",
            document.querySelector('[name="current_residence_condition"]').value
        );
        formData.append("monthly_income", document.querySelector('[name="monthly_income"]').value);
        formData.append("current_living_area", document.querySelector('[name="current_living_area"]').value);
        formData.append("current_address", document.querySelector('[name="current_address"]').value);
        formData.append("is_homeless", document.querySelector('[name="is_homeless"]').checked);

        // Family data
        formData.append("is_single_parent", document.querySelector('[name="is_single_parent"]').checked);
        formData.append("is_veteran", document.querySelector('[name="is_veteran"]').checked);
        formData.append("has_disability", document.querySelector('[name="has_disability"]').checked);

        // If disability document exists, append it
        const applicantDisabilityFile = document.querySelector('input[name="applicant_disability"]')?.files[0];
        if (applicantDisabilityFile) {
            formData.append("applicant_disability", applicantDisabilityFile);
        }

        // Application submission
        formData.append("notes", document.querySelector('[name="notes"]').value);

        // Add all household members as JSON
        formData.append("household_members", JSON.stringify(householdMembers));

        // Create an object to store file references separately
        // We'll append these files with special keys that Django can recognize
        const memberFiles = {};

        // Collect all household member files
        householdMembers.forEach((member, index) => {
            // For each member, we need to find their files in the DOM and append them to formData
            // We'll use a naming convention like member_1_document_id, member_1_document_birth, etc.
            if (member.files) {
                Object.entries(member.files).forEach(([docType, file]) => {
                    if (file instanceof File) {
                        const fileKey = `member_${index}_document_${docType}`;
                        formData.append(fileKey, file);
                        // Store the reference to this file in our member data
                        if (!memberFiles[index]) memberFiles[index] = {};
                        memberFiles[index][docType] = fileKey;
                    }
                });
            }
        });

        // Add the file references to the formData as well
        formData.append("member_files", JSON.stringify(memberFiles));

        // Get CSRF token from cookies
        const csrftoken = getCookie("csrftoken");

        // Submit form using fetch API
        fetch("/my-application/submit/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                console.log(response.json())
                return response.json();
            })
            .then((data) => {
                if (data.success) {
                    alert("Заявка успешно отправлена!");
                    window.location.href = `/application/confirmation/${data.application_number}/`;
                } else {
                    alert(`Ошибка: ${data.error}`);
                }
            })
            .catch((error) => {
                console.error("Error submitting application:", error);
                alert("Произошла ошибка при отправке заявки. Пожалуйста, попробуйте еще раз позже.");
            });
    }

    // Function to handle member form submission - modified to save file references
    memberForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const memberId = document.getElementById("member-id").value || memberIdCounter++;
        const name = document.getElementById("member-name").value;
        const birthdate = document.getElementById("member-birthdate").value;
        const relationship = document.getElementById("member-relationship").value;
        const hasDisability = document.getElementById("member-disability").checked;

        // Get relationship display text
        const relationshipText = memberRelationship.options[memberRelationship.selectedIndex].text;

        // Save actual file references
        const idDoc = document.getElementById("document-id").files[0];
        const birthDoc = document.getElementById("document-birth").files[0];
        const disabilityDoc = hasDisability ? document.getElementById("document-disability").files[0] : null;

        // Document information for display
        const idDocDisplay = idDoc ? "✓" : "✗";
        const birthDocDisplay = relationship === "CHILD" ? (birthDoc ? "✓" : "✗") : "—";
        const disabilityDocDisplay = hasDisability ? (disabilityDoc ? "✓" : "✗") : "—";

        // Prepare member data
        const memberData = {
            id: memberId,
            name: name,
            birthdate: birthdate,
            relationship: relationship,
            relationshipText: relationshipText,
            hasDisability: hasDisability,
            documents: {
                id: idDocDisplay,
                birth: birthDocDisplay,
                disability: disabilityDocDisplay,
            },
            // Store the actual files
            files: {
                id: idDoc,
                birth: birthDoc,
                disability: disabilityDoc,
            },
        };

        // Check if editing existing member or adding new one
        const existingIndex = householdMembers.findIndex((m) => m.id == memberId);
        if (existingIndex >= 0) {
            householdMembers[existingIndex] = memberData;
        } else {
            householdMembers.push(memberData);
        }

        // Update the table display
        updateMembersTable();

        // Close the modal
        closeModal();
    });

    // Helper function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Other existing code remains unchanged...
});
