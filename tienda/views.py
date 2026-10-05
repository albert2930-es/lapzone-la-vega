from decimal import Decimal, InvalidOperation

from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import DireccionForm, LoginForm, RegistroForm
from .models import (
    Carrito,
    Categoria,
    DetalleCarrito,
    DetallePedido,
    Direccion,
    Pago,
    Pedido,
    Producto,
)


def inicio(request):
    productos = (
        Producto.objects.filter(activo=True)
        .select_related('categoria')
        .order_by('-fecha_creacion')[:8]
    )
    return render(request, 'tienda/inicio.html', {'productos': productos})


def productos(request):
    """Filtra el catálogo y devuelve errores para precios inválidos."""
    lista_productos = Producto.objects.filter(activo=True).select_related('categoria')
    categorias = Categoria.objects.order_by('nombre')

    categoria_id = request.GET.get('categoria', '').strip()
    marca = request.GET.get('marca', '').strip()
    busqueda = request.GET.get('q', '').strip()
    precio_min = request.GET.get('precio_min', '').strip()
    precio_max = request.GET.get('precio_max', '').strip()

    if categoria_id.isdigit():
        lista_productos = lista_productos.filter(categoria_id=categoria_id)

    if marca:
        lista_productos = lista_productos.filter(marca__iexact=marca)

    if busqueda:
        lista_productos = lista_productos.filter(
            Q(nombre__icontains=busqueda)
            | Q(marca__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
            | Q(especificaciones__icontains=busqueda)
        )

    try:
        campo_precio = forms.DecimalField(
            max_digits=10, decimal_places=2, min_value=Decimal('0'), required=False
        )
        minimo = campo_precio.clean(precio_min)
        maximo = campo_precio.clean(precio_max)
        if minimo is not None and maximo is not None and minimo > maximo:
            raise ValidationError('El precio mínimo supera el máximo.')
        if minimo is not None:
            lista_productos = lista_productos.filter(precio__gte=minimo)
        if maximo is not None:
            lista_productos = lista_productos.filter(precio__lte=maximo)
    except (ValidationError, InvalidOperation):
        messages.warning(request, 'El filtro de precio no es válido.')

    marcas = (
        Producto.objects.filter(activo=True)
        .exclude(marca='')
        .values_list('marca', flat=True)
        .distinct()
        .order_by('marca')
    )

    return render(
        request,
        'tienda/productos.html',
        {
            'productos': lista_productos.order_by('nombre'),
            'categorias': categorias,
            'marcas': marcas,
        },
    )


def detalle_producto(request, id):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria'), id=id, activo=True
    )
    relacionados = Producto.objects.filter(activo=True).exclude(id=producto.id)
    if producto.categoria_id:
        relacionados = relacionados.filter(categoria_id=producto.categoria_id)
    relacionados = relacionados[:4]

    return render(
        request,
        'tienda/detalle_producto.html',
        {'producto': producto, 'relacionados': relacionados},
    )


@login_required
def carrito(request):
    carrito_obj, _ = Carrito.objects.get_or_create(usuario=request.user)
    detalles = carrito_obj.detalles.select_related('producto')
    total = sum(detalle.subtotal for detalle in detalles)
    cantidad_productos = sum(detalle.cantidad for detalle in detalles)

    return render(
        request,
        'tienda/carrito.html',
        {
            'carrito': carrito_obj,
            'detalles': detalles,
            'total': total,
            'cantidad_productos': cantidad_productos,
        },
    )


