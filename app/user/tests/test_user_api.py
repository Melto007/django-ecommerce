"""
Test for user api
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core import models
import datetime


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
        payload.pop('confirm_password', None)
        create_user(**payload)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', user.password)

    def test_token_create_success(self):
        """Test token create success"""
        payload = {
            'first_name': 'Test name',
            'last_name': 'Test_name',
            'email': 'admin@example.com',
            'password': 'example1234',
            'confirm_password': 'example1234',
        }
        self.assertEqual(payload['password'], payload['confirm_password'])
        payload.pop('confirm_password', None)
        create_user(**payload)

        user = get_user_model().objects.get(email=payload['email'])

        models.UserToken.objects.create(
            user=user.id,
            token='secret',
            expired_at=datetime.datetime.utcnow() +
            datetime.timedelta(days=7)
        )

        get_token = models.UserToken.objects.get(user=user.id)

        self.assertEqual(user.id, get_token.user)


class PrivateUserAPITest(TestCase):
    """Test for private user api"""

    def setup(self):
        self.user = create_user(
            first_name='Test name',
            last_name='Test_name',
            email='admin@example.com',
            password='example1234',
            confirm_password='example1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_token_unauthorized_refresh(self):
        """test user token refresh"""
        payload = {
            'first_name': 'Test name',
            'last_name': 'Test_name',
            'email': 'admin@example.com',
            'password': 'example1234',
        }

        user = create_user(**payload)
        user_id = user.id
        token = 'user_access_token'
        expired_at = '2023-03-2'

        user_token = models.UserToken.objects.filter(
            user=user_id,
            token=token,
            expired_at__gt=expired_at
        ).exists()

        self.assertFalse(user_token)

    def test_user_token_created_success(self):
        """test user token refresh"""
        payload = {
            'first_name': 'Test name',
            'last_name': 'Test_name',
            'email': 'admin@example.com',
            'password': 'example1234',
        }

        user = create_user(**payload)
        user_id = user.id
        token = 'user_access_token'
        expired_at = '2023-03-2'

        models.UserToken.objects.create(
            user=user_id,
            token=token,
            expired_at=expired_at
        )

        res = models.UserToken.objects.get(
            user=user_id
        )

        self.assertEqual(res.user, user_id)
