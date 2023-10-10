from django.contrib import admin

from core import models

admin.site.register(models.User)
admin.site.register(models.UserToken)
admin.site.register(models.TwoFactorAuthentication)
admin.site.register(models.Account)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.DeliveryOptions)
admin.site.register(models.PaymentSelection)
