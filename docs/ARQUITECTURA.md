# Arquitectura y persistencia

## Recorrido de una petición

El navegador solicita una ruta. `config/urls.py` la vincula con una vista en `tienda/views.py`. La vista valida los datos y utiliza el ORM para leer o escribir en MySQL. Django renderiza la plantilla HTML y responde al navegador.

## Modelos

Usuario, Direccion, Categoria, Producto, Carrito, DetalleCarrito, Pedido, DetallePedido y Pago.
Las tablas de autenticación, permisos, sesiones y administración complementan estos nueve modelos.

Un usuario tiene direcciones y pedidos. Su carrito contiene productos mediante DetalleCarrito. Pedido conserva los artículos y precios históricos mediante DetallePedido, y posee un pago. El catálogo agrupa los productos por categoría.

## Integridad

- Carrito es único por usuario y no admite dos detalles del mismo producto.
- Producto.precio usa DecimalField y validación de valor no negativo.
- Pedido.direccion y DetallePedido.producto usan PROTECT para evitar eliminar referencias utilizadas.
- Checkout calcula el total en el servidor y crea pedido, detalles y pago dentro de una transacción.
- InnoDB y claves foráneas protegen las referencias también en MySQL.

## Organización del código

`forms.py` concentra los formularios. `admin.py` configura la administración. Los comentarios de `views.py` y la migración explican las validaciones y la operación transaccional. `tests.py` comprueba escenarios reales de fallo y operaciones de extremo a extremo.

## Evidencias

Las fases 1 a 4 conservan los documentos y las capturas del proyecto. El ensayo final usa una instalación MySQL local aislada y el mismo catálogo histórico, con cuentas y operaciones de demostración. El ensayo técnico no sustituye la defensa presencial del estudiante.
