
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_optimization.settings')
django.setup()

from apps.backend.models import User

def create_user(data:dict): # ✅ tested, add decorator for validations and authorized actions
    """
    Creates an user with the provided data, 
    data must contain: name,email,password_hash
    """
    user = User.objects.create(
        name=data['name'],
        email=data['email'],
        password_hash=data['password_hash']
    )
    return user

def update_user(user_id,data:dict): # ✅ tested, add decorator for validations and authorized actions
    user = User.objects.get(pk=user_id)
    for field,value in data.items():
        setattr(user,field,value)
    user.save()
    return user

def delete_user(user_id): # ✅ tested, add decorator for validations and authorized actions
    user = User.objects.get(pk=user_id)
    user.delete()
    return True

def get_user(user_id): # ✅ tested
    user = User.objects.get(pk=user_id)
    return user

def get_all_users(): # ✅ tested
    return list(User.objects.all())

