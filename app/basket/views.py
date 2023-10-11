from rest_framework import (
    viewsets,
    mixins,
    status
)

from .basket import Basket
from core.models import Product
from product.serializers import (
    ProductSerializer
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class BasketView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request):
        basket = Basket(request)
        product_id = request.data.get('product_id', None)
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product)
        serializer = self.get_serializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
