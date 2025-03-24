document.addEventListener("DOMContentLoaded", function () {
	const sections = ["applicant-data", "family-data", "application-submission"];
	let currentSectionIndex = 0;
	let householdMembers = [];
	let memberIdCounter = 1;

	// Function to show the current section
	function showCurrentSection() {
		// Hide all sections
		document.querySelectorAll(".form-section").forEach((section) => {
			section.classList.add("hidden");
		});

		// Show the current section
		document.getElementById(sections[currentSectionIndex]).classList.remove("hidden");

		// Update navigation buttons
		document.querySelectorAll(".nav-button").forEach((button) => {
			button.classList.remove("bg-blue-500", "text-white");
			button.classList.add("bg-gray-200", "text-gray-700");
		});

		const activeButton = document.querySelector(`.nav-button[data-section="${sections[currentSectionIndex]}"]`);
		if (activeButton) {
			activeButton.classList.remove("bg-gray-200", "text-gray-700");
			activeButton.classList.add("bg-blue-500", "text-white");
		}

		// Update prev/next buttons
		document.getElementById("prev-button").disabled = currentSectionIndex === 0;
		document.getElementById("prev-button").style.opacity = currentSectionIndex === 0 ? "0.5" : "1";

		// Update next button text on last section
		const nextButton = document.getElementById("next-button");
		if (currentSectionIndex === sections.length - 1) {
			nextButton.textContent = "Отправить";
		} else {
			nextButton.textContent = "Далее";
		}
	}

	// Initialize section navigation buttons
	document.querySelectorAll(".nav-button").forEach((button) => {
		button.addEventListener("click", function () {
			const sectionId = this.getAttribute("data-section");
			currentSectionIndex = sections.indexOf(sectionId);
			showCurrentSection();
		});
	});

	// Next button click handler
	document.getElementById("next-button").addEventListener("click", function () {
		if (currentSectionIndex < sections.length - 1) {
			currentSectionIndex++;
			showCurrentSection();
		} else {
			// This is the last section, handle form submission
			handleFormSubmission();
		}
	});

	// Previous button click handler
	document.getElementById("prev-button").addEventListener("click", function () {
		if (currentSectionIndex > 0) {
			currentSectionIndex--;
			showCurrentSection();
		}
	});

	// Handle cancel button
	document.getElementById("cancel-button").addEventListener("click", function () {
		if (confirm("Вы уверены, что хотите отменить? Все несохраненные данные будут потеряны.")) {
			window.location.href = "/"; // Redirect to home page
		}
	});

	// Toggle disability details based on checkbox
	const disabilityCheckbox = document.querySelector('input[name="has_disability"]');
	const disabilityDetails = document.querySelector('input[name="applicant_disability"]');

	if (disabilityCheckbox && disabilityDetails) {
		disabilityCheckbox.addEventListener("change", function () {
			const detailsGroup = disabilityDetails.closest(".form-group");
			if (this.checked) {
				detailsGroup.classList.remove("hidden");
			} else {
				detailsGroup.classList.add("hidden");
				disabilityDetails.value = "";
			}
		});

		// Initialize on page load
		if (!disabilityCheckbox.checked) {
			disabilityDetails.closest(".form-group").classList.add("hidden");
		}
	}

	// Function to update application summary
	function updateApplicationSummary() {
		const status = "-"; // Default
		const priorityScore = "-"; // Default
		const queuePosition = "-"; // Default

		document.getElementById("summary-status").textContent = status;
		document.getElementById("summary-priority-score").textContent = priorityScore;
		document.getElementById("summary-queue-position").textContent = queuePosition;
	}

	// Update summary when navigating to the summary page
	document
		.querySelector(`.nav-button[data-section="application-submission"]`)
		.addEventListener("click", updateApplicationSummary);

	// Handle form submission (placeholder)
	// function handleFormSubmission() {
	// 	const confirmCheckbox = document.querySelector('[name="confirm_submission"]');

	// 	if (!confirmCheckbox.checked) {
	// 		alert("Пожалуйста, подтвердите, что вся информация верна и полна.");
	// 		return;
	// 	}

	// 	// Here you would typically submit the form data via AJAX
	// 	alert("Форма успешно отправлена!");
	// 	// For demonstration purposes only:
	// 	// window.location.href = '/application-confirmation/';
	// }

	// Function to handle showing/hiding dependent fields
	function setupDependentFields() {
		// Example: toggle homelessness details
		const homelessCheckbox = document.querySelector('[name="is_homeless"]');
		const addressField = document.querySelector('[name="current_address"]');

		if (homelessCheckbox && addressField) {
			homelessCheckbox.addEventListener("change", function () {
				const addressGroup = addressField.closest(".form-group");
				const livingAreaField = document.querySelector('[name="current_living_area"]');
				const livingAreaGroup = livingAreaField?.closest(".form-group");

				if (this.checked) {
					addressField.value = "Без определенного места жительства";
					addressField.readOnly = true;

					if (livingAreaField) {
						livingAreaField.value = "0";
						livingAreaGroup.classList.add("opacity-50");
						livingAreaField.readOnly = true;
					}
				} else {
					addressField.value = "";
					addressField.readOnly = false;

					if (livingAreaField) {
						livingAreaField.value = "";
						livingAreaGroup.classList.remove("opacity-50");
						livingAreaField.readOnly = false;
					}
				}
			});
		}
	}

	// Household Member Modal Functions
	const modal = document.getElementById("member-modal");
	const addMemberBtn = document.getElementById("add-member-button");
	const closeModalBtn = document.getElementById("close-modal");
	const cancelMemberBtn = document.getElementById("cancel-member");
	const memberForm = document.getElementById("member-form");
	const memberDisability = document.getElementById("member-disability");
	const disabilityDocGroup = document.getElementById("disability-document-group");
	const birthCertificateGroup = document.getElementById("birth-certificate-group");
	const memberRelationship = document.getElementById("member-relationship");

	// Show modal when add member button is clicked
	addMemberBtn.addEventListener("click", function () {
		modal.classList.remove("hidden");
		document.getElementById("member-id").value = ""; // Clear ID for new member
		memberForm.reset();
		updateDisabilityDocVisibility();
		updateBirthCertificateVisibility();
	});

	// Close modal
	function closeModal() {
		modal.classList.add("hidden");
	}

	closeModalBtn.addEventListener("click", closeModal);
	cancelMemberBtn.addEventListener("click", closeModal);

	// Close modal if clicked outside the content
	modal.addEventListener("click", function (e) {
		if (e.target === modal) {
			closeModal();
		}
	});

	// Toggle disability document visibility based on checkbox
	memberDisability.addEventListener("change", updateDisabilityDocVisibility);

	function updateDisabilityDocVisibility() {
		if (memberDisability.checked) {
			disabilityDocGroup.classList.remove("hidden");
			document.getElementById("document-disability").required = true;
		} else {
			disabilityDocGroup.classList.add("hidden");
			document.getElementById("document-disability").required = false;
		}
	}

	// Toggle birth certificate visibility based on relationship
	memberRelationship.addEventListener("change", updateBirthCertificateVisibility);

	function updateBirthCertificateVisibility() {
		if (memberRelationship.value === "CHILD") {
			birthCertificateGroup.classList.remove("hidden");
			document.getElementById("document-birth").required = true;
		} else {
			birthCertificateGroup.classList.add("hidden");
			document.getElementById("document-birth").required = false;
		}
	}

	// Handle member form submission
	memberForm.addEventListener("submit", function (e) {
		e.preventDefault();

		const memberId = document.getElementById("member-id").value || memberIdCounter++;
		const name = document.getElementById("member-name").value;
		const birthdate = document.getElementById("member-birthdate").value;
		const relationship = document.getElementById("member-relationship").value;
		const hasDisability = document.getElementById("member-disability").checked;

		// Get relationship display text
		const relationshipText = memberRelationship.options[memberRelationship.selectedIndex].text;

		// Document information (in a real application, you would upload these files)
		const idDoc = document.getElementById("document-id").value ? "✓" : "✗";
		const birthDoc = document.getElementById("document-birth").value ? "✓" : "—";
		const disabilityDoc = hasDisability ? (document.getElementById("document-disability").value ? "✓" : "✗") : "—";

		// Prepare member data
		const memberData = {
			id: memberId,
			name: name,
			birthdate: birthdate,
			relationship: relationship,
			relationshipText: relationshipText,
			hasDisability: hasDisability,
			documents: {
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

	// Function to update the members table
	function updateMembersTable() {
		const tableBody = document.getElementById("household-members-list");

		// Clear current table
		tableBody.innerHTML = "";

		if (householdMembers.length === 0) {
			tableBody.innerHTML = `
					<tr class="text-center text-gray-500">
						<td colspan="6" class="border p-4">Нет добавленных членов семьи</td>
					</tr>
				`;
			return;
		}

		// Add each member to the table
		householdMembers.forEach((member) => {
			const row = document.createElement("tr");

			row.innerHTML = `
					<td class="border p-2">${member.name}</td>
					<td class="border p-2">${formatDate(member.birthdate)}</td>
					<td class="border p-2">${member.relationshipText}</td>
					<td class="border p-2">${member.hasDisability ? "Да" : "Нет"}</td>
					<td class="border p-2">
						<div>ID: ${member.documents.id}</div>
						${member.relationship === "CHILD" ? `<div>Birth: ${member.documents.birth}</div>` : ""}
						${member.hasDisability ? `<div>Disability: ${member.documents.disability}</div>` : ""}
					</td>
					<td class="border p-2">
						<div class="flex space-x-2">
							<button class="edit-member text-blue-500 hover:text-blue-700" data-id="${member.id}">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
								</svg>
							</button>
							<button class="delete-member text-red-500 hover:text-red-700" data-id="${member.id}">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
								</svg>
							</button>
						</div>
					</td>
				`;

			tableBody.appendChild(row);
		});

		// Add event listeners for edit and delete buttons
		document.querySelectorAll(".edit-member").forEach((button) => {
			button.addEventListener("click", function () {
				const memberId = this.getAttribute("data-id");
				editMember(memberId);
			});
		});

		document.querySelectorAll(".delete-member").forEach((button) => {
			button.addEventListener("click", function () {
				const memberId = this.getAttribute("data-id");
				deleteMember(memberId);
			});
		});
	}

	// Function to format date for display
	function formatDate(dateString) {
		const date = new Date(dateString);
		return date.toLocaleDateString();
	}

	// Function to edit a member
	function editMember(memberId) {
		const member = householdMembers.find((m) => m.id == memberId);
		if (!member) return;

		// Fill form with member data
		document.getElementById("member-id").value = member.id;
		document.getElementById("member-name").value = member.name;
		document.getElementById("member-birthdate").value = member.birthdate;
		document.getElementById("member-relationship").value = member.relationship;
		document.getElementById("member-disability").checked = member.hasDisability;

		// Update visibility of document fields
		updateDisabilityDocVisibility();
		updateBirthCertificateVisibility();

		// Open modal
		modal.classList.remove("hidden");
	}

	// Function to delete a member
	function deleteMember(memberId) {
		if (confirm("Вы уверены, что хотите удалить этого члена семьи?")) {
			householdMembers = householdMembers.filter((m) => m.id != memberId);
			updateMembersTable();
		}
	}

	setupDependentFields();
	showCurrentSection(); // Initialize the first section
});
