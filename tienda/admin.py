from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Carrito,
    Categoria,
    DetalleCarrito,
    DetallePedido,
    Direccion,
    Pago,
    Pedido,
    Producto,
    Usuario,
)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'telefono', 'rol',
        'is_staff', 'is_active'
    )
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telefono')
    fieldsets = UserAdmin.fieldsets + (
        ('Datos de LapZone', {'fields': ('telefono', 'rol')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos de LapZone', {'fields': ('first_name', 'last_name', 'email', 'telefono', 'rol')}),
    )


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'calle', 'sector', 'ciudad', 'es_principal')
    list_filter = ('ciudad', 'es_principal')
    search_fields = ('usuario__username', 'calle', 'sector')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'categoria', 'precio', 'stock', 'activo')
    list_filter = ('categoria', 'marca', 'activo')
    search_fields = ('nombre', 'marca', 'descripcion', 'especificaciones')
    list_editable = ('precio', 'stock', 'activo')
    ordering = ('nombre',)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_creacion')
    search_fields = ('usuario__username',)


@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')
    search_fields = ('carrito__usuario__username', 'producto__nombre')


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unitario')
    can_delete = False


class PagoInline(admin.StackedInline):
    model = Pago
    extra = 0
    max_num = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo_entrega', 'estado', 'total', 'fecha_pedido')
    list_filter = ('tipo_entrega', 'estado', 'fecha_pedido')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')
    list_editable = ('estado',)
    # Los filtros por fecha funcionan sin las tablas de zonas horarias de MySQL.
    # date_hierarchy usa CONVERT_TZ y falla en instalaciones locales sin esas tablas.
    inlines = [DetallePedidoInline, PagoInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('pedido__id', 'producto__nombre')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'metodo', 'monto', 'estado', 'fecha_pago')
    list_filter = ('metodo', 'estado', 'fecha_pago')
    search_fields = ('pedido__id', 'referencia_transaccion')
