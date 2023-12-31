"""URLS for user api"""
from django.urls import (
    path,
    include
)
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('register', views.UserRegisterView, basename='register')
router.register('refresh', views.RefreshTokenMixin, basename='refresh')
router.register('logout', views.LogoutMixinView, basename='logout')
router.register('login', views.LoginMixinView, basename='login')
router.register(
    'two-factor-auth',
    views.TwoFactorAuthMixinView,
    basename='two-factor-auth'
)
router.register('account', views.AccountMixinView, basename='account')

app_name = 'user'

urlpatterns = [
    path('', include(router.urls))
]
