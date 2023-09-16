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


class UserRegisterView(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        password = self.request.data['password']
        confirm_password = self.request.data['confirm_password']

        if password != confirm_password:
            raise exceptions.APIException('Password is not match')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
