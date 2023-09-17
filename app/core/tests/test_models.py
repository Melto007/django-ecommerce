"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
import datetime
from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_user_register_create(self):
        """Test your details create success &&
            or not"""
        email = 'user@example.com'
        password = 'examplepassword'

        user = get_user_model().objects.create_user(
            email,
            password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """Test for normalize email"""

        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(
                email,
                'sample123'
            )
            self.assertEqual(user.email, expected)

    def test_superuser(self):
        """Test super user"""

        email = 'user@example.com'
        password = 'examplepassword'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_token_create_success(self):
        """Test user token is created or not"""

        email = 'user@example.com'
        password = 'examplepassword'
        token = 'secret'
        get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        res = get_user_model().objects.get(
            email=email
        )

        res = models.UserToken.objects.create(
            token=token,
            user=res.id,
            expired_at=datetime.datetime.utcnow()
        )
        self.assertEquals(res.token, token)

    def test_accout_create_success(self):
        """create account success"""

        email = 'user@example.com'
        password = 'examplepassword'
        get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        res = get_user_model().objects.get(
            email=email
        )

        payload = {
            'phonenumber': 7483748832,
            'billing_address': 'some where',
            'shipping_address': 'temp address',
            'location': 'some where',
            'account_verify': False,
            'created_at': '2023-03-23',
            'status': True
        }

        res = models.Account.objects.create(
            user=res,
            **payload
        )

        self.assertEqual(res.phonenumber, payload['phonenumber'])
