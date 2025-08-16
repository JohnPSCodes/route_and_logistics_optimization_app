import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_optimization.settings')
django.setup()

from apps.backend.models import Stop, Route, Order

def create_stop(data:dict): #✅ tested, add decorator for validations and authorized actions
    """
    Creates a Stop with the provided data.
    data must contain:
    - route_id (int)
    - order_id (int)
    - stop_order (int)
    - estimated_arrival (datetime)
    Optional:
    - delivered (bool, default False)
    - delivery_time (datetime, optional)
    """
    stop = Stop.objects.create(
        route=Route.objects.get(pk=data['route_id']),
        order=Order.objects.get(pk=data['order_id']),
        stop_order=data['stop_order'],
        estimated_arrival=data['estimated_arrival'],
        delivered=data.get('delivered', False),
        delivery_time=data.get('delivery_time')
    )

    return stop

def update_stop(stop_id,data:dict): #✅ tested, add decorator for validations and authorized actions
    """
    Updates an existing Stop.
    data can contain any stop field to update:
    - route_id (int)
    - order_id (int)
    - stop_order (int)
    - estimated_arrival (datetime)
    - delivered (bool)
    - delivery_time (datetime)
    """
    stop = Stop.objects.get(pk=stop_id)

    if 'route_id' in data:
        stop.route = Route.objects.get(pk=data['route_id'])

    if 'order_id' in data:
        stop.order = Order.objects.get(pk=data['order_id'])

    for field, value in data.items():
        if field not in ['route_id', 'order_id']:  # Already processed
            setattr(stop, field, value)

    stop.save()
    return stop

def delete_stop(stop_id): # ✅ tested
    stop = Stop.objects.get(pk=stop_id)
    stop.delete()
    return True

def get_stop(stop_id): # ✅ tested
    stop = Stop.objects.get(pk=stop_id)
    return stop

def get_all_stop(): # ✅ tested
    return list(Stop.objects.all())

