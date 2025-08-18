# pylint: disable=import-error
from apps.backend.models import User, Order, Route, Stop
from django.utils import timezone
from datetime import timedelta

def create_user(name="Test User",email="test@example.com",password_hash="fakehash"):
    return User.objects.create(name=name,email=email,password_hash=password_hash)

def create_order(customer_name="Test Customer",priority=2,**kwargs):
    now = timezone.now()
    defaults = dict(
        address="123 Main St",
        latitude=40.0,
        longitude=-70.0,
        delivery_window_start=now,
        delivery_window_end=now + timedelta(hours=2),
        priority=priority
    )

    defaults.update(kwargs)
    return Order.objects.create(customer_name=customer_name,**defaults)

def create_route(user=None, name="Route Test", planned_date=None, **kwargs):
    if not user:
        user = create_user()
    if not planned_date:
        planned_date = timezone.now().date()
    defaults = dict(created_by=user)
    defaults.update(kwargs)
    return Route.objects.create(name=name,planned_date=planned_date,**defaults)

def create_stop(route=None,order=None,stop_order=1,**kwargs):
    if not route:
        route = create_route()
    if not order:
        order = create_order()
    defaults = dict(
        estimated_arrival=timezone.now() + timedelta(hours=1),
        delivered=False
    )
    defaults.update(kwargs)
    return Stop.objects.create(route=route,order=order,stop_order=stop_order,**defaults)