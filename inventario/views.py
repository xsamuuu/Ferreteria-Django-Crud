from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Producto, Venta, DetalleVenta, Cliente, Categoria
from .forms import ProductoForm, AddToCartForm, CheckoutForm
from django.contrib import messages
from decimal import Decimal
from django.utils.crypto import get_random_string

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST

def index(request):
    # Productos destacados: últimos 4 productos activos
    productos_destacados = Producto.objects.filter(activo=True).order_by('-fecha_registro')[:4]
    # Categorías para la sección de categorías
    categorias = Categoria.objects.filter(activo=True)[:3]
    return render(request, 'index.html', {'productos_destacados': productos_destacados, 'categorias': categorias})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def productos_list(request, category_id=None):
    productos = Producto.objects.filter(activo=True)
    categoria_nombre = "Todos los Productos"
    
    if category_id:
        categoria = get_object_or_404(Categoria, pk=category_id)
        productos = productos.filter(categoria=categoria)
        categoria_nombre = categoria.nombre
        
    return render(request, 'productos/list.html', {'productos': productos, 'categoria_nombre': categoria_nombre})


def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    form = AddToCartForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cantidad = form.cleaned_data['cantidad']
        cart = request.session.get('cart', {})
        item = cart.get(str(producto.id), {'cantidad': 0, 'precio': str(producto.precio_venta), 'nombre': producto.nombre})
        item['cantidad'] = item.get('cantidad', 0) + cantidad
        cart[str(producto.id)] = item
        request.session['cart'] = cart
        messages.success(request, f'Agregaste {cantidad} x {producto.nombre} al carrito.')
        return redirect('producto_detail', pk=producto.pk)
    return render(request, 'productos/detail.html', {'producto': producto, 'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('producto_detail', pk=producto.pk)
    else:
        form = ProductoForm()
    return render(request, 'productos/create.html', {'form': form})


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for pid, data in cart.items():
        try:
            producto = Producto.objects.get(pk=int(pid))
        except Producto.DoesNotExist:
            continue
        cantidad = int(data.get('cantidad', 0))
        precio = Decimal(str(data.get('precio', producto.precio_venta)))
        subtotal = precio * cantidad
        items.append({'producto': producto, 'cantidad': cantidad, 'precio': precio, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'cart/view.html', {'items': items, 'total': total})


def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        messages.info(request, 'Producto eliminado del carrito.')
    return redirect('cart_view')


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'El carrito está vacío.')
        return redirect('productos_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Crear o recuperar cliente
            data = form.cleaned_data
            cliente, created = Cliente.objects.get_or_create(numero_documento=data['numero_documento'], defaults={
                'tipo_documento': data['tipo_documento'],
                'nombres': data['nombres'],
                'apellidos': data['apellidos'],
                'telefono': data['telefono'],
                'email': data.get('email',''),
                'direccion': data.get('direccion',''),
            })

            # Crear venta
            numero = get_random_string(8).upper()
            venta = Venta.objects.create(numero_venta=numero, cliente=cliente)

            total = Decimal('0.00')
            for pid, item in cart.items():
                producto = Producto.objects.get(pk=int(pid))
                cantidad = int(item.get('cantidad', 0))
                precio = Decimal(str(item.get('precio', producto.precio_venta)))
                subtotal = precio * cantidad
                # Crear DetalleVenta sin activar el método save() que recalcula totales
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal,
                    canjeado=False,  # Especificar explícitamente
                    fecha_canje=None
                )
                # Actualizar stock
                producto.stock = max(0, producto.stock - cantidad)
                producto.save()
                total += subtotal

            # Calcular totales de la venta después de crear todos los detalles
            venta.subtotal = total
            venta.igv = (total * Decimal('0.18')).quantize(Decimal('0.01'))
            venta.total = (venta.subtotal + venta.igv).quantize(Decimal('0.01'))
            venta.save()

            # Limpiar carrito
            request.session['cart'] = {}
            messages.success(request, f'Compra realizada correctamente. Nº {venta.numero_venta}')
            return redirect('checkout_success', pk=venta.pk)
    else:
        form = CheckoutForm()
    return render(request, 'cart/checkout.html', {'form': form})


def checkout_success(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'cart/success.html', {'venta': venta})


def services(request):
    return render(request, 'services.html')


def custom_logout(request):
    """Cerrar la sesión del usuario y redirigir al index. Acepta GET y POST."""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('index')


@require_POST
def add_to_cart(request, pk):
    """Agregar un producto al carrito desde la lista o desde detalle (POST)."""
    try:
        producto = Producto.objects.get(pk=pk, activo=True)
    except Producto.DoesNotExist:
        messages.error(request, 'Producto no encontrado.')
        return redirect('productos_list')

    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad < 1:
        cantidad = 1

    cart = request.session.get('cart', {})
    item = cart.get(str(producto.id), {'cantidad': 0, 'precio': str(producto.precio_venta), 'nombre': producto.nombre})
    item['cantidad'] = item.get('cantidad', 0) + cantidad
    cart[str(producto.id)] = item
    request.session['cart'] = cart
    messages.success(request, f'Agregaste {cantidad} x {producto.nombre} al carrito.')
    return redirect(request.META.get('HTTP_REFERER', 'productos_list'))


@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def producto_delete(request, pk):
    """Eliminar un producto (solo administradores)."""
    from django.db.models.deletion import ProtectedError

    producto = get_object_or_404(Producto, pk=pk)
    nombre_producto = producto.nombre

    try:
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado correctamente.')
    except ProtectedError:
        messages.error(request,
                      f'No se puede eliminar el producto "{nombre_producto}" porque tiene ventas registradas. '
                      f'Para mantener la integridad de los datos, los productos con historial de ventas no pueden ser eliminados.')

    return redirect('productos_list')


@login_required
@user_passes_test(lambda u: u.is_staff)
def historial_tickets(request):
    """Vista del historial de tickets/órdenes de compra (solo administradores)."""
    from django.utils import timezone

    # Obtener todos los detalles de venta ordenados por fecha
    tickets = DetalleVenta.objects.select_related('venta', 'venta__cliente', 'producto').order_by('-venta__fecha_venta')

    # Calcular estadísticas totales (antes de aplicar filtros)
    tickets_totales = DetalleVenta.objects.all()
    total_tickets = tickets_totales.count()
    total_pendientes = tickets_totales.filter(canjeado=False).count()
    total_canjeados = tickets_totales.filter(canjeado=True).count()

    # Filtros opcionales
    filtro_estado = request.GET.get('estado', 'todos')
    if filtro_estado == 'canjeados':
        tickets = tickets.filter(canjeado=True)
    elif filtro_estado == 'pendientes':
        tickets = tickets.filter(canjeado=False)

    return render(request, 'tickets/historial.html', {
        'tickets': tickets,
        'filtro_estado': filtro_estado,
        'total_tickets': total_tickets,
        'total_pendientes': total_pendientes,
        'total_canjeados': total_canjeados
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def marcar_canjeado(request, pk):
    """Marcar un ticket/detalle de venta como canjeado o revertir el estado."""
    from django.utils import timezone

    detalle = get_object_or_404(DetalleVenta, pk=pk)

    # Alternar el estado de canjeado
    if detalle.canjeado:
        detalle.canjeado = False
        detalle.fecha_canje = None
        messages.info(request, f'Ticket #{detalle.id} marcado como NO CANJEADO.')
    else:
        detalle.canjeado = True
        detalle.fecha_canje = timezone.now()
        messages.success(request, f'Ticket #{detalle.id} marcado como CANJEADO.')

    detalle.save()
    return redirect('historial_tickets')
