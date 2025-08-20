
from django.test import TestCase
from django.db.utils import IntegrityError
from apps.backend.models import User
from apps.backend.services.users import create_user, update_user, delete_user, get_user, get_all_users

class UserServiceTest(TestCase):

    def setUp(self):
        # Initial users for testing
        self.user_data_1 = {
            "name": "Juan Perez",
            "email": "juan.perez@example.com",
            "password_hash": "hashed_password_123"
        }
        self.user_data_2 = {
            "name": "Maria Lopez",
            "email": "maria.lopez@example.com",
            "password_hash": "hashed_password_456"
        }

    # -------------------- CREATION --------------------
    def test_create_user_success(self):
        # Test creating a user with valid data
        user = create_user(self.user_data_1)
        self.assertEqual(user.name, self.user_data_1["name"])
        self.assertEqual(user.email, self.user_data_1["email"])
        self.assertEqual(user.password_hash, self.user_data_1["password_hash"])
        self.assertIsNotNone(user.user_id)
        self.assertEqual(str(user), "Juan Perez < juan.perez@example.com >")

    def test_create_user_duplicate_email(self):
        # Test creating a user with a duplicate email should raise IntegrityError
        create_user(self.user_data_1)
        with self.assertRaises(IntegrityError):
            create_user(self.user_data_1)

    def test_create_user_missing_fields(self):
        # Test creating a user with missing fields should raise KeyError
        incomplete_data = {"name": "No Email"}
        with self.assertRaises(KeyError):
            create_user(incomplete_data)

    # -------------------- UPDATE --------------------
    def test_update_user_success(self):
        # Test updating an existing user
        user = create_user(self.user_data_1)
        updated_data = {"name": "Juan Updated", "password_hash": "new_hash"}
        updated_user = update_user(user.user_id, updated_data)
        self.assertEqual(updated_user.name, "Juan Updated")
        self.assertEqual(updated_user.password_hash, "new_hash")

    def test_update_user_nonexistent(self):
        # Test updating a non-existent user should raise DoesNotExist
        with self.assertRaises(User.DoesNotExist):
            update_user(9999, {"name": "Nonexistent"})

    def test_update_user_duplicate_email(self):
        # Test updating a user email to one that already exists should raise IntegrityError
        user1 = create_user(self.user_data_1)
        user2 = create_user(self.user_data_2)
        with self.assertRaises(IntegrityError):
            update_user(user2.user_id, {"email": self.user_data_1["email"]})

    # -------------------- DELETION --------------------
    def test_delete_user_success(self):
        # Test deleting an existing user
        user = create_user(self.user_data_1)
        result = delete_user(user.user_id)
        self.assertTrue(result)
        with self.assertRaises(User.DoesNotExist):
            get_user(user.user_id)

    def test_delete_user_nonexistent(self):
        # Test deleting a non-existent user should raise DoesNotExist
        with self.assertRaises(User.DoesNotExist):
            delete_user(9999)

    # -------------------- RETRIEVAL --------------------
    def test_get_user_success(self):
        # Test retrieving an existing user
        user = create_user(self.user_data_1)
        fetched_user = get_user(user.user_id)
        self.assertEqual(fetched_user.email, self.user_data_1["email"])

    def test_get_user_nonexistent(self):
        # Test retrieving a non-existent user should raise DoesNotExist
        with self.assertRaises(User.DoesNotExist):
            get_user(9999)

    def test_get_all_users(self):
        # Test retrieving all users
        self.assertEqual(len(get_all_users()), 0)
        user1 = create_user(self.user_data_1)
        user2 = create_user(self.user_data_2)
        users = get_all_users()
        self.assertEqual(len(users), 2)
        self.assertIn(user1, users)
        self.assertIn(user2, users)
