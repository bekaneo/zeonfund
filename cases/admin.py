from django.contrib import admin
from cases.models import Case, Categories, Images


class CaseImageInLine(admin.TabularInline):
    model = Images
    max_num = 10
    min_num = 1


class CaseAdmin(admin.ModelAdmin):
    model = Case
    inlines = [CaseImageInLine, ]
    list_display = ['title']


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    model = Categories
    list_display = ['title', 'slug']


admin.site.register(Case, CaseAdmin)
