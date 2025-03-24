from django.db import models
from users.models import User

# Create your models here.
class Application(models.Model):
    STATUS_CHOICES = [
        # ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('VERIFIED', 'Verified'),
        ('IN_QUEUE', 'In Queue'),
        ('HOUSING_OFFERED', 'Housing Offered'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED_BY_APPLICANT', 'Rejected by Applicant'),
        ('REJECTED_BY_MANAGER', 'Rejected by Manager'),
        ('EXPIRED', 'Expired'),
    ]
    
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    application_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    submission_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Current living conditions
    current_address = models.TextField()
    is_homeless = models.BooleanField(default=False)
    current_residence_condition = models.CharField(max_length=50, choices=[
        ('GOOD', 'Good'),
        ('ADEQUATE', 'Adequate'),
        ('POOR', 'Poor'),
        ('UNSAFE', 'Unsafe'),
    ])
    
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)

    is_veteran = models.BooleanField(default=False)
    is_single_parent = models.BooleanField(default=False)
    waiting_years = models.PositiveSmallIntegerField(default=0)
    
    current_living_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    has_disability = models.BooleanField(default=False)
    disability_details = models.TextField(blank=True)
    
    # adults_count = models.PositiveSmallIntegerField(default=1)
    # children_count = models.PositiveSmallIntegerField(default=0)
    # elderly_count = models.PositiveSmallIntegerField(default=0)
    
    priority_score = models.IntegerField(default=0)
    queue_position = models.PositiveIntegerField(null=True, blank=True)
    
    # documents_valid_until = models.DateField(null=True, blank=True)
    document_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Application {self.application_number} - {self.applicant}"
    
    def calculate_priority(self):
        """Calculate priority score based on various criteria"""
        score = 0
        reference_income = 100000
        
        if self.monthly_income < reference_income:
            income_factor = (reference_income - self.monthly_income) / reference_income
            score += int(income_factor * 20)  # Max 20 points for income
        
        # score += self.children_count * 10
        if self.has_disability:
            score += 15
        
        # if (self.adults_count + self.children_count + self.elderly_count) > 0 and self.current_living_area:
        #     space_per_person = self.current_living_area / (self.adults_count + self.children_count + self.elderly_count)
        #     if space_per_person < 6:
        #         score += 15
        #     elif space_per_person < 10:
        #         score += 10
        #     elif space_per_person < 15:
        #         score += 5

        if self.is_veteran:
            score += 10
        
        if self.is_single_parent:
            score += 10
        
        score += self.waiting_years * 5
        
        self.priority_score = score
        self.save(update_fields=['priority_score'])
        return score
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            last_application = Application.objects.order_by('-id').first()
            if last_application:
                last_id = int(last_application.application_number[3:])
                self.application_number = f"APP{last_id + 1:06d}"
            else:
                self.application_number = "APP000001"
        
        super().save(*args, **kwargs)


class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='history')
    previous_status = models.CharField(max_length=30, choices=Application.STATUS_CHOICES)
    rejection_reason = models.TextField(blank=True, null=True)
    new_status = models.CharField(max_length=30, choices=Application.STATUS_CHOICES)
    change_date = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.application.application_number}: {self.previous_status} → {self.new_status}"


class ApplicationDocument(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=[
        # ('ID_PROOF', 'ID Proof'),
        ('INCOME_STATEMENT', 'Income Statement'),
        ('DISABILITY_CERTIFICATE', 'Disability Certificate'),
        ('VETERAN_STATUS', 'Veteran Status'),

        # ('RESIDENCE_PROOF', 'Residence Proof'),
        ('OTHER', 'Other'),
    ])
    file = models.FileField(upload_to='application_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.application.application_number} - {self.get_document_type_display()}"

class HouseholdMember(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='household_members')
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    relationship = models.CharField(max_length=50, choices=[
        ('SPOUSE', 'Spouse'),
        ('CHILD', 'Child'),
        ('PARENT', 'Parent'),
        ('SIBLING', 'Sibling'),
        ('OTHER', 'Other'),
    ])
    has_disability = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.full_name} ({self.get_relationship_display()})"

class HouseholdDocument(models.Model):
    household_member = models.ForeignKey(HouseholdMember, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=[
        ('ID_PROOF', 'ID Proof'),
        ('DISABILITY_CERTIFICATE', 'Disability Certificate'),
        ('OTHER', 'Other'),
    ])
    file = models.FileField(upload_to='household_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.household_member.full_name} - {self.get_document_type_display()}"
