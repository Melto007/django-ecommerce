from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import (
    Account,
    User
)


@receiver(post_save, sender=User)
def accountSignals(sender, instance, created, **kwargs):
    find_user = Account.objects.filter(user=instance).exists()

    if not find_user and created:
        Account.objects.update_or_create(user=instance)
