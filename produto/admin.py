from django.contrib import admin
from .models import Produto, Variacao

from django import forms

# # Register your models here.
# admin.site.register(Produto)

class VariacaoInLine(admin.TabularInline):
    model = Variacao
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'slug', 'preco_marketing', 'preco_marketing_promocional', 'tipo',)
    list_display_links = ('id', 'nome', 'slug', 'preco_marketing', 'preco_marketing_promocional', 'tipo',)
    search_fields = ('nome', 'slug', 'preco_marketing', 'preco_marketing_promocional', 'tipo',)
    inlines = [
        VariacaoInLine,
    ]

@admin.register(Variacao)
class VariacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'nome', 'preco', 'preco_promocional', 'estoque',)
    list_display_links = ('produto', 'nome', 'preco', 'preco_promocional', 'estoque',)
    search_fields = ('produto', 'nome', 'preco', 'preco_promocional', 'estoque',)
