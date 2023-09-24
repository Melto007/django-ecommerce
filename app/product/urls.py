"""product mixins view url"""

from django.urls import path, include
from rest_framework import routers
from product import views

router = routers.DefaultRouter()


router.register('product', views.ProductMixinView, basename='product')


urlpatterns = [
    path('', include(router.urls))
]
