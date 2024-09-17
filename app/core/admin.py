"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# _ is considered django/python? shorthand to access translation model
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    # first field is a title for grouping the fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']

    # For creating new objects; 'classes' is to use a custom css tag
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


# Passing in UserAdmin allow us to override defaults, e.g. custom sorting,
#  disabling CRUD, etc.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
