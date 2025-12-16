import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dears_project.settings')
django.setup()

from django.contrib.auth.models import User
from alerts.models import UserProfile

users = User.objects.all()
print(f'\n✅ Total users in database: {users.count()}\n')

for user in users:
    profile_info = f"{user.profile.get_role_display()}" if hasattr(user, 'profile') else "No profile"
    print(f'👤 Username: {user.username}')
    print(f'   Name: {user.get_full_name()}')
    print(f'   Email: {user.email}')
    print(f'   Role: {profile_info}')
    if hasattr(user, 'profile'):
        print(f'   Phone: {user.profile.phone_number}')
        print(f'   Address: {user.profile.address}, {user.profile.city}')
    print()
