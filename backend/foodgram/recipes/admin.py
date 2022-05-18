from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (CartShopping, Favorite, Ingredients, Recipes, Subscribe,
                     Tags)


class IngredientInline(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 0


class TagInline(admin.TabularInline):
    model = Recipes.tags.through
    extra = 0


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    model = Ingredients
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name', )
    search_fields = ('name', )
    ordering = ('id', 'name', 'measurement_unit', )
    list_display_links = ('id', 'name',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    model = Tags
    list_display = (
        'id',
        'name',
        'color',
    )
    list_filter = ('name', )
    search_fields = ('name', )
    ordering = ('id', 'name', )
    list_display_links = ('id', 'name', )


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    model = Recipes
    list_display = (
        'id',
        'author',
        'name',
        'favorites_count'
    )
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', )
    ordering = (
        'id',
        'author',
        'name',
    )
    list_display_links = (
        'id',
        'author',
        'name',
    )
    read_only_fields = ('preview',)

    list_per_page = 20

    def favorites_count(self, obj):
        return obj.favorite.count()

    favorites_count.short_description = "Популярность"

    inlines = [IngredientInline, TagInline]


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    model = Subscribe
    list_display = (
        'id',
        'user',
        'author',
    )
    list_filter = ('user', 'author', )
    ordering = (
        'id',
        'user',
        'author',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = (
        'id',
        'user',
        'recipes',
    )
    list_filter = ('user', 'recipes', )
    ordering = (
        'id',
        'user',
        'recipes',
    )

@admin.register(CartShopping)
class CartShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipes'
    )
