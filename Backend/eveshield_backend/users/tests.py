from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

# ========= TEST CASES FOR USER REGISTRATION, LOGIN & LOGOUT ========


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.valid_phone = "+254712345678"
        self.valid_password = "password123"
        self.register_url = '/api/users/auth/register/'
        self.login_url = '/api/users/auth/login/'
        self.logout_url = '/api/users/auth/logout/'

    def test_register_user(self):
        data = {
            "phone_number": self.valid_phone,
            "username": "Test User",
            "password": self.valid_password
        }
        response = self.client.post(self.register_url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        # First, register the user
        self.client.post(self.register_url, {
            "phone_number": self.valid_phone,
            "username": "Test User",
            "password": self.valid_password
        })

        # Then log in using phone number
        response = self.client.post(self.login_url, {
            "phone_number": self.valid_phone,
            "password": self.valid_password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_user(self):
        # Register and log in the user
        self.client.post(self.register_url, {
            "phone_number": self.valid_phone,
            "username": "Test User",
            "password": self.valid_password
        })

        login_response = self.client.post(self.login_url, {
            "phone_number": self.valid_phone,
            "password": self.valid_password
        })

        access_token = login_response.data["tokens"]["access"]
        refresh_token = login_response.data["tokens"]["refresh"]

        # Set the auth header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Logout with refresh token
        response = self.client.post(self.logout_url, {
            "refresh": refresh_token
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
