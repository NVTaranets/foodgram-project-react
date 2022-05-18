from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        max_length=64,
        blank=False,
        verbose_name='Единица измерения'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient')
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tags(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Имя'
    )
    color = ColorField(
        default='#FF0000',
        blank=False,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        'Slug тега',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField(
        'Текст рецепта',
        help_text='Введите текст рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipesIngredients',
        related_name='ingredients',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipesTags',
        related_name='tags',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='Время должно быть > 0!'),
        ],
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class RecipesIngredients(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='Колличество должно быть > 0!'),
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.recipes} {self.ingredients}'


class RecipesTags(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'{self.recipes} {self.tags}'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribe',
        verbose_name='Кто подписался'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='on_subscribe',
        verbose_name='На кого подписались'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='Unique subscribe'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='Subscribe not for yourself!'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )

    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'],
                name='unique favorite'
            )
        ]


class CartShopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_shoppings',
        verbose_name='Пользователь, добавивший рецепт в корзину'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='cart_shoppings',
        verbose_name='Рецепт в корзине пользователя'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipes'),
                name='Рецепт уже находится в корзине!'
            )
        ]
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзинах'

    def __str__(self) -> str:
        return f'{self.user.username} {self.recipes.name}'
