"""
Script para sembrar categorías, proveedor y productos de ejemplo.
Ejecutar con: .\venv\Scripts\python.exe tools\seed_products.py
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ferreteria.settings')

import django
django.setup()

from inventario.models import Categoria, Proveedor, Producto
from decimal import Decimal

cat, _ = Categoria.objects.get_or_create(nombre='Herramientas', defaults={'descripcion':'Herramientas manuales y eléctricas'})
cat2, _ = Categoria.objects.get_or_create(nombre='Pinturas', defaults={'descripcion':'Pinturas y accesorios'})
prov, _ = Proveedor.objects.get_or_create(nombre='Distribuciones SA', defaults={'ruc':'9999999999','telefono':'999999999','direccion':'Av Principal 123','ciudad':'Lima'})

productos = [
    {'codigo':'TALDR-600','nombre':'Taladro Percutor 600W','categoria':cat,'proveedor':prov,'precio_compra':Decimal('60.00'),'precio_venta':Decimal('89.99'),'stock':10},
    {'codigo':'SET-LLAV-12','nombre':'Set de Llaves 12pz','categoria':cat,'proveedor':prov,'precio_compra':Decimal('15.00'),'precio_venta':Decimal('24.50'),'stock':20},
    {'codigo':'CASCO-SEC','nombre':'Casco de Seguridad','categoria':cat,'proveedor':prov,'precio_compra':Decimal('7.00'),'precio_venta':Decimal('12.00'),'stock':15},
    {'codigo':'CINTA-5M','nombre':'Cinta Métrica 5m','categoria':cat,'proveedor':prov,'precio_compra':Decimal('3.00'),'precio_venta':Decimal('5.99'),'stock':50},
    {'codigo':'PINT-BLANCO','nombre':'Pintura Blanco 4L','categoria':cat2,'proveedor':prov,'precio_compra':Decimal('20.00'),'precio_venta':Decimal('35.00'),'stock':25},
]

for p in productos:
    obj, created = Producto.objects.update_or_create(codigo=p['codigo'], defaults={
        'nombre':p['nombre'],
        'descripcion':'',
        'categoria':p['categoria'],
        'proveedor':p['proveedor'],
        'precio_compra':p['precio_compra'],
        'precio_venta':p['precio_venta'],
        'stock':p['stock'],
    })
    print(('CREATED' if created else 'UPDATED') + ' ' + obj.codigo)
print('SEED_DONE')

