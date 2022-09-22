from django.contrib import admin
from cases.models import Case, Categories


@admin.register(Case)
class UserAdmin(admin.ModelAdmin):
    model = Case
    list_display = ['title', 'description', 'deadline', 'created_at', 'status']


@admin.register(Categories)
class UserAdmin(admin.ModelAdmin):
    model = Categories
    list_display = ['title', 'slug']
