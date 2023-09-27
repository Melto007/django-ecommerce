"""Product view signals"""
from core.models import (
    ProductImage,
    Product
)
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Product)
def product_image_save(sender, instance, created, **kwargs):
    """save product"""
    if created:
        ProductImage.objects.create(
            product=instance
        )
