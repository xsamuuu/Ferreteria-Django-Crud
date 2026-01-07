from django.contrib import admin
from .models import Categoria, Proveedor, Producto, Cliente, Venta, DetalleVenta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ruc', 'ciudad', 'activo')
    search_fields = ('nombre', 'ruc')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'proveedor', 'precio_venta', 'stock', 'activo')
    list_filter = ('categoria', 'proveedor', 'activo')
    search_fields = ('codigo', 'nombre')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'nombres', 'apellidos', 'telefono', 'activo')
    search_fields = ('numero_documento', 'nombres', 'apellidos')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_venta', 'cliente', 'fecha_venta', 'total', 'estado')
    search_fields = ('numero_venta', 'cliente__nombres', 'cliente__apellidos')

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto__nombre',)
