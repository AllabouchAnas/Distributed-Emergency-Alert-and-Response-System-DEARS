import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dears_project.settings')
django.setup()

from django.contrib.auth.models import User
from alerts.models import UserProfile

# Update admin user
admin = User.objects.get(username='admin')
admin.first_name = 'Admin'
admin.last_name = 'User'
admin.email = 'admin@dears.local'
admin.save()

# Create or update profile
profile, created = UserProfile.objects.get_or_create(
    user=admin,
    defaults={
        'role': 'ADMIN',
        'phone_number': '+1234567890',
        'address': '123 Admin Street',
        'city': 'Admin City'
    }
)

if not created:
    profile.role = 'ADMIN'
    profile.phone_number = '+1234567890'
    profile.address = '123 Admin Street'
    profile.city = 'Admin City'
    profile.save()

print(f"Admin user profile {'created' if created else 'updated'}: {admin.get_full_name()} - {profile.get_role_display()}")
print(f"Phone: {profile.phone_number}")
print(f"Address: {profile.address}, {profile.city}")
