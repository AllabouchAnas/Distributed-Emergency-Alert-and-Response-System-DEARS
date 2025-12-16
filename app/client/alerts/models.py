import uuid
from django.db import models
from django.urls import reverse


class EmergencyReport(models.Model):
    """Model representing an emergency alert report."""
    
    # Emergency type choices
    MEDICAL = 'MEDICAL'
    FIRE = 'FIRE'
    POLICE = 'POLICE'
    OTHER = 'OTHER'
    
    EMERGENCY_TYPE_CHOICES = [
        (MEDICAL, 'Medical Emergency'),
        (FIRE, 'Fire Emergency'),
        (POLICE, 'Police Emergency'),
        (OTHER, 'Other Emergency'),
    ]
    
    # Status choices
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'
    
    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
    ]
    
    # Primary key using UUID
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for this emergency report'
    )
    
    # Reporter information
    name = models.CharField(
        max_length=200,
        help_text='Name of the person reporting the emergency'
    )
    
    contact_info = models.CharField(
        max_length=200,
        help_text='Email or phone number for contact'
    )
    
    # Emergency details
    emergency_type = models.CharField(
        max_length=20,
        choices=EMERGENCY_TYPE_CHOICES,
        help_text='Type of emergency'
    )
    
    location = models.CharField(
        max_length=500,
        help_text='Text description of the location'
    )
    
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text='Latitude coordinate'
    )
    
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text='Longitude coordinate'
    )
    
    description = models.TextField(
        help_text='Detailed description of the emergency'
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NEW,
        help_text='Current status of the emergency report'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the report was created'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the report was last updated'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Emergency Report'
        verbose_name_plural = 'Emergency Reports'
    
    def __str__(self):
        """String representation of the model."""
        return f"{self.get_emergency_type_display()} - {str(self.id)[:8]}"
    
    def get_absolute_url(self):
        """Get the URL to view this report's status."""
        return reverse('status', kwargs={'report_id': self.id})
    
    def get_status_badge_class(self):
        """Return CSS class for status badge."""
        status_classes = {
            self.NEW: 'status-new',
            self.IN_PROGRESS: 'status-in-progress',
            self.RESOLVED: 'status-resolved',
        }
        return status_classes.get(self.status, 'status-new')
