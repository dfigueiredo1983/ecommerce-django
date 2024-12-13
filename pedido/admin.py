from django.contrib import admin
from .models import Pedido, ItemPedido
# Register your models here.

# admin.site.register(Pedido)
# admin.site.register(ItemPedido)

class ItemPedidoInLine(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status',)
    list_display_links = ('id', 'user', 'status',)
    search_fields = ('nome', 'user', 'status',)
    inlines = [
        ItemPedidoInLine,
    ]

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'produto_id', 'variacao', 'variacao_id', 'preco', 'preco_promocional', 'quantidade', 'imagem',)
    list_display_links = ('pedido', 'produto_id', 'variacao', 'variacao_id', 'preco', 'imagem',)
    search_fields = ('pedido', 'produto_id', 'variacao', 'variacao_id', 'preco', 'imagem',)
