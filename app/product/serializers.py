from core.models import (
    Product
)
from rest_framework import (
    serializers
)


class ProductSerializer(serializers.ModelSerializer):
    """product serializer"""
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'about_item',
            'description', 'product_details', 'stock',
            'status'
        ]
