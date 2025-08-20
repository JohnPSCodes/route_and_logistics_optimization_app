
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from apps.backend.models import Order
from .utils.test_helpers import create_order
from apps.backend.services.orders import (
    create_order,
    update_order,
    delete_order,
    get_order,
    get_all_orders
)

class OrderModelTest(TestCase):

    def test_order_creation(self):
        """Test basic order creation with default status and priority"""
        order = create_order()
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.customer_name, "Test Customer")
        self.assertEqual(order.priority, 1)

    def test_order_status_update(self):
        """Test updating order status"""
        order = create_order()
        order.status = 'assigned'
        order.save()
        updated_order = Order.objects.get(pk=order.pk)
        self.assertEqual(updated_order.status, 'assigned')

        # Update to delivered
        order.status = 'delivered'
        order.save()
        updated_order = Order.objects.get(pk=order.pk)
        self.assertEqual(updated_order.status, 'delivered')

    def test_order_str_representation(self):
        """Test __str__ method"""
        order = create_order()
        expected_str = f"Order {order.id} - {order.customer_name}"
        self.assertEqual(str(order), expected_str)

    def test_order_priority_default(self):
        """Test that priority defaults to 1 if not provided"""
        data = {
            "customer_name": "Priority Test",
            "address": "123 Test St",
            "latitude": 0.0,
            "longitude": 0.0,
            "delivery_window_start": datetime.now(),
            "delivery_window_end": datetime.now() + timedelta(hours=1)
        }
        order = Order.objects.create(**data)
        self.assertEqual(order.priority, 1)

    def test_delivery_window_validation(self):
        """Test that delivery_window_end cannot be before delivery_window_start"""
        start = datetime.now()
        end = start - timedelta(hours=1)
        data = {
            "customer_name": "Invalid Window",
            "address": "456 Test Ave",
            "latitude": 0.0,
            "longitude": 0.0,
            "priority": 1,
            "delivery_window_start": start,
            "delivery_window_end": end
        }
        order = Order(**data)
        with self.assertRaises(ValidationError):
            order.full_clean()  # Django model validation

    def test_invalid_status_assignment(self):
        """Test that assigning an invalid status raises an error"""
        order = create_order()
        order.status = 'cancelled'  # invalid
        with self.assertRaises(ValidationError):
            order.full_clean()

class OrderServiceTest(TestCase):

    def setUp(self):
        """Common data for tests"""
        self.base_data = {
            "customer_name": "Service Test",
            "address": "123 Service St",
            "latitude": 10.123456,
            "longitude": -70.654321,
            "priority": 2,
            "delivery_window_start": datetime.now(),
            "delivery_window_end": datetime.now() + timedelta(hours=2),
        }

    def test_create_order_complete(self):
        """Create an order with all data provided"""
        order = create_order(self.base_data)
        self.assertEqual(order.customer_name, self.base_data["customer_name"])
        self.assertEqual(order.priority, self.base_data["priority"])
        self.assertEqual(order.status, "pending")

    def test_create_order_with_defaults(self):
        """Create an order with partial data, should set default status and priority"""
        data = self.base_data.copy()
        data.pop("priority")
        order = create_order(data)
        self.assertEqual(order.priority, 1)
        self.assertEqual(order.status, "pending")

    def test_update_order_fields(self):
        """Update multiple fields of an order"""
        order = create_order(self.base_data)
        new_data = {
            "customer_name": "Updated Customer",
            "priority": 5,
            "status": "assigned"
        }
        updated_order = update_order(order.id, new_data)
        self.assertEqual(updated_order.customer_name, "Updated Customer")
        self.assertEqual(updated_order.priority, 5)
        self.assertEqual(updated_order.status, "assigned")

    def test_delete_order(self):
        """Delete an order"""
        order = create_order(self.base_data)
        result = delete_order(order.id)
        self.assertTrue(result)
        with self.assertRaises(Order.DoesNotExist):
            get_order(order.id)

    def test_get_order(self):
        """Retrieve a single order by ID"""
        order = create_order(self.base_data)
        fetched_order = get_order(order.id)
        self.assertEqual(fetched_order.id, order.id)
        self.assertEqual(fetched_order.customer_name, order.customer_name)

    def test_get_all_orders(self):
        """Retrieve all orders"""
        order1 = create_order(self.base_data)
        order2 = create_order(self.base_data)
        all_orders = get_all_orders()
        self.assertEqual(len(all_orders), 2)
        self.assertIn(order1, all_orders)
        self.assertIn(order2, all_orders)

    def test_invalid_delivery_window_on_create(self):
        """Attempt to create order with invalid delivery window"""
        data = self.base_data.copy()
        data["delivery_window_end"] = data["delivery_window_start"] - timedelta(hours=1)
        order = Order(**data)
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_invalid_status_update(self):
        """Attempt to update an order with invalid status"""
        order = create_order(self.base_data)
        order.status = "cancelled"
        with self.assertRaises(ValidationError):
            order.full_clean()