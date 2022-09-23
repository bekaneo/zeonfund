from django.contrib import admin
from cases.models import Case, Categories, Images
from modeltranslation.admin import TranslationAdmin


class CaseImageInLine(admin.TabularInline):
    model = Images
    max_num = 10
    min_num = 1


class CaseAdmin(TranslationAdmin):
    model = Case
    inlines = [CaseImageInLine, ]
    list_display = ['title']


@admin.register(Categories)
class CategoryAdmin(TranslationAdmin):
    model = Categories
    list_display = ['title', 'slug']


admin.site.register(Case, CaseAdmin)
