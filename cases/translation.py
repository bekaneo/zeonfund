from modeltranslation.translator import register, TranslationOptions
from .models import Case


@register(Case)
class CaseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
