"""
Script para cargar datos de ejemplo en el sistema de ferretería
Ejecutar con: python manage.py shell < cargar_datos_ejemplo.py
"""

from inventario.models import Categoria, Proveedor, Producto, Cliente, Venta, DetalleVenta
from decimal import Decimal
from django.utils import timezone

print(" Cargando datos de ejemplo...")

# 1. CREAR CATEGORÍAS
print("\n Creando Categorías...")
categorias = [
    {"nombre": "Herramientas Manuales", "descripcion": "Martillos, destornilladores, llaves, etc."},
    {"nombre": "Herramientas Eléctricas", "descripcion": "Taladros, sierras, pulidoras, etc."},
    {"nombre": "Materiales de Construcción", "descripcion": "Cemento, arena, ladrillos, etc."},
    {"nombre": "Pinturas y Accesorios", "descripcion": "Pinturas, brochas, rodillos, etc."},
    {"nombre": "Electricidad", "descripcion": "Cables, interruptores, enchufes, etc."},
    {"nombre": "Plomería", "descripcion": "Tubos, llaves, accesorios de baño, etc."},
]

for cat_data in categorias:
    cat, created = Categoria.objects.get_or_create(nombre=cat_data["nombre"], defaults=cat_data)
    if created:
        print(f"   {cat.nombre}")

# 2. CREAR PROVEEDORES
print("\n Creando Proveedores...")
proveedores = [
    {"nombre": "Ferretería Central SAC", "ruc": "20123456789", "telefono": "01-4567890",
     "email": "ventas@ferreteriacentral.com", "direccion": "Av. Industrial 123", "ciudad": "Lima"},
    {"nombre": "Distribuidora El Constructor", "ruc": "20234567890", "telefono": "01-5678901",
     "email": "contacto@elconstructor.com", "direccion": "Jr. Comercio 456", "ciudad": "Callao"},
    {"nombre": "Importadora Tools Peru", "ruc": "20345678901", "telefono": "01-6789012",
     "email": "info@toolsperu.com", "direccion": "Av. Argentina 789", "ciudad": "Lima"},
]

for prov_data in proveedores:
    prov, created = Proveedor.objects.get_or_create(ruc=prov_data["ruc"], defaults=prov_data)
    if created:
        print(f"   {prov.nombre}")

