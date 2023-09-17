"""Serializer for user api"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import (
    Account
)


class UserSerializer(serializers.ModelSerializer):
    """serializer for user"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for account"""

    class Meta:
        model = Account
        fields = [
            'id', 'phonenumber',
            'billing_address', 'shipping_address', 'location',
            'account_verify', 'status'
        ]
