from django.contrib import admin

from .models import Carrito, DetallePedido, ItemCarrito, Pago, Pedido


class DetalleInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("folio", "usuario", "estado", "total", "creado")
    list_filter = ("estado",)
    inlines = [DetalleInline]


admin.site.register([Carrito, ItemCarrito, Pago])