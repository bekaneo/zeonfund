from django.contrib import admin
from cases.models import Case, Categories


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    model = Case
    list_display = ['title', 'description', 'category', 'created_at', 'status']


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    model = Categories
    list_display = ['title', 'slug']

