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
    RESPONDER = 'RESPONDER'
    
    ROLE_CHOICES = [
        (CITIZEN, 'Citizen'),
        (ADMIN, 'Administrator'),
        (RESPONDER, 'Emergency Responder'),
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
    
    # Link to ResponseUnit for responders
    assigned_unit = models.ForeignKey(
        'ResponseUnit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_responders',
        help_text='Response unit assigned to this responder'
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
    
    def is_responder(self):
        """Check if user has responder role."""
        return self.role == self.RESPONDER


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


class Zone(models.Model):
    """Model representing a geographic zone for alert targeting."""
    
    zone_name = models.CharField(
        max_length=100,
        help_text='Name of the zone (e.g., Downtown, North District)'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Description of the zone'
    )
    
    coordinates = models.TextField(
        blank=True,
        help_text='Geographic coordinates (JSON format for polygon)'
    )
    
    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
    
    def __str__(self):
        return self.zone_name


class ResponseUnit(models.Model):
    """Model representing emergency response units (police cars, ambulances, fire trucks)."""
    
    # Unit type choices
    POLICE = 'POLICE'
    FIRE = 'FIRE'
    MEDICAL = 'MEDICAL'
    
    UNIT_TYPE_CHOICES = [
        (POLICE, 'Police Unit'),
        (FIRE, 'Fire Unit'),
        (MEDICAL, 'Medical Unit'),
    ]
    
    # Status choices
    AVAILABLE = 'AVAILABLE'
    EN_ROUTE = 'EN_ROUTE'
    ON_SITE = 'ON_SITE'
    UNAVAILABLE = 'UNAVAILABLE'
    
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (EN_ROUTE, 'En Route'),
        (ON_SITE, 'On Site'),
        (UNAVAILABLE, 'Unavailable'),
    ]
    
    unit_name = models.CharField(
        max_length=120,
        unique=True,
        help_text='Unique name for the unit (e.g., Police Car 12, Ambulance 5)'
    )
    
    unit_type = models.CharField(
        max_length=20,
        choices=UNIT_TYPE_CHOICES,
        help_text='Type of response unit'
    )
    
    current_location = models.CharField(
        max_length=255,
        help_text='Current location of the unit'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=AVAILABLE,
        help_text='Current status of the unit'
    )
    
    contact_info = models.CharField(
        max_length=100,
        blank=True,
        help_text='Contact information (phone/radio)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Response Unit'
        verbose_name_plural = 'Response Units'
    
    def __str__(self):
        return f"{self.unit_name} ({self.get_unit_type_display()})"
    
    def is_available(self):
        """Check if unit is available for assignment."""
        return self.status == self.AVAILABLE


class Alert(models.Model):
    """Model representing emergency alerts sent through the system."""
    
    # Emergency type choices (same as EmergencyReport)
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
    DISPATCHED = 'DISPATCHED'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'
    CANCELLED = 'CANCELLED'
    
    STATUS_CHOICES = [
        (NEW, 'New'),
        (DISPATCHED, 'Dispatched'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
        (CANCELLED, 'Cancelled'),
    ]
    
    # Reporter (linked to User)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='alerts',
        help_text='User who created the alert'
    )
    
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
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NEW,
        help_text='Current status of the alert'
    )
    
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alerts',
        help_text='Geographic zone where the alert originated'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the alert was created'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the alert was last updated'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
    
    def __str__(self):
        return f"Alert #{self.id} - {self.get_emergency_type_display()}"
    
    def get_status_badge_class(self):
        """Return CSS class for status badge."""
        status_classes = {
            self.NEW: 'status-new',
            self.DISPATCHED: 'status-dispatched',
            self.IN_PROGRESS: 'status-in-progress',
            self.RESOLVED: 'status-resolved',
            self.CANCELLED: 'status-cancelled',
        }
        return status_classes.get(self.status, 'status-new')


class Response(models.Model):
    """Model representing response unit assignments to alerts."""
    
    # Response status choices
    ASSIGNED = 'ASSIGNED'
    EN_ROUTE = 'EN_ROUTE'
    ON_SITE = 'ON_SITE'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    
    RESPONSE_STATUS_CHOICES = [
        (ASSIGNED, 'Assigned'),
        (EN_ROUTE, 'En Route'),
        (ON_SITE, 'On Site'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    alert = models.ForeignKey(
        Alert,
        on_delete=models.CASCADE,
        related_name='responses',
        help_text='Alert this response is addressing'
    )
    
    response_unit = models.ForeignKey(
        ResponseUnit,
        on_delete=models.CASCADE,
        related_name='responses',
        help_text='Response unit assigned'
    )
    
    status = models.CharField(
        max_length=20,
        choices=RESPONSE_STATUS_CHOICES,
        default=ASSIGNED,
        help_text='Current status of the response'
    )
    
    notes = models.TextField(
        blank=True,
        help_text='Notes about the response'
    )
    
    assigned_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the unit was assigned'
    )
    
    arrived_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the unit arrived on site'
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the response was completed'
    )
    
    class Meta:
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.response_unit.unit_name} → Alert #{self.alert.id}"
