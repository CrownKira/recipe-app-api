from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

# to convert string in python to human readable text
# so that it gets passed through the translation engine

from core import models


class UserAdmin(BaseUserAdmin):
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
    # The ModelAdmin class is the representation of a model in the admin
    # interface. Usually, these are stored in a file named admin.py in your
    # application.
    # change the ordering to be id
    # list them by email and name, order them by id
    # In the preceding example, the ModelAdmin class
    # doesn’t define any custom values (yet).
    # As a result, the default admin interface will be
    # provided. If you are happy with the
    # default admin interface, you don’t need to define
    # a ModelAdmin object at all –
    # you can register the model class without providing
    # a ModelAdmin description
    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        # None is the title here
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
