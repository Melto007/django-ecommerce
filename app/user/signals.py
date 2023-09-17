from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core.models import (
    Account
)


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    """create account in the database"""
    if created:
        Account.objects.create(
            user=instance
        )
