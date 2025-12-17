# Generated data migration to create initial users

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_initial_users(apps, schema_editor):
    """Create admin and regular user accounts."""
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('alerts', 'UserProfile')
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@dears.local',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('admin'),
        }
    )
    
    if created:
        # Create admin profile
        UserProfile.objects.create(
            user=admin_user,
            role='ADMIN',
            phone_number='+1234567890',
            address='123 Admin Street',
            city='Admin City'
        )
    
    # Create regular user
    regular_user, created = User.objects.get_or_create(
        username='user',
        defaults={
            'email': 'user@dears.local',
            'first_name': 'Regular',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False,
            'password': make_password('user'),
        }
    )
    
    if created:
        # Create user profile
        UserProfile.objects.create(
            user=regular_user,
            role='CITIZEN',
            phone_number='+0987654321',
            address='456 User Avenue',
            city='User City'
        )


def reverse_initial_users(apps, schema_editor):
    """Remove initial users."""
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=['admin', 'user']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0002_remove_emergencyreport_contact_info_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_users, reverse_initial_users),
    ]
