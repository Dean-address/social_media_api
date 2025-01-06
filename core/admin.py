from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                )
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ],
            },
        )
    ]


admin.site.register(models.CustomUser, UserAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Post)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.Follow)
