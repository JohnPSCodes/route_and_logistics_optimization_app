# pylint: disable=import-error
from django.test import TestCase
from apps.backend.models import Route # important
from .utils.test_helpers import create_route, create_user
from django.utils import timezone

class RouteModelTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_route_creation(self):
        route = create_route(user=self.user)
        self.assertEqual(route.status, 'planned')
        self.assertEqual(str(route), f"{route.name} ({route.planned_date})")

    def test_route_creation_with_custom_date(self):
        custom_date = timezone.now().date() + timezone.timedelta(days=5)
        route = create_route(user=self.user, planned_date=custom_date)
        self.assertEqual(route.planned_date, custom_date)
