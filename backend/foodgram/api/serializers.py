from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Ingredients, Recipes,
                            RecipesIngredients, Tags)

User = get_user_model()


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.subscribe.filter(author=obj).exists()


class RecipesUser(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionsSerializer(RecipesUser):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='author.recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        exclude = (
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "password",
            "groups",
            "user_permissions"
        )

    def get_recipes(self, obj):
        queryset = Recipes.objects.filter(author=obj)
        return RecipesUser(
            queryset,
            many=True
        ).data

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.subscribe.filter(author=obj).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = '__all__'


class RecipesIngredientsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )

    class Meta:
        model = RecipesIngredients

        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipesIngredients
        fields = (
            'id',
            'amount'
        )

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError(
                'Значение Должно быть больше 0.'
            )
        return amount


class ToWriteTagsRecipies(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return TagSerializer(value).data


class RecipesSerializer(serializers.ModelSerializer):
    tags = ToWriteTagsRecipies(
        queryset=Tags.objects.all(),
        many=True,
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientWriteSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time'
                  )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.favorite.filter(
            user=user,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.cart_shoppings.filter(
            user=user,
        ).exists()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.add_ingredients(ingredients_data, recipe)
        recipe.save()
        return recipe

    def validate(self, data):
        ingredients = data.pop('ingredients')
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredients,
                id=ingredient_item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент уже добавлен'
                )
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def add_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            ingredient_instance = get_object_or_404(
                Ingredients,
                pk=ingredient['id'])
            RecipesIngredients.objects.create(
                recipes=recipe,
                ingredients=ingredient_instance,
                amount=amount
            )

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        super().update(instance, validated_data)
        RecipesIngredients.objects.filter(
            recipes=instance
        ).delete()
        self.add_ingredients(ingredients_data, instance)
        instance.save()
        return instance


class RecipesSerializerGet(RecipesSerializer):
    tags = TagSerializer(
        read_only=True,
        many=True
    )
    ingredients = RecipesIngredientsSerializer(
        many=True,
        source='recipesingredients_set',
    )

    class Meta:
        model = Recipes
        fields = '__all__'
