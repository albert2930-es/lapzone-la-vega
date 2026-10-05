from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.CharField(
        max_length=20,
        choices=[
            ("cliente", "Cliente"),
            ("administrador", "Administrador"),
        ],
        default="cliente"
    )

    class Meta:
        db_table = "usuario"

    def __str__(self):
        return self.username


class Direccion(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="direcciones"
    )
    calle = models.CharField(max_length=150)
    sector = models.CharField(max_length=100)
    referencia = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, default="La Vega")
    es_principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.calle}, {self.sector}, {self.ciudad}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    especificaciones = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField(default=0)
    imagen = models.CharField(max_length=255, blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos"
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"


class Carrito(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="carrito"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="detalles_carrito"
    )
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["carrito", "producto"],
                name="uq_carrito_producto"
            )
        ]

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"


class Pedido(models.Model):
    TIPO_ENTREGA = [
        ("domicilio", "Domicilio"),
        ("retiro_tienda", "Retiro en tienda"),
    ]

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_camino", "En camino"),
        ("entregado", "Entregado"),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pedidos"
    )
    tipo_entrega = models.CharField(
        max_length=20,
        choices=TIPO_ENTREGA,
        default="domicilio"
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Pedido #{self.id}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_pedido"
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"Pedido #{self.pedido.id} - {self.producto.nombre}"


class Pago(models.Model):
    METODOS = [
        ("efectivo", "Efectivo"),
        ("transferencia", "Transferencia"),
    ]

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("completado", "Completado"),
        ("rechazado", "Rechazado"),
    ]

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name="pago"
    )
    metodo = models.CharField(
        max_length=20,
        choices=METODOS
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )
    referencia_transaccion = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"Pago del pedido #{self.pedido.id}"