from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "is_active",
    )
    list_filter = (
        "name",
        "is_active",
    )
    search_fields = (
        "name",
        "email",
    )
