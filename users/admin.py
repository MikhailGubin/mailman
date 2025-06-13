from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id","email", "avatar", "phone_number", "country"]
    list_filter = ("id","email", "avatar", "phone_number", "country")
    search_fields = ("id","email", "avatar", "phone_number", "country")
