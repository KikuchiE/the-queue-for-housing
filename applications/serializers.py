# from rest_framework import serializers
# from .models import Application

# class ApplicantDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Application
#         fields = [
#             'current_address', 'is_homeless', 'current_residence_condition',
#             'monthly_income', 'current_living_area', 'is_veteran',
#             'is_single_parent', 'has_disability', 'disability_details'
#         ]

# class FamilyDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Application
#         fields = ['adults_count', 'children_count', 'elderly_count']

# class ApplicationSubmissionSerializer(serializers.Serializer):
#     notes = serializers.CharField(allow_blank=True, required=False)

# api/serializers.py
# api/serializers.py
from rest_framework import serializers

# Serializer to validate input (just iin)
class QueueSerializer(serializers.Serializer):
    iin = serializers.CharField(max_length=12)  # Adjust max_length as needed

# Serializer for response (just queue_position)
class QueueCheckResponseSerializer(serializers.Serializer):
    queue_position = serializers.IntegerField()