"""Product view signals"""
from core.models import (
    ProductImage,
    Product
)
from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_delete
)
from config.cloudinary import (
    destroy_image
)


@receiver(post_save, sender=Product)
def product_image_save(sender, instance, created, **kwargs):
    """save product"""
    if created:
        ProductImage.objects.create(
            product=instance
        )


@receiver(pre_delete, sender=Product)
def product_image_delete(sender, instance, **kwargs):
    """delete product"""
    if instance:
        res = ProductImage.objects.filter(product=instance).first()
        destroy_image(res.public_id)
