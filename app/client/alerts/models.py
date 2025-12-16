import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile with role and personal information."""
    
    # User role choices
    CITIZEN = 'CITIZEN'
    ADMIN = 'ADMIN'
    
    ROLE_CHOICES = [
        (CITIZEN, 'Citizen'),
        (ADMIN, 'Administrator'),
    ]
    
    # Link to Django User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CITIZEN,
        help_text='User role in the system'
    )
    
    # Personal information
    phone_number = models.CharField(
        max_length=20,
        help_text='Contact phone number'
    )
    
    address = models.CharField(
        max_length=500,
        help_text='Home address'
    )
    
    city = models.CharField(
        max_length=100,
        help_text='City'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == self.ADMIN
    
    def is_citizen(self):
        """Check if user has citizen role."""
        return self.role == self.CITIZEN


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()



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
    
    # Reporter (linked to User)
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emergency_reports',
        help_text='User who reported the emergency'
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
