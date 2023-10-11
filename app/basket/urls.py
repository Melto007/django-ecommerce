from django.urls import path, include

from rest_framework import routers

router = routers.DefaultRouter()
from basket import views


router.register('add', views.BasketView, basename='add')

urlpatterns = [
    path('', include(router.urls))
]
