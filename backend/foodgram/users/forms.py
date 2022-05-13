from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import MyUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MyUser
        fields = ('email', 'username', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ('email',)
