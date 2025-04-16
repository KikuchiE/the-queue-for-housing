from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date
from housing_units.models import HousingUnit  # Replace 'your_app' with the actual app name

class HousingUnitModelTests(TestCase):
    def setUp(self):
        """Set up a sample HousingUnit for tests"""
        self.unit = HousingUnit.objects.create(
            unit_number='A101',
            address='123 Main St, Cityville',
            floor=1,
            total_area=Decimal('75.50'),
            rooms_count=2,
            status='AVAILABLE',
            has_elevator=False,
            has_heating=True,
            last_inspection_date=date(2023, 1, 15),
            next_available_date=date(2023, 6, 1)
        )

    def test_string_representation(self):
        """Test the string representation of the HousingUnit"""
        self.assertEqual(str(self.unit), 'Unit A101 - 2 rooms')

    def test_unit_number_unique(self):
        """Test that unit_number is unique"""
        with self.assertRaises(Exception):
            HousingUnit.objects.create(
                unit_number='A101',  # Duplicate unit_number
                address='456 Elm St, Cityville',
                floor=2,
                total_area=Decimal('85.00'),
                rooms_count=3,
                status='RESERVED'
            )

    def test_status_choices(self):
        """Test that status is limited to the defined choices"""
        invalid_unit = HousingUnit(
            unit_number='B202',
            address='789 Oak St, Cityville',
            floor=2,
            total_area=Decimal('90.00'),
            rooms_count=3,
            status='INVALID_STATUS'  # Invalid choice
        )
        with self.assertRaises(ValidationError):
            invalid_unit.full_clean()

    def test_default_status(self):
        """Test that the default status is 'AVAILABLE'"""
        unit = HousingUnit.objects.create(
            unit_number='C303',
            address='101 Pine St, Cityville',
            floor=3,
            total_area=Decimal('100.00'),
            rooms_count=4
        )
        self.assertEqual(unit.status, 'AVAILABLE')

    def test_total_area_decimal_places(self):
        """Test that total_area has correct decimal places"""
        unit = HousingUnit(
            unit_number='D404',
            address='202 Cedar St, Cityville',
            floor=4,
            total_area=Decimal('120.123'),  # More than 2 decimal places
            rooms_count=5
        )
        with self.assertRaises(ValidationError):
            unit.full_clean()

    def test_rooms_count_positive(self):
        """Test that rooms_count is positive"""
        unit = HousingUnit(
            unit_number='E505',
            address='303 Birch St, Cityville',
            floor=5,
            total_area=Decimal('150.00'),
            rooms_count=0  # Invalid: should be positive
        )
        with self.assertRaises(ValidationError):
            unit.full_clean()

    def test_floor_positive(self):
        """Test that floor is positive"""
        unit = HousingUnit(
            unit_number='F606',
            address='404 Spruce St, Cityville',
            floor=0,  # Invalid: should be positive
            total_area=Decimal('160.00'),
            rooms_count=6
        )
        with self.assertRaises(ValidationError):
            unit.full_clean()

    def test_boolean_fields_default(self):
        """Test default values for boolean fields"""
        unit = HousingUnit.objects.create(
            unit_number='G707',
            address='505 Maple St, Cityville',
            floor=7,
            total_area=Decimal('170.00'),
            rooms_count=7
        )
        self.assertFalse(unit.has_elevator)
        self.assertTrue(unit.has_heating)

    def test_date_fields(self):
        """Test date fields"""
        self.assertEqual(self.unit.last_inspection_date, date(2023, 1, 15))
        self.assertEqual(self.unit.next_available_date, date(2023, 6, 1))

    def test_max_digits_total_area(self):
        """Test that total_area does not exceed max_digits"""
        unit = HousingUnit(
            unit_number='H808',
            address='606 Walnut St, Cityville',
            floor=8,
            total_area=Decimal('9999.99'),  # 6 digits total, should pass
            rooms_count=8
        )
        unit.full_clean()  # Should not raise ValidationError

        invalid_unit = HousingUnit(
            unit_number='I909',
            address='707 Chestnut St, Cityville',
            floor=9,
            total_area=Decimal('10000.00'),  # 7 digits, exceeds max_digits
            rooms_count=9
        )
        with self.assertRaises(ValidationError):
            invalid_unit.full_clean()

    def test_unit_number_max_length(self):
        """Test that unit_number does not exceed max_length"""
        unit = HousingUnit(
            unit_number='A' * 21,  # 21 characters, exceeds max_length=20
            address='808 Ash St, Cityville',
            floor=10,
            total_area=Decimal('200.00'),
            rooms_count=10
        )
        with self.assertRaises(ValidationError):
            unit.full_clean()