#!/usr/bin/env python
"""Create a new admin user with custom credentials"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growfund.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# New admin credentials - CUSTOMIZE THESE
email = 'Migwibrian316@gmail.com'   # Your email
password = 'Buffers316!'             # Your password
first_name = 'Brian'                 # Your first name
last_name = 'Migwi'                  # Your last name

print("=" * 60)
print("CREATING NEW ADMIN USER")
print("=" * 60)

try:
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        admin = User.objects.get(email=email)
        print(f"\n✓ User already exists: {admin.email}")
        print(f"  Updating to admin permissions...")
        
        # Update to admin
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_verified = True
        admin.is_active = True
        admin.first_name = first_name
        admin.last_name = last_name
        admin.set_password(password)
        admin.save()
        
        print(f"\n✓ User updated to admin successfully!")
    else:
        # Create new admin user
        print(f"\n✓ Creating new admin user: {email}")
        admin = User.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"\n✓ Admin user created successfully!")
    
    # Display details
    print("\n" + "=" * 60)
    print("NEW ADMIN USER DETAILS")
    print("=" * 60)
    print(f"\nEmail: {admin.email}")
    print(f"Password: {password}")
    print(f"Name: {admin.first_name} {admin.last_name}")
    print(f"Staff: {admin.is_staff}")
    print(f"Superuser: {admin.is_superuser}")
    print(f"Verified: {admin.is_verified}")
    print(f"Active: {admin.is_active}")
    print(f"Balance: ${admin.balance}")
    
    print("\n" + "=" * 60)
    print("LOGIN CREDENTIALS")
    print("=" * 60)
    print(f"\nEmail: {email}")
    print(f"Password: {password}")
    print(f"\nAdmin Panel: https://your-service.onrender.com/admin/")
    print(f"API Login: https://your-service.onrender.com/api/auth/login/")
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()