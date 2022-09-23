from modeltranslation.translator import register, TranslationOptions
from .models import Case, Categories


@register(Case)
class CaseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('title',)
