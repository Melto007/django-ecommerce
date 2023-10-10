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
from django.utils.translation import gettext_lazy as _


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

    @property
    def product(self):
        return self.productimage_set.all()


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


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="order_user"
    )
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class DeliveryOptions(models.Model):
    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery")
    ]
    delivery_name = models.CharField(
        verbose_name=_("delivery_name"),
        help_text=_("Required"),
        max_length=255
    )
    delivery_price = models.DecimalField(
        verbose_name=_("delivery_price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 to 999.99"),
            },
        },
        max_digits=5,
        decimal_places=2
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("delivery_method"),
        help_text=_("Required"),
        max_length=255
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("delivery_timeframe"),
        help_text=_("Required"),
        max_length=255
    )
    delivery_window = models.CharField(
        verbose_name=_("delivery_window"),
        help_text=_("Required"),
        max_length=255
    )
    order = models.IntegerField(
        verbose_name=_("list_order"),
        help_text=_("Required")
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.delivery_name


class PaymentSelection(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Required"),
        max_length=255
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name
