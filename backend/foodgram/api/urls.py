from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

v1 = DefaultRouter()
v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(v1.urls)),
]
