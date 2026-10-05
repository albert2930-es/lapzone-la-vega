# Guion de la defensa de LapZone

## Antes de entrar al aula

1. Confirmar que MySQL esté iniciado y que `.env` apunte a la base prevista.
2. Activar el entorno y ejecutar `python iniciar.py check --database default`.
3. Ejecutar `python iniciar.py runserver` y abrir inicio y administración.
4. Tener lista una cuenta de cliente y una cuenta de administrador.
5. Revisar el stock del producto elegido y la conexión para Bootstrap y las fotos.
6. Abrir las diapositivas y el PDF consolidado. El repositorio debe estar accesible al docente.

## Demostración sugerida: 7 a 10 minutos

1. Presentar el problema: consultar y comprar tecnología dentro de La Vega.
2. Mostrar el registro y los errores de campos vacíos. Iniciar sesión.
3. Navegar por inicio, catálogo y detalle. Usar el buscador o un filtro.
4. Agregar un producto al carrito y modificar su cantidad dentro del stock.
5. Crear una dirección de ejemplo y elegir entrega local. Confirmar un pedido de prueba en efectivo.
6. Mostrar la confirmación y el historial del cliente. Aclarar que no se ejecuta un cobro real.
7. Abrir Django Admin y consultar el pedido, sus detalles, el pago pendiente y el stock actualizado.
8. Crear un producto temporal, cambiar precio o stock y eliminar solo ese registro temporal.
9. Cerrar sesión y resumir el aprendizaje.

## Preguntas probables

**¿Cómo aplicaste MVT?** Los modelos definen entidades y relaciones. Las vistas reciben las peticiones y ejecutan la lógica. Las plantillas presentan los datos que envían las vistas.

**¿Por qué MySQL e InnoDB?** MySQL cumple el motor indicado para el proyecto. InnoDB permite transacciones y claves foráneas, necesarias para mantener coherentes pedido, pago, detalles y stock.

**¿Qué ocurre si cambia el stock?** El checkout bloquea y vuelve a consultar los productos dentro de `transaction.atomic()`. Si no alcanza el stock, informa el problema y evita crear un pedido parcial.

**¿Puede un cliente editar la dirección de otro?** Las consultas incluyen `usuario=request.user`. Las pruebas comprueban una respuesta 404 para datos ajenos.

**¿Cómo guardas las contraseñas?** Django guarda hashes mediante su sistema de autenticación. La configuración privada de MySQL y Django se mantiene fuera de Git.

**¿Qué cambió durante las pruebas?** Se corrigieron formularios vacíos, filtros de precio no válidos, identificadores de dirección mal formados y el motor MyISAM.

**¿Qué faltaría para producción?** Configurar un servidor de producción, desactivar DEBUG, gestionar los recursos estáticos y desarrollar funciones comerciales adicionales como cobros reales. Esta entrega demuestra un sistema académico local.
