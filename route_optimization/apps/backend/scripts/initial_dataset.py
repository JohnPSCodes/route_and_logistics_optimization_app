import os
import django
import csv
from django.utils import timezone
from datetime import timedelta

# Django Config (adjust the path based on your project)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'route_optimization.settings')
django.setup()

from apps.backend.models import User, Order

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

if __name__ == "__main__":
    import_users_from_csv('datasets_users.csv')
    import_orders_from_csv('datasets_orders.csv')