# 3. CREAR PRODUCTOS
print("\n Creando Productos...")
productos = [
    # Herramientas Manuales
    {"codigo": "MART-001", "nombre": "Martillo de Uña 16 oz", "categoria": "Herramientas Manuales",
     "proveedor": "Ferretería Central SAC", "precio_compra": 15.00, "precio_venta": 25.00,
     "stock": 50, "stock_minimo": 10, "unidad_medida": "UND"},
    {"codigo": "DEST-001", "nombre": "Juego Destornilladores 6 pzs", "categoria": "Herramientas Manuales",
     "proveedor": "Importadora Tools Peru", "precio_compra": 20.00, "precio_venta": 35.00,
     "stock": 30, "stock_minimo": 8, "unidad_medida": "UND"},
    {"codigo": "LLAV-001", "nombre": "Llave Inglesa 12 pulgadas", "categoria": "Herramientas Manuales",
     "proveedor": "Importadora Tools Peru", "precio_compra": 25.00, "precio_venta": 45.00,
     "stock": 20, "stock_minimo": 5, "unidad_medida": "UND"},

    # Herramientas Eléctricas
    {"codigo": "TALA-001", "nombre": "Taladro Percutor 650W", "categoria": "Herramientas Eléctricas",
     "proveedor": "Importadora Tools Peru", "precio_compra": 150.00, "precio_venta": 250.00,
     "stock": 15, "stock_minimo": 5, "unidad_medida": "UND"},
    {"codigo": "SIER-001", "nombre": "Sierra Circular 7 1/4 pulgadas", "categoria": "Herramientas Eléctricas",
     "proveedor": "Importadora Tools Peru", "precio_compra": 180.00, "precio_venta": 300.00,
     "stock": 10, "stock_minimo": 3, "unidad_medida": "UND"},

    # Materiales de Construcción
    {"codigo": "CEME-001", "nombre": "Cemento Portland Tipo I x 42.5kg", "categoria": "Materiales de Construcción",
     "proveedor": "Distribuidora El Constructor", "precio_compra": 18.00, "precio_venta": 28.00,
     "stock": 200, "stock_minimo": 50, "unidad_medida": "UND"},
    {"codigo": "LADR-001", "nombre": "Ladrillo King Kong 18 Huecos", "categoria": "Materiales de Construcción",
     "proveedor": "Distribuidora El Constructor", "precio_compra": 0.80, "precio_venta": 1.20,
     "stock": 5000, "stock_minimo": 1000, "unidad_medida": "UND"},

    # Pinturas
    {"codigo": "PINT-001", "nombre": "Pintura Látex Blanco x 1 Galón", "categoria": "Pinturas y Accesorios",
     "proveedor": "Ferretería Central SAC", "precio_compra": 35.00, "precio_venta": 55.00,
     "stock": 80, "stock_minimo": 20, "unidad_medida": "UND"},
    {"codigo": "BROC-001", "nombre": "Brocha 3 pulgadas", "categoria": "Pinturas y Accesorios",
     "proveedor": "Ferretería Central SAC", "precio_compra": 8.00, "precio_venta": 15.00,
     "stock": 60, "stock_minimo": 15, "unidad_medida": "UND"},

    # Electricidad
    {"codigo": "CABL-001", "nombre": "Cable THW 2.5mm x metro", "categoria": "Electricidad",
     "proveedor": "Distribuidora El Constructor", "precio_compra": 2.50, "precio_venta": 4.00,
     "stock": 500, "stock_minimo": 100, "unidad_medida": "MT"},
    {"codigo": "INTE-001", "nombre": "Interruptor Simple", "categoria": "Electricidad",
     "proveedor": "Ferretería Central SAC", "precio_compra": 3.50, "precio_venta": 6.00,
     "stock": 100, "stock_minimo": 20, "unidad_medida": "UND"},

    # Plomería
    {"codigo": "TUBO-001", "nombre": "Tubo PVC 1/2 pulgada x 3m", "categoria": "Plomería",
     "proveedor": "Distribuidora El Constructor", "precio_compra": 8.00, "precio_venta": 14.00,
     "stock": 150, "stock_minimo": 30, "unidad_medida": "UND"},
    {"codigo": "LLAV-002", "nombre": "Llave de Lavatorio Cromada", "categoria": "Plomería",
     "proveedor": "Ferretería Central SAC", "precio_compra": 35.00, "precio_venta": 60.00,
     "stock": 25, "stock_minimo": 8, "unidad_medida": "UND"},
]

for prod_data in productos:
    categoria = Categoria.objects.get(nombre=prod_data["categoria"])
    proveedor = Proveedor.objects.get(nombre=prod_data["proveedor"])

    prod, created = Producto.objects.get_or_create(
        codigo=prod_data["codigo"],
        defaults={
            "nombre": prod_data["nombre"],
            "categoria": categoria,
            "proveedor": proveedor,
            "precio_compra": Decimal(str(prod_data["precio_compra"])),
            "precio_venta": Decimal(str(prod_data["precio_venta"])),
            "stock": prod_data["stock"],
            "stock_minimo": prod_data["stock_minimo"],
            "unidad_medida": prod_data["unidad_medida"],
        }
    )
    if created:
        print(f"   {prod.codigo} - {prod.nombre}")

