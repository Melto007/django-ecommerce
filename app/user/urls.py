"""URLS for user api"""
from django.urls import (
    path,
    include
)
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('register', views.UserRegisterView, basename='register')
router.register('account', views.AccountMixinView, basename='account')

app_name = 'user'

urlpatterns = [
    path('', include(router.urls))
]
