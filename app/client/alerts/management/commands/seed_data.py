from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from alerts.models import UserProfile, ResponseUnit, Alert, UserRole, EmergencyType, UnitStatus, AlertStatus
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Users
        self.create_users()
        
        # Create Response Units
        self.create_response_units()
        
        # Create Alerts
        self.create_alerts()

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))

    def create_users(self):
        # Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@dears.com', 'admin123')
            # Profile is created by signal, update it
            admin.profile.role = UserRole.ADMIN
            admin.profile.save()
            self.stdout.write('Created admin user')

        # Responder
        if not User.objects.filter(username='responder1').exists():
            responder = User.objects.create_user('responder1', 'responder1@dears.com', 'password123')
            responder.first_name = 'John'
            responder.last_name = 'Doe'
            responder.save()
            responder.profile.role = UserRole.RESPONDER
            responder.profile.phone_number = '555-0101'
            responder.profile.save()
            self.stdout.write('Created responder user')

        # Citizen
        if not User.objects.filter(username='citizen1').exists():
            citizen = User.objects.create_user('citizen1', 'citizen1@dears.com', 'password123')
            citizen.first_name = 'Jane'
            citizen.last_name = 'Smith'
            citizen.save()
            citizen.profile.role = UserRole.CITIZEN
            citizen.profile.phone_number = '555-0202'
            citizen.profile.address = '123 Main St'
            citizen.profile.city = 'Metropolis'
            citizen.profile.save()
            self.stdout.write('Created citizen user')

    def create_response_units(self):
        units_data = [
            {'name': 'Police Unit 1', 'type': EmergencyType.POLICE, 'lat': 40.7128, 'lon': -74.0060},
            {'name': 'Fire Truck 5', 'type': EmergencyType.FIRE, 'lat': 40.7138, 'lon': -74.0070},
            {'name': 'Ambulance 3', 'type': EmergencyType.MEDICAL, 'lat': 40.7148, 'lon': -74.0050},
        ]

        for data in units_data:
            unit, created = ResponseUnit.objects.get_or_create(
                unit_name=data['name'],
                defaults={
                    'unit_type': data['type'],
                    'current_location': 'Downtown',
                    'latitude': data['lat'],
                    'longitude': data['lon'],
                    'status': UnitStatus.AVAILABLE
                }
            )
            if created:
                self.stdout.write(f"Created unit: {unit.unit_name}")

    def create_alerts(self):
        citizen = User.objects.get(username='citizen1')
        
        alerts_data = [
            {
                'type': EmergencyType.MEDICAL,
                'desc': 'Heart attack suspected',
                'loc': '123 Main St',
                'lat': 40.7128,
                'lon': -74.0060,
                'status': AlertStatus.PENDING
            },
            {
                'type': EmergencyType.FIRE,
                'desc': 'Trash can fire',
                'loc': 'Central Park',
                'lat': 40.7851,
                'lon': -73.9683,
                'status': AlertStatus.RESOLVED
            }
        ]

        for data in alerts_data:
            if not Alert.objects.filter(description=data['desc']).exists():
                Alert.objects.create(
                    user=citizen,
                    emergency_type=data['type'],
                    description=data['desc'],
                    location=data['loc'],
                    latitude=data['lat'],
                    longitude=data['lon'],
                    status=data['status']
                )
                self.stdout.write(f"Created alert: {data['desc']}")
