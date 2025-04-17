# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'iin', 'email', 'first_name', 'last_name', 'phone_number', 
                 'profile_picture', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'iin', 'phone_number']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            iin=validated_data.get('iin', None),
            phone_number=validated_data.get('phone_number', None)
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data



# API BOT

from rest_framework import serializers
from applications.models import Application, ApplicationDocument

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'category', 'is_for_ward', 'current_address', 'is_homeless',
            'current_residence_condition', 'monthly_income', 'current_living_area',
            'is_veteran', 'is_single_parent', 'has_disability', 'disability_details',
            'adults_count', 'children_count', 'elderly_count'
        ]

class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ['document_type', 'file', 'document_name']

