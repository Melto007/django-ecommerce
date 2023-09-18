"""Serializer for user api"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import (
    UserToken,
    TwoFactorAuth
)


class UserSerializer(serializers.ModelSerializer):
    """serializer for user"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserTokenSerializer(serializers.ModelSerializer):
    """Serializer for token"""

    class Meta:
        model = UserToken
        fields = ['id', 'user', 'token', 'expired_at']


class TwoFactorSerializer(serializers.ModelSerializer):
    """serializer for two factor authentication"""

    class Meta:
        model = TwoFactorAuth
        fields = ['id', 'user', 'token', 'expired_at']
        read_only_fields = ['id']


class RefreshTokenSerializer(UserTokenSerializer):
    class Meta(UserTokenSerializer.Meta):
        model = UserTokenSerializer.Meta.model
        fields = UserTokenSerializer.Meta.fields
