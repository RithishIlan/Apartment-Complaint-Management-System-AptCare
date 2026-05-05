import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aptcare.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# 1. Fix Admin Role
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
else:
    # Update existing admin to have the correct role so login works
    User.objects.filter(username='admin').update(role='admin')

# 2. Create Showcase Resident
if not User.objects.filter(username='resident1').exists():
    User.objects.create_user(
        username='resident1', 
        email='resident@aptcare.com', 
        password='Resident123!', 
        role='user', 
        first_name='John', 
        last_name='Doe', 
        block='A', 
        flat_number='101',
        is_active=True
    )

print("Startup configuration completed successfully.")
