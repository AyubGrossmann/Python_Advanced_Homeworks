from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register(self):
        response = self.client.post("/api/auth/register/", {
            "username": "student",
            "email": "student@example.com",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="student")
        self.assertNotEqual(user.password, "StrongPass123!")

    def test_passwords_must_match(self):
        response = self.client.post("/api/auth/register/", {
            "username": "student",
            "email": "student@example.com",
            "password": "StrongPass123!",
            "password_confirm": "OtherPass123!",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_sets_httponly_cookies(self):
        User.objects.create_user(
            username="student", email="student@example.com",
            password="StrongPass123!"
        )
        response = self.client.post("/api/auth/login/", {
            "username_or_email": "student",
            "password": "StrongPass123!",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.cookies["access_token"]["httponly"])
        self.assertTrue(response.cookies["refresh_token"]["httponly"])
