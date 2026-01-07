def cart_item_count(request):
    """Context processor que devuelve el número total de items en el carrito (suma de cantidades)."""
    cart = request.session.get('cart', {})
    total = 0
    for item in cart.values():
        try:
            total += int(item.get('cantidad', 0))
        except Exception:
            pass
    return {'cart_count': total}

