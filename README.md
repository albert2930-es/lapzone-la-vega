# LapZone La Vega

Tienda online de laptops y accesorios con entrega local en La Vega o retiro en tienda.

**Estudiante:** Albert Peguero, 5to A. **Entrega final:** 5 de octubre de 2026.

## Funcionalidades implementadas

- Registro, inicio y cierre de sesión con autenticación de Django.
- Catálogo, búsqueda y filtros por marca, categoría y precio.
- Carrito por usuario, cantidades y control de disponibilidad.
- Direcciones del cliente, entrega a domicilio o retiro en tienda.
- Pedido, detalle, pago registrado como pendiente y actualización de stock.
- Administración de productos, categorías, pedidos y usuarios mediante Django Admin.
- Validaciones del servidor y operaciones de compra dentro de una transacción.

Los pagos son registros de efectivo o transferencia; el proyecto no procesa cobros bancarios reales. Alertas automáticas de inventario, informes avanzados de ventas y recuperación de contraseñas no forman parte de la versión demostrada.

## Tecnologías y arquitectura

Python 3.14, Django 6.1.1, MySQL 8.4 con InnoDB, HTML, CSS y Bootstrap 5.3.3.
La interfaz usa la arquitectura MVT: `models.py` define los datos, `views.py` gestiona las peticiones y `templates/tienda/` contiene las páginas.

```text
config/                 Configuración y rutas
tienda/
  models.py             Nueve modelos del dominio
  forms.py              Registro, login y direcciones
  views.py              Catálogo, carrito y compra
  admin.py              Gestión administrativa
  migrations/           Esquema e integridad MySQL
  templates/tienda/      HTML de la aplicación
  static/tienda/         CSS y recursos gráficos
  tests.py              23 pruebas automáticas
docs/                   Guion de la defensa y documentación técnica
manage.py               Comandos estándar de Django
iniciar.py              Comandos con configuración .env
requirements.txt        Dependencias exactas verificadas
.env.example            Ejemplo de configuración sin credenciales
```

## Instalación en Windows

Requiere Python compatible con Django 6.1 y un servicio MySQL disponible. Para reproducir el entorno comprobado, usar Python 3.14.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Editar `.env` con la clave local y las credenciales de MySQL. El archivo está excluido de Git. Crear la base de datos en MySQL:

```sql
CREATE DATABASE lapzone_db CHARACTER SET utf8mb4;
```

```powershell
python iniciar.py migrate
python iniciar.py cargar_productos_demo
python iniciar.py createsuperuser
python iniciar.py check --database default
python iniciar.py runserver
```

Abrir `http://127.0.0.1:8000/` y `http://127.0.0.1:8000/admin/`.
`iniciar.py` admite los mismos comandos que `manage.py`, cargando primero las variables de `.env`.
El catálogo de ejemplo usa imágenes SVG locales. Las fotos de productos del catálogo histórico pueden requerir Internet, al igual que Bootstrap y las fuentes servidas desde CDN.

## Pruebas

```powershell
python iniciar.py test tienda --verbosity 2
```

Las pruebas usan una base MySQL temporal separada. El usuario de MySQL necesita permiso para crear esa base. Cubren formularios, rutas, acceso por usuario, CRUD, carrito, pedido/pago/stock, unicidad, transacciones y claves foráneas.

## Correcciones incorporadas

- Un POST vacío activa la validación de formularios.
- Los precios rechazan letras, valores no finitos y rangos invertidos.
- El checkout valida el identificador de la dirección antes de consultarla.
- La migración `0002_integridad_mysql` convierte tablas MyISAM a InnoDB y restaura claves foráneas después de comprobar que no existan referencias huérfanas.
- La configuración de la base y la clave de Django se leen de variables de entorno.
- La lista de pedidos del administrador conserva filtros por fecha sin exigir tablas de zonas horarias de MySQL.
- La verificación final ejecuta 24 pruebas automatizadas con resultado satisfactorio.

La migración no cambia los registros de negocio. Antes de aplicarla a una base existente, conservar un respaldo y revisar el resultado.

## Demostración y documentación

Consultar [el guion de defensa](docs/DEFENSA.md) y [la arquitectura](docs/ARQUITECTURA.md).
La entrega en plataforma consta del PDF consolidado de las fases 1 a 4 y las diapositivas de presentación.
La demostración presencial corresponde al estudiante y debe hacerse con el sistema ejecutándose en su equipo.
