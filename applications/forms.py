from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Application, ApplicationHistory
from users.models import User

class ApplicationForm(forms.ModelForm):
    """Main form for creating and editing housing applications"""
    
    class Meta:
        model = Application
        exclude = ['application_number', 'applicant', 'status', 'submission_date', 
                'last_updated', 'priority_score', 'queue_position', 'document_verified']
        
        widgets = {
            'current_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'disability_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'current_residence_condition': forms.Select(attrs={'class': 'form-select'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_living_area': forms.NumberInput(attrs={'class': 'form-control'}),
            'adults_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'children_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'elderly_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'waiting_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'documents_valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
        labels = {
            'current_address': _('Current Address'),
            'is_homeless': _('Currently Homeless'),
            'current_residence_condition': _('Current Housing Condition'),
            'monthly_income': _('Monthly Income (KZT)'),
            'is_veteran': _('Veteran Status'),
            'is_single_parent': _('Single Parent'),
            'waiting_years': _('Years on Waiting List'),
            'current_living_area': _('Current Living Area (sq.m)'),
            'has_disability': _('Has Disability'),
            'disability_details': _('Disability Details'),
            'adults_count': _('Number of Adults'),
            'children_count': _('Number of Children'),
            'elderly_count': _('Number of Elderly'),
            'documents_valid_until': _('Documents Valid Until'),
        }
        
        help_texts = {
            'current_living_area': _('Total area of current residence in square meters'),
            'monthly_income': _('Total monthly household income'),
            'documents_valid_until': _('Date until which submitted documents remain valid'),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.applicant_id:
            instance.applicant = self.user
        
        if commit:
            instance.save()
            instance.calculate_priority()
        return instance


class ApplicationSearchForm(forms.Form):
    """Form for searching applications"""
    application_number = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Application Number')})
    )
    status = forms.ChoiceField(
        choices=[('', '--------')] + Application.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    applicant_name = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Applicant Name')})
    )
    submission_date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    submission_date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class ApplicationStatusUpdateForm(forms.ModelForm):
    """Form for updating application status"""
    
    class Meta:
        model = ApplicationHistory
        fields = ['new_status', 'notes', 'rejection_reason']
        widgets = {
            'new_status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'rejection_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.application = kwargs.pop('application', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.application:
            current_status = self.application.status
            # Filter status choices based on current status and workflow rules
            valid_next_statuses = self._get_valid_next_statuses(current_status)
            self.fields['new_status'].choices = [
                (status, label) for status, label in Application.STATUS_CHOICES
                if status in valid_next_statuses
            ]
            
            # Show rejection reason only for REJECTED status
            if 'REJECTED' not in valid_next_statuses:
                self.fields['rejection_reason'].widget = forms.HiddenInput()
    
    def _get_valid_next_statuses(self, current_status):
        """Define valid status transitions based on current status"""
        status_flow = {
            'DRAFT': ['SUBMITTED'],
            'SUBMITTED': ['UNDER_REVIEW', 'REJECTED'],
            'UNDER_REVIEW': ['VERIFIED', 'REJECTED'],
            'VERIFIED': ['IN_QUEUE', 'REJECTED'],
            'IN_QUEUE': ['HOUSING_OFFERED', 'REJECTED', 'EXPIRED'],
            'HOUSING_OFFERED': ['ACCEPTED', 'REJECTED', 'EXPIRED'],
            'ACCEPTED': ['EXPIRED'],
            'REJECTED': [],
            'EXPIRED': [],
        }
        return status_flow.get(current_status, [])
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.application:
            instance.application = self.application
            instance.previous_status = self.application.status
            
            # Update the application status
            self.application.status = instance.new_status
            if commit:
                self.application.save(update_fields=['status', 'last_updated'])
        
        if self.user:
            instance.changed_by = self.user
            
        if commit:
            instance.save()
        
        return instance


class DocumentUploadForm(forms.Form):
    """Form for uploading application supporting documents"""
    DOCUMENT_TYPES = [
        ('ID', _('ID Document')),
        ('INCOME', _('Income Proof')),
        ('RESIDENCE', _('Current Residence Document')),
        ('FAMILY', _('Family Composition Document')),
        ('DISABILITY', _('Disability Certificate')),
        ('VETERAN', _('Veteran Status Document')),
        ('OTHER', _('Other Supporting Document')),
    ]
    
    document_type = forms.ChoiceField(
        choices=DOCUMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    document_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Document Description')})
    )
    expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class FamilyMemberForm(forms.Form):
    """Form for adding family member information"""
    RELATION_CHOICES = [
        ('SPOUSE', _('Spouse')),
        ('CHILD', _('Child')),
        ('PARENT', _('Parent')),
        ('GRANDPARENT', _('Grandparent')),
        ('OTHER', _('Other')),
    ]
    
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    middle_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    relationship = forms.ChoiceField(
        choices=RELATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    has_disability = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_dependent = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class EmploymentDetailsForm(forms.Form):
    """Form for employment and workplace details"""
    EMPLOYMENT_TYPES = [
        ('FULL_TIME', _('Full-time')),
        ('PART_TIME', _('Part-time')),
        ('SELF_EMPLOYED', _('Self-employed')),
        ('RETIRED', _('Retired')),
        ('UNEMPLOYED', _('Unemployed')),
        ('STUDENT', _('Student')),
        ('OTHER', _('Other')),
    ]
    
    employment_type = forms.ChoiceField(
        choices=EMPLOYMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    employer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    position = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    employment_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    workplace_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
    )
    monthly_salary = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )