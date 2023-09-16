"""
Test for user api
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:register-list')


def create_user(**params):
    """Create user"""
    user = get_user_model().objects.create_user(**params)
    return user


class PublicUserApiTest(TestCase):
    """Testing public user api"""

    def setup(self):
        self.client = APIClient()

    def test_user_create_success(self):
        """Test user create success"""
        payload = {
            'first_name': 'Test name',
            'last_name': 'Test_name',
            'email': 'admin@example.com',
            'password': 'example1234',
            'confirm_password': 'example1234',
        }
        self.assertEqual(payload['password'], payload['confirm_password'])
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
