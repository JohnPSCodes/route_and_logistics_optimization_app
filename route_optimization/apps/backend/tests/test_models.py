from django.test import TestCase
from apps.backend.models import Order, User, Route, Stop
from django.utils import timezone
from datetime import timedelta


class OrderModelTests(TestCase):
    def test_order_creation(self):
        now = timezone.now()
        order = Order.objects.create(
            customer_name="Test Customer",
            address="123 Main St",
            latitude=40.7128,
            longitude=-74.0060,
            priority=2,
            delivery_window_start=now,
            delivery_window_end=now + timedelta(hours=2),
        )
        self.assertEqual(order.status, 'pending')  # Default
        self.assertEqual(order.customer_name, "Test Customer")
    
    def test_order_status_update(self):
        now = timezone.now()
        order = Order.objects.create(
            customer_name="Test Customer",
            address="123 Main St",
            latitude=40.7128,
            longitude=-74.0060,
            priority=2,
            delivery_window_start=now,
            delivery_window_end=now + timedelta(hours=2),
        )
        # Update status to 'assigned'
        order.status = 'assigned'
        order.save()

        # Fetch again from DB to confirm persistence
        updated_order = Order.objects.get(pk=order.pk)
        self.assertEqual(updated_order.status, 'assigned')

        # Update status to 'delivered'
        updated_order.status = 'delivered'
        updated_order.save()

        updated_order = Order.objects.get(pk=order.pk)
        self.assertEqual(updated_order.status, 'delivered')

class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            name="Juan Perez",
            email="juan.perez@example.com",
            password_hash="hashed_password_123"
        )
        self.assertEqual(user.name, "Juan Perez")
        self.assertEqual(user.email, "juan.perez@example.com")
        self.assertEqual(user.password_hash, "hashed_password_123")
        self.assertIsNotNone(user.user_id)  # Generated automatically
        self.assertEqual(str(user), "Juan Perez < juan.perez@example.com")

class RouteModelTests(TestCase):
    def setUp(self):
        # We create a user to relate it to Route
        self.user = User.objects.create(
            name="Test User",
            email="testuser@example.com",
            password_hash="fakehash"
        )

    def test_route_creation(self):
        route = Route.objects.create(
            name="Route Test",
            planned_date=timezone.now().date(),
            created_by=self.user,
        )
        self.assertEqual(route.status, 'planned')  # Default value
        self.assertEqual(str(route), f"{route.name} ({route.planned_date})")

class StopModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="testuser@example.com",
            password_hash="fakehash"
        )
        self.route = Route.objects.create(
            name="Route Test",
            planned_date=timezone.now().date(),
            created_by=self.user,
        )
        self.order1 = Order.objects.create(
            customer_name="Customer 1",
            address="Address 1",
            latitude=10.0,
            longitude=20.0,
            delivery_window_start=timezone.now(),
            delivery_window_end=timezone.now() + timezone.timedelta(hours=2),
            priority=1,
        )
        self.order2 = Order.objects.create(
            customer_name="Customer 2",
            address="Address 2",
            latitude=30.0,
            longitude=40.0,
            delivery_window_start=timezone.now(),
            delivery_window_end=timezone.now() + timezone.timedelta(hours=2),
            priority=1,
        )
        # Create stops linked to the route and orders
        self.stop1 = Stop.objects.create(
            route=self.route,
            order=self.order1,
            stop_order=1,
            estimated_arrival=timezone.now() + timezone.timedelta(hours=1)
        )
        self.stop2 = Stop.objects.create(
            route=self.route,
            order=self.order2,
            stop_order=2,
            estimated_arrival=timezone.now() + timezone.timedelta(hours=2)
        )
    def test_cascade_delete_route_removes_stops(self):
        # Before deleting the route, stops exist
        self.assertEqual(Stop.objects.filter(route=self.route).count(), 2)

        # Delete the route
        route_id = self.route.id
        self.route.delete()

        # After deletion, stops linked to this route should be deleted too
        self.assertEqual(Stop.objects.filter(route_id=route_id).count(), 0)

    def test_access_stops_from_route(self):
        # Access stops through related_name 'stops'
        stops = self.route.stops.all()
        self.assertEqual(stops.count(), 2)
        self.assertIn(self.stop1, stops)
        self.assertIn(self.stop2, stops)

    def test_stop_creation(self):
        stop = Stop.objects.create(
            route=self.route,
            order=self.order1,
            stop_order=1,
            estimated_arrival=timezone.now() + timezone.timedelta(hours=1)
        )
        self.assertFalse(stop.delivered)  # Default
        expected_str = f"Stop {stop.stop_order} - Route: {self.route.name} - Order ID: {stop.order.id}"
        self.assertEqual(str(stop), expected_str)