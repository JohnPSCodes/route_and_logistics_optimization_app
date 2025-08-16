import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_optimization.settings')
django.setup()

from apps.backend.models import Order

def create_order(data:dict): # ✅ tested, add decorator for validations and authorized actions
    """
    Creates an order with the provided data,
    data must contain:
    - customer_name
    - address
    - latitude
    - longitude
    - priority
    - delivery_window_start (datetime)
    - delivery_window_end (datetime)
    - status (opcional, default='pending')
    """
    order = Order.objects.create(
        customer_name=data['customer_name'],
        address=data['address'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        priority=data.get('priority', 1),
        delivery_window_start=data['delivery_window_start'],
        delivery_window_end=data['delivery_window_end'],
        status=data.get('status', 'pending')
    )
    return order


def update_order(order_id,data:dict): #✅ tested, add decorator for validations and authorized actions
    """
    Updates an existing Order with the provided data.
    'data' should be a dictionary with any of the Order fields to update.
    """
    order = Order.objects.get(pk=order_id)
    for field,value in data.items():
        setattr(order,field,value)
    order.save()
    return order

def delete_order(order_id): # ✅ tested
    """
    Deletes the Order with the given order_id.
    Returns True if deletion was successful.
    """
    order = Order.objects.get(pk=order_id)
    order.delete()
    return True


def get_order(order_id): # ✅ tested
    """
    Retrieves an Order by its ID.
    Returns the Order instance.
    """
    order = Order.objects.get(pk=order_id)
    return order

def get_all_orders(): # ✅ tested
    return list(Order.objects.all())


