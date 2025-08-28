import os
import django
import csv
from django.utils import timezone
from datetime import datetime

# Django Config (adjust the path based on your project)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_optimization.settings')
django.setup()

from apps.backend.models import User, Order, Route, Stop

def import_users_from_csv(filename):
    """Import users from a CSV file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir, '..', 'datasets', filename))
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            User.objects.create(
                name=row['name'],
                email=row['email'],
                password_hash=row['password_hash'],
            )
    print("Users imported successfully.")

def import_orders_from_csv(filename):
    """Import orders from a CSV file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir, '..', 'datasets', filename))
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Order.objects.create(
                customer_name=row['customer_name'],
                address=row['address'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                delivery_window_start=timezone.datetime.fromisoformat(row['delivery_window_start']),
                delivery_window_end=timezone.datetime.fromisoformat(row['delivery_window_end']),
                priority=int(row['priority']),
            )
    print("Orders imported successfully.")

def import_routes_from_csv(filename):
    """Import routes from a CSV file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir,'..','datasets',filename))
    with open(file_path,newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Route.objects.create(
                name=row['name'],
                planned_date=datetime.strptime(row['planned_date'], "%Y-%m-%d").date(),
                status=row['status'],
                created_by_id=int(row['created_by_id'])
            )
    print("Routes imported successfully.")

def import_stops_from_csv(filename):
    """Import stops from a CSV file while validating foreign keys."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir,'..','datasets',filename))
    with open(file_path,newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Validate that the related Order exists
            try:
                order = Order.objects.get(id=int(row['order_id']))
            except Order.DoesNotExist:
                print(f"Order {row['order_id']} does not exist. Skipping stop.")
                continue

            # Validate that the related Route exists
            try:
                route = Route.objects.get(id=int(row['route_id']))
            except Route.DoesNotExist:
                print(f"Route {row['route_id']} does not exist. Skipping stop.")
                continue

            # Create the Stop object
            Stop.objects.create(
                stop_order=int(row['stop_order']),
                estimated_arrival=timezone.datetime.fromisoformat(row['estimated_arrival']),
                delivered=bool(int(row['delivered'])),
                delivery_time=timezone.datetime.fromisoformat(row['delivery_time']),
                order=order,
                route=route
            )
    print("Stops imported successfully.")

if __name__ == "__main__":
    # Import datasets in the correct order to maintain FK constraints
    import_users_from_csv('datasets_users.csv')
    import_orders_from_csv('datasets_orders.csv')
    import_routes_from_csv('dataset_routes.csv')
    import_stops_from_csv('dataset_stops.csv')
