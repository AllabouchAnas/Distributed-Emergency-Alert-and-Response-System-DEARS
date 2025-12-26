import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Enumerations
class UserRole(models.TextChoices):
    CITIZEN = 'CITIZEN', 'Citizen'
    ADMIN = 'ADMIN', 'Administrator'
    RESPONDER = 'RESPONDER', 'Responder'

class EmergencyType(models.TextChoices):
    POLICE = 'POLICE', 'Police'
    FIRE = 'FIRE', 'Fire'
    MEDICAL = 'MEDICAL', 'Medical'

class AlertStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    RESOLVED = 'RESOLVED', 'Resolved'

class UnitStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Available'
    EN_ROUTE = 'EN_ROUTE', 'En Route'
    ON_SCENE = 'ON_SCENE', 'On Scene'
    UNAVAILABLE = 'UNAVAILABLE', 'Unavailable'

class UserProfile(models.Model):
    """
    Extended user profile matching 'User' entity in UML.
    Fields: userID (id), username (user.username), passwordHash (user.password), role.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CITIZEN,
        help_text='User role'
    )
    
    # Personal information
    phone_number = models.CharField(
        max_length=20,
        help_text='Contact phone number',
        blank=True
    )
    
    address = models.CharField(
        max_length=500,
        help_text='Home address',
        blank=True
    )
    
    city = models.CharField(
        max_length=100,
        help_text='City',
        blank=True
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

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def is_responder(self):
        return self.role == UserRole.RESPONDER

    def is_citizen(self):
        return self.role == UserRole.CITIZEN

    def submit_alert(self):
        # Logic to submit alert would go here or in views/services
        pass

    def view_alert_history(self):
        # Logic to view history
        return self.user.alerts.all()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class ResponseUnit(models.Model):
    """
    Model matching 'ResponseUnit' entity in UML.
    """
    unit_id = models.AutoField(primary_key=True)  # unitID
    unit_name = models.CharField(max_length=100)  # unitName
    unit_type = models.CharField(
        max_length=20, 
        choices=EmergencyType.choices
    )  # unitType
    current_location = models.CharField(max_length=255)  # currentLocation
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=UnitStatus.choices, 
        default=UnitStatus.AVAILABLE
    )  # status

    class Meta:
        verbose_name = 'Response Unit'
        verbose_name_plural = 'Response Units'
        db_table = 'response_units'

    def __str__(self):
        return f"{self.unit_name} ({self.unit_type})"

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def update_location(self, location):
        self.current_location = location
        self.save()

from django.db.models.functions import Now

class Alert(models.Model):
    """
    Model matching 'Alert' entity in UML.
    """
    alert_id = models.AutoField(primary_key=True)  # alertID
    timestamp = models.DateTimeField(db_default=Now())  # timestamp
    description = models.TextField()  # description
    location = models.CharField(max_length=255)  # location
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=AlertStatus.choices, 
        default=AlertStatus.PENDING
    )  # status
    emergency_type = models.CharField(
        max_length=20, 
        choices=EmergencyType.choices
    )  # emergencyType

    # Relationships
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='alerts'
    )  # Association with User (submit)
    
    # Association with ResponseUnit (assign) - 0..1
    assigned_unit = models.ForeignKey(
        ResponseUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alerts',
        db_column='assigned_unit'
    )

    class Meta:
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
        db_table = 'alerts'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Alert {self.alert_id} - {self.emergency_type}"

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def assign_unit(self, unit):
        self.assigned_unit = unit
        self.save()
