from django.db import models
from users.models import User

class HousingUnit(models.Model):
    UNIT_STATUS = [
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Under Maintenance'),
    ]
    
    unit_number = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    floor = models.PositiveSmallIntegerField()
    total_area = models.DecimalField(max_digits=6, decimal_places=2)
    rooms_count = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=20, choices=UNIT_STATUS, default='AVAILABLE')
    # is_accessible = models.BooleanField(default=False)
    # monthly_rent = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    has_elevator = models.BooleanField(default=False)
    has_heating = models.BooleanField(default=True)
    last_inspection_date = models.DateField(null=True, blank=True)
    next_available_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Unit {self.unit_number} - {self.rooms_count} rooms"

class HousingAllocation(models.Model):
    STATUS_CHOICES = [
        ('OFFERED', 'Offered'),
        # ('ACCEPTED', 'Accepted'),
        # ('DECLINED', 'Declined'),
        ('EXPIRED', 'Offer Expired'),
        ('ACTIVE', 'Tenancy Active'),
    ]
    
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE)
    housing_unit = models.ForeignKey(HousingUnit, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    offer_date = models.DateField(auto_now_add=True)
    # response_deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OFFERED')
    # rejection_reason = models.TextField(null=True, blank=True)

    # response_date = models.DateField(null=True, blank=True)
    # tenancy_start_date = models.DateField(null=True, blank=True)
    tenancy_end_date = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Allocation: {self.application.application_number} → {self.housing_unit.unit_number}"