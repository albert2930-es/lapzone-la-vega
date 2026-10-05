from django.db.models import Sum

from .models import Carrito, Categoria


def navegacion(request):
    """Datos pequeños que se muestran en todas las páginas."""
    categorias_nav = Categoria.objects.order_by('nombre')[:8]
    carrito_cantidad = 0

    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            carrito_cantidad = (
                carrito.detalles.aggregate(total=Sum('cantidad')).get('total') or 0
            )

    return {
        'categorias_nav': categorias_nav,
        'carrito_cantidad': carrito_cantidad,
    }
