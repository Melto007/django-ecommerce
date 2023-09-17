"""Views for user api"""
from rest_framework import (
    viewsets,
    mixins,
    exceptions,
    status
)
from rest_framework.response import Response
from .serializer import (
    UserSerializer,
    RefreshTokenSerializer,
    UserTokenSerializer
)
from django.contrib.auth import get_user_model
from config.authentication import (
    JWTAuthentication,
    create_access_token,
    decode_access_token,
    create_refresh_token,
    decode_refresh_token
)
from core.models import (
    UserToken
)
import datetime


class UserRegisterView(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request):
        data = request.data
        email = self.request.data['email']
        password = self.request.data['password']
        confirm_password = self.request.data['confirm_password']

        if email[-4:] != 'com' and email[-9:-4] != 'gmail':
            raise exceptions.APIException("Invalid email")

        if password != confirm_password:
            raise exceptions.APIException('Password is not match')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        token = create_access_token(serializer.data['id'])
        refresh_token = create_refresh_token(
            serializer.data['id']
        )

        UserToken.objects.create(
            user=serializer.data['id'],
            token=refresh_token,
            expired_at=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        request.session['refresh_token'] = refresh_token

        response = {
            'token': token,
        }

        return Response(response, status=status.HTTP_201_CREATED)


class LoginMixinView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request):
        """viewset for login user"""
        data = self.request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise exceptions.APIException(
                'Email field is required'
            )

        if password is None:
            raise exceptions.APIException(
                'Password field is required'
            )

        user = self.queryset.filter(
            email=email
        ).first()

        if user is None:
            raise exceptions.APIException(
                'Invalid Credential'
            )

        if not user.check_password(password):
            raise exceptions.APIException(
                'Invalid Credential - password'
            )

        token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(
            user=user.id,
            token=refresh_token,
            expired_at=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        request.session['refresh_token'] = refresh_token

        response = {
            'token': token
        }

        return Response(response, status=status.HTTP_200_OK)


class LogoutMixinView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserTokenSerializer
    queryset = UserToken.objects.all()

    def create(self, request):
        """Logout user view"""
        try:
            refresh_token = request.session.get(
                'refresh_token',
                None
            )
            self.queryset.filter(
                token=refresh_token
            ).delete()

            del request.session['refresh_token']

            response = {
                'message': 'Logout Successfully'
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e: # noqa
            raise exceptions.APIException('Unauthenticated')


class RefreshTokenMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = RefreshTokenSerializer
    queryset = UserToken.objects.all()

    def create(self, request):
        """generate refresh token"""
        refresh_token = request.session.get(
            'refresh_token',
            None
        )
        id = decode_refresh_token(refresh_token)

        if not self.queryset.filter(
            user=id,
            token=refresh_token,
            expired_at__gt=datetime.datetime.now(
                tz=datetime.timezone.utc
            )
        ).exists():
            self.queryset.filter(
                user=id,
                token=refresh_token
            ).delete()
            raise exceptions.AuthenticationFailed('Unauthenticated')

        token = create_access_token(id)

        response = {
            'token': token
        }
        return Response(response, status=status.HTTP_201_CREATED)
