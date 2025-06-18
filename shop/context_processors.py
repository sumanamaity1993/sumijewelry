def cart(request):
    """Add cart count to the context for all templates."""
    if request.user.is_authenticated:
        cart, created = request.user.cart_set.get_or_create()
        cart_count = cart.get_total_items()
    else:
        cart_count = 0
    return {'cart_count': cart_count} 