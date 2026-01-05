from django.contrib import admin
from accounts.models import UserLogin


@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at']

