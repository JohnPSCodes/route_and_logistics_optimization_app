# pylint: disable=import-error
from django.test import TestCase
from apps.backend.models import User # important
from .utils.test_helpers import create_user

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = create_user(name="Juan Perez", email="juan.perez@example.com", password_hash="hashed_password_123")
        self.assertEqual(user.name, "Juan Perez")
        self.assertEqual(user.email, "juan.perez@example.com")
        self.assertEqual(user.password_hash, "hashed_password_123")
        self.assertIsNotNone(user.user_id)
        self.assertEqual(str(user), "Juan Perez < juan.perez@example.com")
