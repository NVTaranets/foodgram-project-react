from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, MyUserViewSet, RecipesViewSet, TagViewSet

v1 = DefaultRouter()
v1.register('users', MyUserViewSet, basename='users')
v1.register('tags', TagViewSet)
v1.register('ingredients', IngredientViewSet)
v1.register('recipes', RecipesViewSet)

urlpatterns = [
    path('', include(v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
