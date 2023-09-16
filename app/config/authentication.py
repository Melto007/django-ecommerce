"""authentication for user login"""
import jwt
import datetime
import os


def create_access_token(id):
    """create token for user login"""
    secret = os.environ.get('JWT_SECRET')
    return jwt.encode(
        {
            'user': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'iat': datetime.datetime.utcnow(),
        },
        secret,
        algorithm="HS256",
    )
