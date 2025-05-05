from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


# Register your models here.


class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = (
   "id", "email","first_name","last_name", "is_active","is_staff","is_superuser" )
    list_display_links = ("first_name", "last_name","email","id")
    fieldsets = (
        (None, {"fields": ( "password",)}),
        (_("Personal info"), {"fields": (
         "email","first_name", "last_name", 'profile_image',
        )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ( 'profile_picture', 'address',)
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)