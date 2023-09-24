from rest_framework import (
    viewsets,
    mixins,
    exceptions,
    status
)
from rest_framework.response import Response
from .serializers import (
    ProductSerializer
)
from config.authentication import (
    JWTAuthentication
)
from core.models import (
    Product
)


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """product mixins"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]

    def perform_create(self, request):
        user = self.request.user
        name = request.data.get('name', None)

        product_name = self.queryset.filter(
            name=name
        ).exists()

        if product_name:
            raise exceptions.APIException(
                'Product name already exists'
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
