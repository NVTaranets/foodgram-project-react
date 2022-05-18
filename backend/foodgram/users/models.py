from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .managers import MyUserManager
from .validators import validate_username


class MyUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username must be Alphanumeric',
                code='invalid_username'
            ),
            validate_username,
        ],
        verbose_name='Логин'
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
         )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
         )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    # @property
    # def is_admin(self):
    #     return self.is_staff or self.role == UserRole.ADMIN

    # @property
    # def is_subscribed(self):
    #     return self.role == UserRole.MODERATOR

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
