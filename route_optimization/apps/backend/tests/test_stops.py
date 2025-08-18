# pylint: disable=import-error
from django.test import TestCase
from apps.backend.models import Stop # important
from .utils.test_helpers import create_stop


class StopModelTest(TestCase):
    def setUp(self):
        self.stop = create_stop()

    def test_stop_creation(self):
        self.assertFalse(self.stop.delivered)
