# pylint: disable=import-error
from django.test import TestCase
from apps.backend.models import Order
from .utils.test_helpers import create_order

class OrderModelTest(TestCase):
    def test_order_creation(self):
        order = create_order()
        self.assertEqual(order.status,'pending')
        self.assertEqual(order.customer_name,"Test Customer")
    
    def test_order_status_update(self):
        order = create_order()
        order.status = 'assigned'
        order.save()
        updated_order =Order.objects.get(pk=order.pk)
        self.assertEqual(updated_order.status,'assigned')
