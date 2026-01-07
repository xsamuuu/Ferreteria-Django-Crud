# Script de prueba para flujo: listar productos -> añadir al carrito -> checkout
import os
import django
from django.test import Client

# Asegurar DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ferreteria.settings')

django.setup()
from inventario.models import Producto, Venta

c = Client()

r = c.get('/productos/')
print('LIST_STATUS', r.status_code)
productos = list(Producto.objects.all())
print('PRODUCTS_COUNT', len(productos))
if not productos:
    print('NO_PRODUCTS')
    raise SystemExit(0)

p = productos[0]
print('FIRST_PRODUCT', p.pk, p.nombre)

# Añadir 2 unidades al carrito
r = c.post(f'/productos/{p.pk}/', {'cantidad': 2}, follow=True)
print('ADD_STATUS', r.status_code)

r = c.get('/cart/')
print('CART_STATUS', r.status_code)
print('CART_SNIPPET', r.content.decode()[:400])

# Checkout
checkout_data = {
    'tipo_documento': 'DNI',
    'numero_documento': '12345678',
    'nombres': 'Juan',
    'apellidos': 'Perez',
    'telefono': '999999999',
    'email': 'juan@example.com',
    'direccion': 'Calle Falsa 123'
}

r = c.post('/checkout/', checkout_data, follow=True)
print('CHECKOUT_STATUS', r.status_code)
print('REDIRECT_CHAIN', r.redirect_chain)

print('VENTAS_COUNT', Venta.objects.count())
if Venta.objects.exists():
    v = Venta.objects.latest('id')
    print('VENTA', v.numero_venta, str(v.total), str(v.subtotal))
    for d in v.detalles.all():
        print('DETALLE', d.producto.nombre, d.cantidad, d.subtotal)
