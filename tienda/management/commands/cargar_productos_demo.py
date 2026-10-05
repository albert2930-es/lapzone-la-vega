from decimal import Decimal

from django.core.management.base import BaseCommand

from tienda.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Crea/actualiza categorías y productos de demostración para LapZone.'

    def handle(self, *args, **options):
        categorias = {
            'Laptops': 'Equipos portátiles para estudio, trabajo, creación de contenido y gaming.',
            'Cargadores': 'Cargadores y adaptadores para laptops y dispositivos compatibles.',
            'Audífonos': 'Audífonos y headsets para llamadas, música y videojuegos.',
            'Mouse': 'Mouse alámbricos e inalámbricos para productividad y gaming.',
            'Teclados': 'Teclados de oficina, compactos y mecánicos para diferentes usos.',
            'Mochilas': 'Mochilas y bolsos para transportar laptops y accesorios con protección.',
        }
        cat_objs = {}
        for nombre, descripcion in categorias.items():
            cat, _ = Categoria.objects.update_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion},
            )
            cat_objs[nombre] = cat

        productos = [
            {
                'nombre': 'Lenovo IdeaPad 15', 'marca': 'Lenovo', 'categoria': 'Laptops',
                'descripcion': 'Laptop equilibrada para clases, tareas, navegación y trabajo de oficina.',
                'especificaciones': 'Pantalla 15.6 pulgadas FHD\nProcesador Intel Core i5\nRAM 8 GB\nSSD 512 GB\nWi-Fi y Bluetooth',
                'precio': Decimal('34995.00'), 'stock': 8, 'imagen': '/static/tienda/img/productos/laptop.svg',
            },
            {
                'nombre': 'HP Laptop 15', 'marca': 'HP', 'categoria': 'Laptops',
                'descripcion': 'Equipo portátil de uso diario con almacenamiento rápido y buen rendimiento multitarea.',
                'especificaciones': 'Pantalla 15.6 pulgadas\nProcesador AMD Ryzen 5\nRAM 8 GB\nSSD 512 GB\nWindows 11',
                'precio': Decimal('36950.00'), 'stock': 7, 'imagen': '/static/tienda/img/productos/laptop.svg',
            },
            {
                'nombre': 'ASUS VivoBook 15', 'marca': 'ASUS', 'categoria': 'Laptops',
                'descripcion': 'Laptop ligera para productividad, estudio y entretenimiento cotidiano.',
                'especificaciones': 'Pantalla FHD 15.6 pulgadas\nProcesador Intel Core i5\nRAM 16 GB\nSSD 512 GB\nTeclado numérico',
                'precio': Decimal('41995.00'), 'stock': 5, 'imagen': '/static/tienda/img/productos/laptop.svg',
            },
            {
                'nombre': 'Dell Inspiron 14', 'marca': 'Dell', 'categoria': 'Laptops',
                'descripcion': 'Portátil compacta para estudiantes y profesionales que necesitan movilidad.',
                'especificaciones': 'Pantalla 14 pulgadas FHD\nProcesador Intel Core i5\nRAM 8 GB\nSSD 512 GB\nWebcam HD',
                'precio': Decimal('43900.00'), 'stock': 4, 'imagen': '/static/tienda/img/productos/laptop.svg',
            },
            {
                'nombre': 'Acer Aspire 5', 'marca': 'Acer', 'categoria': 'Laptops',
                'descripcion': 'Laptop versátil con memoria amplia para múltiples aplicaciones y trabajo académico.',
                'especificaciones': 'Pantalla 15.6 pulgadas FHD\nProcesador AMD Ryzen 7\nRAM 16 GB\nSSD 512 GB\nHDMI y USB-C',
                'precio': Decimal('46950.00'), 'stock': 6, 'imagen': '/static/tienda/img/productos/laptop.svg',
            },
            {
                'nombre': 'Logitech M170', 'marca': 'Logitech', 'categoria': 'Mouse',
                'descripcion': 'Mouse inalámbrico sencillo y cómodo para uso escolar y de oficina.',
                'especificaciones': 'Conexión inalámbrica 2.4 GHz\nReceptor USB\nDiseño ambidiestro\nBatería AA',
                'precio': Decimal('895.00'), 'stock': 24, 'imagen': '/static/tienda/img/productos/mouse.svg',
            },
            {
                'nombre': 'Logitech G203', 'marca': 'Logitech', 'categoria': 'Mouse',
                'descripcion': 'Mouse para gaming con sensor preciso y botones configurables.',
                'especificaciones': 'Sensor hasta 8000 DPI\n6 botones\nConexión USB\nIluminación RGB',
                'precio': Decimal('1795.00'), 'stock': 13, 'imagen': '/static/tienda/img/productos/mouse.svg',
            },
            {
                'nombre': 'Redragon M711 Cobra', 'marca': 'Redragon', 'categoria': 'Mouse',
                'descripcion': 'Mouse gaming con agarre cómodo e iluminación personalizable.',
                'especificaciones': 'Sensor ajustable\n7 botones programables\nCable USB\nIluminación RGB',
                'precio': Decimal('1495.00'), 'stock': 15, 'imagen': '/static/tienda/img/productos/mouse.svg',
            },
            {
                'nombre': 'Logitech K120', 'marca': 'Logitech', 'categoria': 'Teclados',
                'descripcion': 'Teclado de tamaño completo para oficina, estudio y tareas diarias.',
                'especificaciones': 'Distribución completa\nTeclado numérico\nConexión USB\nDiseño resistente',
                'precio': Decimal('995.00'), 'stock': 20, 'imagen': '/static/tienda/img/productos/teclado.svg',
            },
            {
                'nombre': 'Redragon Kumara K552', 'marca': 'Redragon', 'categoria': 'Teclados',
                'descripcion': 'Teclado mecánico compacto orientado a gaming y escritura rápida.',
                'especificaciones': 'Formato TKL\nSwitches mecánicos\nConexión USB\nRetroiluminación',
                'precio': Decimal('2595.00'), 'stock': 10, 'imagen': '/static/tienda/img/productos/teclado.svg',
            },
            {
                'nombre': 'HyperX Alloy Core RGB', 'marca': 'HyperX', 'categoria': 'Teclados',
                'descripcion': 'Teclado gaming de membrana con controles multimedia e iluminación.',
                'especificaciones': 'Tamaño completo\nIluminación RGB\nControles multimedia\nConexión USB',
                'precio': Decimal('2995.00'), 'stock': 9, 'imagen': '/static/tienda/img/productos/teclado.svg',
            },
            {
                'nombre': 'HyperX Cloud Stinger 2', 'marca': 'HyperX', 'categoria': 'Audífonos',
                'descripcion': 'Headset cómodo para juegos, clases en línea y llamadas.',
                'especificaciones': 'Diadema ajustable\nMicrófono integrado\nConector 3.5 mm\nControl de volumen',
                'precio': Decimal('2695.00'), 'stock': 11, 'imagen': '/static/tienda/img/productos/audifonos.svg',
            },
            {
                'nombre': 'JBL Tune 520BT', 'marca': 'JBL', 'categoria': 'Audífonos',
                'descripcion': 'Audífonos inalámbricos para música y uso diario con diseño plegable.',
                'especificaciones': 'Bluetooth\nMicrófono integrado\nDiseño plegable\nCarga por USB-C',
                'precio': Decimal('3195.00'), 'stock': 12, 'imagen': '/static/tienda/img/productos/audifonos.svg',
            },
            {
                'nombre': 'UGREEN Cargador USB-C 65W', 'marca': 'UGREEN', 'categoria': 'Cargadores',
                'descripcion': 'Cargador USB-C compacto para laptops y dispositivos compatibles con Power Delivery.',
                'especificaciones': 'Potencia máxima 65 W\nUSB-C Power Delivery\nEntrada 100-240 V\nProtecciones eléctricas',
                'precio': Decimal('2395.00'), 'stock': 18, 'imagen': '/static/tienda/img/productos/cargador.svg',
            },
            {
                'nombre': 'Baseus Cargador USB-C 100W', 'marca': 'Baseus', 'categoria': 'Cargadores',
                'descripcion': 'Adaptador de alta potencia para equipos compatibles y carga de varios dispositivos.',
                'especificaciones': 'Potencia máxima 100 W\nUSB-C\nCarga rápida\nEntrada 100-240 V',
                'precio': Decimal('3495.00'), 'stock': 14, 'imagen': '/static/tienda/img/productos/cargador.svg',
            },
            {
                'nombre': 'Targus Classic 15.6', 'marca': 'Targus', 'categoria': 'Mochilas',
                'descripcion': 'Mochila acolchada para laptop de hasta 15.6 pulgadas y accesorios.',
                'especificaciones': 'Compartimento acolchado\nHasta 15.6 pulgadas\nBolsillos organizadores\nCorreas ajustables',
                'precio': Decimal('2195.00'), 'stock': 16, 'imagen': '/static/tienda/img/productos/mochila.svg',
            },
            {
                'nombre': 'Lenovo B210', 'marca': 'Lenovo', 'categoria': 'Mochilas',
                'descripcion': 'Mochila compacta para transportar laptop, cargador y artículos de estudio.',
                'especificaciones': 'Hasta 15.6 pulgadas\nMaterial ligero\nCompartimento principal\nBolsillo frontal',
                'precio': Decimal('1695.00'), 'stock': 17, 'imagen': '/static/tienda/img/productos/mochila.svg',
            },
            {
                'nombre': 'HP Prelude 15.6', 'marca': 'HP', 'categoria': 'Mochilas',
                'descripcion': 'Mochila de uso diario con protección para laptop y diseño sobrio.',
                'especificaciones': 'Hasta 15.6 pulgadas\nCompartimento acolchado\nBolsillos internos\nCorreas ajustables',
                'precio': Decimal('1895.00'), 'stock': 19, 'imagen': '/static/tienda/img/productos/mochila.svg',
            },
        ]

        creados = 0
        actualizados = 0
        for data in productos:
            categoria = cat_objs[data.pop('categoria')]
            _, creado = Producto.objects.update_or_create(
                nombre=data['nombre'],
                marca=data['marca'],
                defaults={**data, 'categoria': categoria, 'activo': True},
            )
            if creado:
                creados += 1
            else:
                actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {len(cat_objs)} categorías, {creados} productos creados y {actualizados} actualizados.'
        ))
