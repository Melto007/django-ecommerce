from core.models import (
    Product,
    ProductImage
)
from rest_framework import (
    serializers
)


class ProductImageSerializer(serializers.ModelSerializer):
    """Product Image Upload Serializer"""

    class Meta:
        model = ProductImage
        fields = [
            'id', 'public_id', 'url', 'product'
        ]
        extra_kwargs = {
            'public_id': {'write_only': True},
        }


class ProductSerializer(serializers.ModelSerializer):
    """product serializer"""
    product = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'about_item',
            'description', 'product_details', 'stock',
            'status', 'product'
        ]