@login_required
def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id, activo=True)

    if producto.stock <= 0:
        messages.warning(request, 'Este producto está agotado.')
        return redirect('detalle_producto', id=producto.id)

    carrito_obj, _ = Carrito.objects.get_or_create(usuario=request.user)
    detalle, creado = DetalleCarrito.objects.get_or_create(
        carrito=carrito_obj, producto=producto
    )

    if creado:
        detalle.cantidad = 1
        detalle.save(update_fields=['cantidad'])
        messages.success(request, 'Producto agregado al carrito.')
    elif detalle.cantidad < producto.stock:
        detalle.cantidad += 1
        detalle.save(update_fields=['cantidad'])
        messages.success(request, 'Se aumentó la cantidad del producto en el carrito.')
    else:
        messages.warning(request, 'Ya tienes en el carrito todo el stock disponible.')

    return redirect('carrito')


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    form = RegistroForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        messages.success(request, 'Tu cuenta fue creada correctamente.')
        return redirect('inicio')

    return render(request, 'tienda/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    form = LoginForm(request, data=request.POST if request.method == 'POST' else None)
    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST' and form.is_valid():
        usuario = form.get_user()
        login(request, usuario)
        messages.success(request, f'Bienvenido, {usuario.first_name or usuario.username}.')

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect('inicio')

    return render(request, 'tienda/login.html', {'form': form, 'next': next_url})


def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('inicio')


@login_required
def actualizar_carrito(request, id):
    carrito_obj = get_object_or_404(Carrito, usuario=request.user)
    detalle = get_object_or_404(DetalleCarrito, id=id, carrito=carrito_obj)

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except (TypeError, ValueError):
            messages.error(request, 'La cantidad indicada no es válida.')
            return redirect('carrito')

        if cantidad <= 0:
            detalle.delete()
            messages.info(request, 'Producto eliminado del carrito.')
        elif cantidad <= detalle.producto.stock:
            detalle.cantidad = cantidad
            detalle.save(update_fields=['cantidad'])
            messages.success(request, 'Cantidad actualizada.')
        else:
            messages.warning(
                request,
                f'Solo hay {detalle.producto.stock} unidades disponibles.',
            )

    return redirect('carrito')


@login_required
def eliminar_del_carrito(request, id):
    carrito_obj = get_object_or_404(Carrito, usuario=request.user)
    detalle = get_object_or_404(DetalleCarrito, id=id, carrito=carrito_obj)

    if request.method == 'POST':
        detalle.delete()
        messages.info(request, 'Producto eliminado del carrito.')

    return redirect('carrito')


@login_required
def vaciar_carrito(request):
    carrito_obj, _ = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        eliminados, _ = carrito_obj.detalles.all().delete()
        if eliminados:
            messages.info(request, 'El carrito fue vaciado correctamente.')
        else:
            messages.info(request, 'El carrito ya estaba vacío.')

    return redirect('carrito')


@login_required
def mis_direcciones(request):
    direcciones = request.user.direcciones.order_by('-es_principal', 'sector')
    return render(request, 'tienda/mis_direcciones.html', {'direcciones': direcciones})


@login_required
def direccion_crear(request):
    form = DireccionForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        direccion = form.save(commit=False)
        direccion.usuario = request.user
        direccion.ciudad = 'La Vega'

        if form.cleaned_data.get('es_principal') or not request.user.direcciones.exists():
            request.user.direcciones.update(es_principal=False)
            direccion.es_principal = True

        direccion.save()
        messages.success(request, 'Dirección guardada correctamente.')
        return redirect('mis_direcciones')

    return render(
        request,
        'tienda/direccion_form.html',
        {'form': form, 'titulo': 'Agregar dirección'},
    )


@login_required
def direccion_editar(request, id):
    direccion = get_object_or_404(Direccion, id=id, usuario=request.user)
    form = DireccionForm(request.POST if request.method == 'POST' else None, instance=direccion)

    if request.method == 'POST' and form.is_valid():
        direccion = form.save(commit=False)
        direccion.ciudad = 'La Vega'
        if form.cleaned_data.get('es_principal'):
            request.user.direcciones.exclude(id=direccion.id).update(es_principal=False)
        direccion.save()
        messages.success(request, 'Dirección actualizada.')
        return redirect('mis_direcciones')

    return render(
        request,
        'tienda/direccion_form.html',
        {'form': form, 'titulo': 'Editar dirección'},
    )


@login_required
def direccion_eliminar(request, id):
    direccion = get_object_or_404(Direccion, id=id, usuario=request.user)

    if request.method == 'POST':
        try:
            era_principal = direccion.es_principal
            direccion.delete()
            if era_principal:
                siguiente = request.user.direcciones.first()
                if siguiente:
                    siguiente.es_principal = True
                    siguiente.save(update_fields=['es_principal'])
            messages.info(request, 'Dirección eliminada.')
        except Exception:
            messages.error(
                request,
                'No se puede eliminar esa dirección porque está asociada a un pedido.',
            )

    return redirect('mis_direcciones')


@login_required
def checkout(request):
    """Confirma el pedido, sus detalles y el stock dentro de una transacción."""
    carrito_obj = get_object_or_404(Carrito, usuario=request.user)
    detalles_qs = carrito_obj.detalles.select_related('producto')

    if not detalles_qs.exists():
        messages.info(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    direcciones = request.user.direcciones.order_by('-es_principal', 'sector')
    total = sum(detalle.subtotal for detalle in detalles_qs)

    if request.method == 'GET':
        return render(
            request,
            'tienda/checkout.html',
            {
                'carrito': carrito_obj,
                'detalles': detalles_qs,
                'direcciones': direcciones,
                'total': total,
            },
        )

    tipo_entrega = request.POST.get('tipo_entrega')
    direccion_id = request.POST.get('direccion_id')
    metodo_pago = request.POST.get('metodo_pago')
    referencia = request.POST.get('referencia_transaccion', '').strip()

    if tipo_entrega not in {'domicilio', 'retiro_tienda'}:
        messages.error(request, 'Selecciona un tipo de entrega válido.')
        return redirect('checkout')

    if metodo_pago not in {'efectivo', 'transferencia'}:
        messages.error(request, 'Selecciona un método de pago válido.')
        return redirect('checkout')

    direccion = None
    if tipo_entrega == 'domicilio':
        if not direccion_id:
            messages.warning(request, 'Agrega o selecciona una dirección de entrega.')
            return redirect('checkout')
        try:
            direccion_id = forms.IntegerField(
                min_value=1, max_value=9223372036854775807
            ).clean(direccion_id)
        except ValidationError:
            messages.error(request, 'Selecciona una dirección de entrega válida.')
            return redirect('checkout')
        direccion = get_object_or_404(
            Direccion, id=direccion_id, usuario=request.user
        )

    detalle_ids = list(detalles_qs.values_list('id', flat=True))

    with transaction.atomic():
        detalles = list(
            DetalleCarrito.objects.select_for_update()
            .filter(id__in=detalle_ids, carrito=carrito_obj)
            .select_related('producto')
        )

        productos_bloqueados = {}
        total_real = Decimal('0.00')

        for detalle in detalles:
            producto = Producto.objects.select_for_update().get(id=detalle.producto_id)
            if not producto.activo or detalle.cantidad > producto.stock:
                messages.error(
                    request,
                    f'El stock de {producto.nombre} cambió. Revisa tu carrito.',
                )
                return redirect('carrito')
            productos_bloqueados[producto.id] = producto
            total_real += producto.precio * detalle.cantidad

        pedido = Pedido.objects.create(
            usuario=request.user,
            direccion=direccion,
            tipo_entrega=tipo_entrega,
            estado='pendiente',
            total=total_real,
        )

        for detalle in detalles:
            producto = productos_bloqueados[detalle.producto_id]
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=detalle.cantidad,
                precio_unitario=producto.precio,
            )
            producto.stock -= detalle.cantidad
            producto.save(update_fields=['stock'])

        Pago.objects.create(
            pedido=pedido,
            metodo=metodo_pago,
            monto=total_real,
            estado='pendiente',
            referencia_transaccion=referencia if metodo_pago == 'transferencia' else '',
        )

        DetalleCarrito.objects.filter(carrito=carrito_obj).delete()

    messages.success(request, f'Pedido #{pedido.id} creado correctamente.')
    return redirect('pedido_confirmado', id=pedido.id)


@login_required
def pedido_confirmado(request, id):
    pedido = get_object_or_404(
        Pedido.objects.select_related('direccion', 'pago').prefetch_related(
            'detalles__producto'
        ),
        id=id,
        usuario=request.user,
    )
    return render(request, 'tienda/pedido_confirmado.html', {'pedido': pedido})


@login_required
def mis_pedidos(request):
    pedidos = (
        Pedido.objects.filter(usuario=request.user)
        .select_related('pago', 'direccion')
        .prefetch_related('detalles__producto')
        .order_by('-fecha_pedido')
    )
    return render(request, 'tienda/mis_pedidos.html', {'pedidos': pedidos})
