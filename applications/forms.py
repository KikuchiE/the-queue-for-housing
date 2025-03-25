from django import forms
from .models import Application, ApplicationDocument

class ApplicantDataForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'current_residence_condition', 
            'monthly_income', 
            'current_living_area', 
            'current_address', 
            'is_homeless'
        ]
        widgets = {
            'current_address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'}),
            'current_residence_condition': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01'}),
            'current_living_area': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01'}),
            'is_homeless': forms.CheckboxInput(attrs={'class': 'mr-2'}),
        }

class FamilyDataForm(forms.ModelForm):
    applicant_disability = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'p-2 border rounded w-full'})
    )

    class Meta:
        model = Application
        fields = ['is_single_parent', 'is_veteran', 'has_disability', 'adults_count', 'children_count', 'elderly_count']
        widgets = {
            'is_single_parent': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'is_veteran': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'has_disability': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'adults_count': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'children_count': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'elderly_count': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        # Handle disability document upload if needed
        if self.cleaned_data.get('applicant_disability') and instance.has_disability:
            ApplicationDocument.objects.create(
                application=instance,
                document_type='DISABILITY_CERTIFICATE',
                file=self.cleaned_data['applicant_disability']
            )
        
        return instance
    
    
    
    
    
from django import forms
from .models import Application, ApplicationDocument

class ApplicantDataForm(forms.ModelForm):
    """Form for basic applicant data"""
    class Meta:
        model = Application
        fields = [
            'current_residence_condition',
            'monthly_income',
            'current_living_area',
            'current_address',
            'is_homeless',
        ]
        widgets = {
            'current_residence_condition': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'current_living_area': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'current_address': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3}),
            'is_homeless': forms.CheckboxInput(attrs={'class': 'mr-2'}),
        }


class FamilyDataForm(forms.ModelForm):
    """Form for family data and special status"""
    is_single_parent_document = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}))
    is_veteran_document = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}))
    disability_document = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}))
    
    class Meta:
        model = Application
        fields = [
            'is_single_parent',
            'is_veteran',
            'has_disability',
            'disability_details',
            'adults_count',
            'children_count',
            'elderly_count',
        ]
        widgets = {
            'is_single_parent': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'is_veteran': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'has_disability': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'disability_details': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3}),
            'adults_count': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 1}),
            'children_count': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
            'elderly_count': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
        }


class ApplicationSubmissionForm(forms.Form):
    """Form for application submission and notes"""
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'w-full p-2 border rounded',
        'rows': 4,
        'placeholder': 'Add any additional information here...'
    }))
    confirm_submission = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'mr-2'}))


def save_application_with_documents(applicant_form, family_form, submission_form, user):
    """Helper function to save application with related documents"""
    application = applicant_form.save(commit=False)
    application.applicant = user
    
    # Update with family form data
    for field in family_form.Meta.fields:
        if field in family_form.cleaned_data:
            setattr(application, field, family_form.cleaned_data[field])
    
    application.save()
    
    # Save documents if provided
    documents_to_save = []
    
    if family_form.cleaned_data.get('is_single_parent') and family_form.cleaned_data.get('is_single_parent_document'):
        documents_to_save.append({
            'document_type': 'SINGLE_PARENT_PROOF',
            'file': family_form.cleaned_data['is_single_parent_document']
        })
    
    if family_form.cleaned_data.get('is_veteran') and family_form.cleaned_data.get('is_veteran_document'):
        documents_to_save.append({
            'document_type': 'VETERAN_STATUS',
            'file': family_form.cleaned_data['is_veteran_document']
        })
    
    if family_form.cleaned_data.get('has_disability') and family_form.cleaned_data.get('disability_document'):
        documents_to_save.append({
            'document_type': 'DISABILITY_CERTIFICATE',
            'file': family_form.cleaned_data['disability_document']
        })
    
    # Save documents
    for doc_data in documents_to_save:
        doc = ApplicationDocument(
            application=application,
            document_type=doc_data['document_type'],
            file=doc_data['file']
        )
        doc.save()
    
    # Calculate priority score
    application.calculate_priority()
    
    return application