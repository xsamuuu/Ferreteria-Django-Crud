from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


# 1. Categoría de Productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# 2. Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    ruc = models.CharField(max_length=20, unique=True, verbose_name="RUC/NIT")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    direccion = models.TextField(verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    pais = models.CharField(max_length=100, default="Perú", verbose_name="País")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.ruc}"


# 3. Producto
class Producto(models.Model):
    UNIDADES_MEDIDA = [
        ('UND', 'Unidad'),
        ('KG', 'Kilogramo'),
        ('LT', 'Litro'),
        ('MT', 'Metro'),
        ('M2', 'Metro Cuadrado'),
        ('M3', 'Metro Cúbico'),
        ('CAJ', 'Caja'),
        ('PAQ', 'Paquete'),
    ]

    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos', verbose_name="Categoría")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='productos', verbose_name="Proveedor")
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Precio de Compra")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Precio de Venta")
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Stock")
    stock_minimo = models.IntegerField(default=10, validators=[MinValueValidator(0)], verbose_name="Stock Mínimo")
    unidad_medida = models.CharField(max_length=3, choices=UNIDADES_MEDIDA, default='UND', verbose_name="Unidad de Medida")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def margen_ganancia(self):
        """Calcula el margen de ganancia en porcentaje"""
        if self.precio_compra > 0:
            return ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100
        return 0

    @property
    def necesita_reposicion(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.stock <= self.stock_minimo


# 4. Cliente
class Cliente(models.Model):
    TIPO_DOCUMENTO = [
        ('DNI', 'DNI'),
        ('RUC', 'RUC'),
        ('CE', 'Carnet de Extranjería'),
        ('PAS', 'Pasaporte'),
    ]

    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO, default='DNI', verbose_name="Tipo de Documento")
    numero_documento = models.CharField(max_length=20, unique=True, verbose_name="Número de Documento")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} - {self.numero_documento}"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del cliente"""
        return f"{self.nombres} {self.apellidos}"


# 5. Venta
class Venta(models.Model):
    METODOS_PAGO = [
        ('EFE', 'Efectivo'),
        ('TAR', 'Tarjeta'),
        ('TRA', 'Transferencia'),
        ('YAP', 'Yape'),
        ('PLI', 'Plin'),
    ]

    ESTADO_VENTA = [
        ('PEN', 'Pendiente'),
        ('COM', 'Completada'),
        ('ANU', 'Anulada'),
    ]

    numero_venta = models.CharField(max_length=20, unique=True, verbose_name="Número de Venta")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas', verbose_name="Cliente")
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))], verbose_name="Subtotal")
    igv = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))], verbose_name="IGV (18%)")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))], verbose_name="Total")
    metodo_pago = models.CharField(max_length=3, choices=METODOS_PAGO, default='EFE', verbose_name="Método de Pago")
    estado = models.CharField(max_length=3, choices=ESTADO_VENTA, default='PEN', verbose_name="Estado")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta {self.numero_venta} - {self.cliente.nombre_completo}"

    def calcular_totales(self):
        """Calcula el subtotal, IGV y total de la venta"""
        detalles = self.detalles.all()
        self.subtotal = sum(detalle.subtotal for detalle in detalles)
        self.igv = self.subtotal * Decimal('0.18')
        self.total = self.subtotal + self.igv
        self.save()


# 6. Detalle de Venta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles', verbose_name="Venta")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_venta', verbose_name="Producto")
    cantidad = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], verbose_name="Subtotal")
    canjeado = models.BooleanField(default=False, verbose_name="Producto Canjeado")
    fecha_canje = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Canje")

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"
        ordering = ['id']

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    def save(self, *args, **kwargs):
        """Calcula el subtotal automáticamente"""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar los totales de la venta
        self.venta.calcular_totales()
