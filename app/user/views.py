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
    UserTokenSerializer,
    TwoFactorAuthSerializer,
    AccountSerializer
)
from django.contrib.auth import get_user_model
from config.authentication import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)
from core.models import (
    UserToken,
    TwoFactorAuthentication,
    Account
)
import datetime
import pyotp
from .tasks import mail_sharedTask
from config import authentication


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

        response = {
            'message': "Registered Successfully",
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

        user_id = user.id
        email = user.email

        mail_sharedTask.apply_async(args=[user_id, email], queue='celery')

        request.session['id'] = user_id

        response = {
            'message': 'code is send to mail'
        }

        return Response(response, status=status.HTTP_201_CREATED)


class TwoFactorAuthMixinView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TwoFactorAuthSerializer
    queryset = TwoFactorAuthentication.objects.all()

    def create(self, request):
        user_id = request.session.get('id', None)
        data = self.request.data
        code = data.get('code', None)

        if code is None:
            raise exceptions.APIException(
                'Authentication Code is required - code'
            )

        if user_id is None:
            raise exceptions.AuthenticationFailed(
                'Invalid credential - user id'
            )

        check_code = self.queryset.filter(
            user=user_id,
            expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).first()

        if not check_code:
            raise exceptions.AuthenticationFailed(
                'Invalid credentical - check code'
            )

        secret = check_code.two_factor_auth
        totp = pyotp.TOTP(secret, interval=120)

        if not totp.verify(code):
            raise exceptions.AuthenticationFailed(
                'Invalid credential - secret'
            )

        user = check_code.user

        token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        UserToken.objects.create(
            user=user,
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
            del request.session['id']

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


class AccountMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    authentication_classes = [authentication.JWTAuthentication]

    def get_queryset(self):
        user = self.request.session.get('id', None)
        if user:
            return self.queryset.filter(user=user)
