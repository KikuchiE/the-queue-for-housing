from django import forms
from applications.models import Application

class ApplicationFilterForm(forms.Form):
    applicant_iin = forms.CharField(
        label='Applicant\'s IIN',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded mt-1', 
            'placeholder': 'Applicant\'s IIN'
        })
    )
    application_number = forms.CharField(
        label='Application Number',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded mt-1', 
            'placeholder': 'Application Number'
        })
    )
    status = forms.ChoiceField(
        label='Status',
        required=False,
        choices=[('', 'All Statuses')] + Application.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded mt-1'
        })
    )