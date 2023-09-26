"""
Models
"""
import datetime

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser
)
from django.conf import settings
from django.core.validators import RegexValidator # noqa


class UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")

        if not password:
            raise ValueError("Password field is required")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError("Email field is required")

        if not password:
            raise ValueError("Password field is required")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """model for creating users"""

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    username = None

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()


class TwoFactorAuthentication(models.Model):
    user = models.IntegerField()
    two_factor_auth = models.CharField(max_length=255, default='')
    expired_at = models.DateTimeField(
        default=datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
    )

    def __str__(self):
        return str(self.two_factor_auth)


class UserToken(models.Model):
    user = models.IntegerField()
    token = models.CharField(max_length=255)
    expired_at = models.DateTimeField(default=settings.TOKEN_EXPIES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phonenumber = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    account_verify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    about_item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    product_details = models.CharField(max_length=255)
    stock = models.IntegerField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    public_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)
