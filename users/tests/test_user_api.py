from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:register")
LOGIN_URL = reverse("user:login")
ME_URL = reverse("user:manage")
LOGOUT_URL = reverse("user:logout")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "test@email.com",
            "password": "testpass",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            user.check_password(payload["password"])
        )
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            "email": "test@email.com",
            "password": "testpass",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
