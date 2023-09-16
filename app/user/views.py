"""Views for user api"""
from rest_framework import (
    viewsets,
    mixins,
    exceptions,
    status
)
from rest_framework.response import Response
from .serializer import (
    UserSerializer
)
from django.contrib.auth import get_user_model
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
        token = authentication.create_access_token(serializer.data['id'])

        response = {
            'token': token
        }

        return Response(response, status=status.HTTP_201_CREATED)
