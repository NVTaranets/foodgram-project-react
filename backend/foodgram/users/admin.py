from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import MyUser


class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = (
        'id',
        'email',
        'username',
        'is_staff',
        'is_active',
        'is_superuser'
    )
    list_display_links = ('id', 'email', )
    list_filter = ('email', 'username', )
    fieldsets = (
        (None, {'fields': (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
             )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(MyUser, MyUserAdmin)
