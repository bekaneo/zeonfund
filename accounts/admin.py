from django.contrib import admin
from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'username', 'phone_number', 'is_staff', 'is_active']
