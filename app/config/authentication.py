"""authentication for user login"""
import jwt
import datetime
import os
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header
)
from rest_framework import exceptions
from django.contrib.auth import get_user_model


class JWTAuthentication(BaseAuthentication):
    """authentication class for user"""
    def authenticate(self, request):
        """authentication check for user"""
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            user_id = decode_access_token(token)
            user = get_user_model().objects.get(pk=user_id)
            self.user = user
            return {user, None}
        raise exceptions.AuthenticationFailed("Unauthorized")


def create_access_token(id):
    """create token for user login"""
    secret = os.environ.get('ACCESS_SECRET')
    return jwt.encode(
        {
            'user': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'iat': datetime.datetime.utcnow(),
        },
        secret,
        algorithm="HS256",
    )


def decode_access_token(token):
    """decode access token"""
    try:
        payload = jwt.decode(
            token,
            os.environ.get('ACCESS_SECRET'),
            algorithms="HS256",
        )
        return payload['user']
    except Exception as e: # noqa
        raise exceptions.AuthenticationFailed('Unauthenticated')


def create_refresh_token(id):
    """create refresh token for user"""
    secret = os.environ.get('REFRESH_TOKEN')
    return jwt.encode(
        {
            'user': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        },
        secret,
        algorithm="HS256",
    )


def decode_refresh_token(token):
    """decode refresh token for user"""
    secret = os.environ.get('REFRESH_TOKEN')
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms="HS256",
        )
        return payload['user']
    except Exception as e: # noqa
        raise exceptions.AuthenticationFailed('Unauthenticated')
