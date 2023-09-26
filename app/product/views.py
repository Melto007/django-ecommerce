from rest_framework import (
    viewsets,
    mixins,
    exceptions,
    status
)
from rest_framework.response import Response
from .serializers import (
    ProductSerializer,
    ProductImageSerializer
)
from config.authentication import (
    JWTAuthentication
)
from core.models import (
    Product,
    ProductImage
)
from config.cloudinary import (
    upload_image
)
import tempfile


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


class ProductImageMixinView(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    authentication_class = [JWTAuthentication]

    def put(self, request):
        """update product image"""
        file = request.FILES.get('image', None)
        product = request.headers.get('product', None)

        instance = self.queryset.get(product=product)

        if not instance:
            raise exceptions.APIException(
                'Invalid Product'
            )

        secure_url = upload_image(file)

        payload = {
            'public_id': secure_url['public_id'],
            'url': secure_url['secure_url']
        }
        serializer = self.get_serializer(
            instance,
            data=payload,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
