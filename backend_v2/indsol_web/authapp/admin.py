from authapp.models import Users
from django.contrib import admin


# Authapp
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "is_staff",
        "is_manager",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "username",
        "is_staff",
        "is_manager",
        "created_at",
        "updated_at",
    )
    exclude = [
        "groups",
        "first_name",
        "last_name",
        "email",
        "user_permissions",
        "last_login",
    ]
    search_fields = ("name",)


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


admin.site.register(Users, UsersAdmin)
