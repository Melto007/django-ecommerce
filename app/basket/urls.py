from django.urls import (
    path,
    include
)
from basket import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('add', views.BasketView, basename='add')

urlpatterns = [
    path('', include(router.urls))
]
