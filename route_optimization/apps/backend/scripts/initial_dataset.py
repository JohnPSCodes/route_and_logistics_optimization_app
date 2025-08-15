import os
import django
import csv
from django.utils import timezone
from datetime import timedelta,datetime

# Django Config (adjust the path based on your project)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_optimization.settings')
django.setup()

from apps.backend.models import User, Order, Route, Stop

def import_users_from_csv(filename):
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

def import_routes_from_csv(filename): # working
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir,'..','datasets',filename))
    with open(file_path,newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Route.objects.create(
                name = row['name'],
                planned_date = datetime.strptime(row['planned_date'],"%Y-%m-%d").date(),
                status = row['status'],
                created_by_id = int(row['created_by_id'])
            )
    print("Routes imported successfully.")

def import_stops_from_csv(filename): # working
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir,'..','datasets',filename))
    with open(file_path,newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Stop.objects.create(
                stop_order = int(row['stop_order']),
                estimated_arrival = timezone.datetime.fromisoformat(row['estimated_arrival']),
                delivered = int(row['delivered']),
                delivery_time = timezone.datetime.fromisoformat(row['delivery_time']),
                order_id = int(row['order_id']),
                route_id = int(row['route_id'])
            )
    print("Stops imported successfully.")

if __name__ == "__main__":
    import_users_from_csv('datasets_users.csv')
    import_orders_from_csv('datasets_orders.csv')
    import_routes_from_csv('dataset_routes.csv')
    import_stops_from_csv('dataset_stops.csv')