# 4. CREAR CLIENTES
print("\n Creando Clientes...")
clientes = [
    {"tipo_documento": "DNI", "numero_documento": "12345678", "nombres": "Juan Carlos",
     "apellidos": "Pérez García", "telefono": "987654321", "email": "juan.perez@email.com",
     "direccion": "Av. Los Alamos 123, San Isidro"},
    {"tipo_documento": "DNI", "numero_documento": "23456789", "nombres": "María Elena",
     "apellidos": "López Rodríguez", "telefono": "976543210", "email": "maria.lopez@email.com",
     "direccion": "Jr. Las Flores 456, Miraflores"},
    {"tipo_documento": "RUC", "numero_documento": "20456789012", "nombres": "Constructora",
     "apellidos": "Los Andes SAC", "telefono": "965432109", "email": "ventas@losandes.com",
     "direccion": "Av. Industrial 789, San Juan de Lurigancho"},
    {"tipo_documento": "DNI", "numero_documento": "34567890", "nombres": "Pedro Antonio",
     "apellidos": "Ramírez Silva", "telefono": "954321098", "email": "pedro.ramirez@email.com",
     "direccion": "Calle Los Pinos 321, Surco"},
]

for cli_data in clientes:
    cli, created = Cliente.objects.get_or_create(numero_documento=cli_data["numero_documento"], defaults=cli_data)
    if created:
        print(f"   {cli.nombre_completo} - {cli.numero_documento}")

# 5. CREAR VENTAS DE EJEMPLO
print("\n Creando Ventas de Ejemplo...")

# Venta 1
cliente1 = Cliente.objects.get(numero_documento="12345678")
venta1 = Venta.objects.create(
    numero_venta="V-2024-0001",
    cliente=cliente1,
    metodo_pago="EFE",
    estado="COM"
)

# Detalles de Venta 1
DetalleVenta.objects.create(
    venta=venta1,
    producto=Producto.objects.get(codigo="MART-001"),
    cantidad=2,
    precio_unitario=Decimal("25.00")
)
DetalleVenta.objects.create(
    venta=venta1,
    producto=Producto.objects.get(codigo="DEST-001"),
    cantidad=1,
    precio_unitario=Decimal("35.00")
)
print(f"   {venta1.numero_venta} - Total: S/. {venta1.total}")

# Venta 2
cliente2 = Cliente.objects.get(numero_documento="20456789012")
venta2 = Venta.objects.create(
    numero_venta="V-2024-0002",
    cliente=cliente2,
    metodo_pago="TRA",
    estado="COM"
)

# Detalles de Venta 2
DetalleVenta.objects.create(
    venta=venta2,
    producto=Producto.objects.get(codigo="CEME-001"),
    cantidad=50,
    precio_unitario=Decimal("28.00")
)
DetalleVenta.objects.create(
    venta=venta2,
    producto=Producto.objects.get(codigo="LADR-001"),
    cantidad=1000,
    precio_unitario=Decimal("1.20")
)
DetalleVenta.objects.create(
    venta=venta2,
    producto=Producto.objects.get(codigo="PINT-001"),
    cantidad=10,
    precio_unitario=Decimal("55.00")
)
print(f"   {venta2.numero_venta} - Total: S/. {venta2.total}")

# Venta 3
cliente3 = Cliente.objects.get(numero_documento="23456789")
venta3 = Venta.objects.create(
    numero_venta="V-2024-0003",
    cliente=cliente3,
    metodo_pago="YAP",
    estado="COM"
)

# Detalles de Venta 3
DetalleVenta.objects.create(
    venta=venta3,
    producto=Producto.objects.get(codigo="TALA-001"),
    cantidad=1,
    precio_unitario=Decimal("250.00")
)
DetalleVenta.objects.create(
    venta=venta3,
    producto=Producto.objects.get(codigo="BROC-001"),
    cantidad=3,
    precio_unitario=Decimal("15.00")
)
print(f"   {venta3.numero_venta} - Total: S/. {venta3.total}")

print("\n ¡Datos de ejemplo cargados exitosamente!")
print("\n Resumen:")
print(f"  - Categorías: {Categoria.objects.count()}")
print(f"  - Proveedores: {Proveedor.objects.count()}")
print(f"  - Productos: {Producto.objects.count()}")
print(f"  - Clientes: {Cliente.objects.count()}")
print(f"  - Ventas: {Venta.objects.count()}")
print(f"  - Detalles de Venta: {DetalleVenta.objects.count()}")
print("\n ¡Listo! Ya puedes acceder al panel de administración.")

