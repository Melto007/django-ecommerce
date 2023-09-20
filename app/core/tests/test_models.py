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

    def test_account_create_success(self):
        """Test account create success"""

        email = 'user@example.com'
        password = 'examplepassword'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        payload = {
            'phonenumber': 7849383394,
            'billing_address': 'no where',
            'shipping_address': 'some where',
            'location': 'what ever',
            'account_verify': True,
            'created_at': '1990-01-30',
            'updated_at': '2039-01-03',
            'status': False
        }

        if not models.Account.objects.filter(user=user).exists():
            models.Account.objects.create(user=user, **payload)
        account = models.Account.objects.filter(
            user=user
        ).first()

        self.assertEqual(account.user, user)
