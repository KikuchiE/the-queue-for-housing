from django.db import models
from applications.models import Application

# Create your models here.
class Notification(models.Model):
    TYPE_CHOICES = [
        ('STATUS_CHANGE', 'Status Change'),
        ('DOCUMENT_RENEWAL', 'Document Renewal'),
        ('QUEUE_UPDATE', 'Queue Position Update'),
        ('HOUSING_OFFER', 'Housing Offer'),
        ('GENERAL', 'General Notification'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('READ', 'Read'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, 
                                    related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    sent_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.notification_type} for {self.application.application_number}"