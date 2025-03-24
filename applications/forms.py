from django import forms
from .models import Application, HouseholdMember, ApplicationDocument, HouseholdDocument

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
        fields = ['is_single_parent', 'is_veteran', 'has_disability']
        widgets = {
            'is_single_parent': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'is_veteran': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'has_disability': forms.CheckboxInput(attrs={'class': 'mr-2'})
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

class HouseholdMemberForm(forms.ModelForm):
    document_id = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'p-2 border rounded w-full'})
    )
    
    document_birth = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'p-2 border rounded w-full'})
    )
    
    document_disability = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'p-2 border rounded w-full'})
    )
    
    class Meta:
        model = HouseholdMember
        fields = ['full_name', 'date_of_birth', 'relationship', 'has_disability']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'w-full p-2 border rounded', 
                'type': 'date',
                'required': True
            }),
            'relationship': forms.Select(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'has_disability': forms.CheckboxInput(attrs={'class': 'mr-2'})
        }
    
    def save(self, application=None, commit=True):
        instance = super().save(commit=False)
        if application:
            instance.application = application
        
        if commit:
            instance.save()
            
            # Save ID document
            if self.cleaned_data.get('document_id'):
                HouseholdDocument.objects.create(
                    household_member=instance,
                    document_type='ID_PROOF',
                    file=self.cleaned_data['document_id']
                )
            
            # Save birth certificate if provided
            if self.cleaned_data.get('document_birth'):
                HouseholdDocument.objects.create(
                    household_member=instance,
                    document_type='OTHER',
                    file=self.cleaned_data['document_birth']
                )
            
            # Save disability document if applicable
            if self.cleaned_data.get('document_disability') and instance.has_disability:
                HouseholdDocument.objects.create(
                    household_member=instance,
                    document_type='DISABILITY_CERTIFICATE',
                    file=self.cleaned_data['document_disability']
                )
                
        return instance

class ApplicationSubmissionForm(forms.ModelForm):
    confirm_submission = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'mr-2'})
    )
    
    class Meta:
        model = Application
        fields = []
        # fields = ['notes']
        # widgets = {
            # 'notes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'})
        # }