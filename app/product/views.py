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
    upload_image,
    destroy_image
)


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """product mixins"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    lookup_field = 'pk'

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

    def destroy(self, request, pk, **kwargs):
        res = self.queryset.get(id=pk)

        if not res:
            raise exceptions.APIException(
                'Product does not exists'
            )

        res.delete()

        message = {
            'message': 'Item deleted'
        }

        return Response(message)


class ProductImageMixinView(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    authentication_class = [JWTAuthentication]

    def list(self, request):
        res = self.queryset.all()
        serializer = self.get_serializer(res, many=True)
        return Response(serializer.data)

    def put(self, request):
        """update product image"""
        file = request.FILES.get('image', None)
        product = request.headers.get('product', None)

        if file is None:
            raise exceptions.APIException(
                'File field is required'
            )

        instance = self.queryset.get(product=product)

        if not instance:
            raise exceptions.APIException(
                'Invalid Product'
            )

        if instance.public_id:
            destroy_image(instance.public_id)

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
