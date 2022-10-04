from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        if [form.cleaned_data['is_main'] for form in self.forms if form.cleaned_data].count(True) == 1:
            return super().clean()  # вызываем базовый код переопределяемого метода
        else:
            raise ValidationError('Нужно выбрать один и только один раздел')


class ArticleScopeInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset
    extra = 3


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ordering = ['name']
