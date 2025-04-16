from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class UserManagerTests(TestCase):
    def test_create_user(self):
        """Test creating a regular user with valid credentials"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone_number='+1234567890'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_administrator)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_email(self):
        """Test creating user without email raises ValueError"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='testpass123',
                first_name='John',
                last_name='Doe'
            )

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
            phone_number='+1234567890'
        )
        
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.check_password('adminpass123'))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_administrator)
        self.assertTrue(superuser.is_superuser)

    def test_normalize_email(self):
        """Test email normalization"""
        user = User.objects.create_user(
            email='Test.User@Example.COM',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone_number='+1234567890'
        )
        self.assertEqual(user.email, 'Test.User@example.com')

class UserModelTests(TestCase):
    def setUp(self):
        """Set up test user for model tests"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone_number='+1234567890',
            iin='123456789012'
        )

    def test_string_representation(self):
        """Test the string representation of the user"""
        self.assertEqual(str(self.user), 'John Doe')

    def test_get_full_name(self):
        """Test get_full_name method"""
        self.assertEqual(self.user.get_full_name(), 'John Doe')

    def test_email_unique(self):
        """Test that email field is unique"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',  # Duplicate email
                password='testpass456',
                first_name='Jane',
                last_name='Doe',
                phone_number='+0987654321'
            )

    def test_iin_unique(self):
        """Test that IIN field is unique"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test2@example.com',
                password='testpass456',
                first_name='Jane',
                last_name='Doe',
                phone_number='+0987654321',
                iin='123456789012'  # Duplicate IIN
            )

    def test_default_profile_picture(self):
        """Test default profile picture path"""
        self.assertEqual(
            self.user.profile_picture.name,
            'profile_pictures/default.png'
        )

    def test_field_max_lengths(self):
        """Test max length constraints on fields"""
        user = User(
            email='test2@example.com',
            first_name='x' * 151,  # Exceeds max_length
            last_name='Doe',
            phone_number='+1234567890'
        )
        with self.assertRaises(Exception):
            user.full_clean()

    def test_date_joined(self):
        """Test date_joined is set automatically"""
        self.assertIsNotNone(self.user.date_joined)
        self.assertLessEqual(self.user.date_joined, timezone.now())

    def test_is_active_default(self):
        """Test is_active default value"""
        self.assertTrue(self.user.is_active)

    def test_is_staff_default(self):
        """Test is_staff default value"""
        self.assertFalse(self.user.is_staff)