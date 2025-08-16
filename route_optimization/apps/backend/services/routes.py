import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_optimization.settings')
django.setup()

from apps.backend.models import Route,User


def create_route(data:dict): # ✅ tested, add decorator for validations and authorized actions
    """
    Creates a route with the provided data.
    data must contain: name,planned_date,status,created_by_id
    """

    user = User.objects.get(pk=data['created_by_id']) # FK lookup

    route = Route.objects.create(
        name=data['name'],
        planned_date=data['planned_date'],
        status=data['status'],
        created_by=user
    )
    return route

def update_route(route_id,data:dict): # ✅ tested, add decorator for validations and authorized actions
    """
    Updates a route with the provided data.
    data can contain: name,planned_date,status,created_by_id
    """

    route = Route.objects.get(pk=route_id)

    if "created_by_id" in data:
        route.created_by = User.objects.get(pk=data["created_by_id"])
        data.pop("created_by_id") # remove from dict to avoid conflict
    
    # update the fields dinamically
    for field,value in data.items():
        setattr(route,field,value)
    
    route.save()
    return route

def delete_route(route_id): # ✅ tested
    route = Route.objects.get(pk=route_id)
    route.delete()
    return True

def get_route(route_id): # ✅ tested
    route = Route.objects.get(pk=route_id)
    return route

def get_all_route(): # ✅ tested
    return list(Route.objects.all())

