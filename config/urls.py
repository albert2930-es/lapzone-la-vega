from django.contrib import admin
from django.urls import path

from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),

    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),

    path('checkout/', views.checkout, name='checkout'),
    path('pedido/<int:id>/confirmado/', views.pedido_confirmado, name='pedido_confirmado'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),

    path('mis-direcciones/', views.mis_direcciones, name='mis_direcciones'),
    path('mis-direcciones/nueva/', views.direccion_crear, name='direccion_crear'),
    path('mis-direcciones/<int:id>/editar/', views.direccion_editar, name='direccion_editar'),
    path('mis-direcciones/<int:id>/eliminar/', views.direccion_eliminar, name='direccion_eliminar'),
]
