from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

User = get_user_model()


class UserAdmin(BaseUserAdmin):

    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_active", "is_superuser")
    fieldsets = (
        (
            "User information",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password",
                    "logo",
                )
            },
        ),
        ("Permissions", {"fields": ("groups", "user_permissions", "is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            "Create new user",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    readonly_fields = ("timestamp",)
    search_fields = ("email", "username")
    ordering = ("email", "username")
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
