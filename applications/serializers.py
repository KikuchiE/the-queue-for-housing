from rest_framework import serializers
from .models import Application

class ApplicantDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'current_address', 'is_homeless', 'current_residence_condition',
            'monthly_income', 'current_living_area', 'is_veteran',
            'is_single_parent', 'has_disability', 'disability_details'
        ]

class FamilyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['adults_count', 'children_count', 'elderly_count']

class ApplicationSubmissionSerializer(serializers.Serializer):
    notes = serializers.CharField(allow_blank=True, required=False)