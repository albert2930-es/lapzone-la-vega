from decimal import Decimal

from django.contrib.admin.sites import site
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Carrito, Categoria, DetalleCarrito, DetallePedido, Direccion, Pago, Pedido, Producto, Usuario


class Fase4Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Usuario.objects.create_user('qa_cliente', password='PruebaFase4!2026', first_name='Pruebas')
        cls.other = Usuario.objects.create_user('qa_otro', password='PruebaFase4!2026')
        cls.category = Categoria.objects.create(nombre='Categoria QA')
        cls.product = Producto.objects.create(nombre='Producto QA', marca='LapZone', precio=Decimal('100.50'), stock=5, categoria=cls.category)
        cls.address = Direccion.objects.create(usuario=cls.user, calle='Calle de pruebas 4', sector='QA', es_principal=True)

    def login(self):
        self.client.force_login(self.user)

    def cart(self):
        cart, _ = Carrito.objects.get_or_create(usuario=self.user)
        return DetalleCarrito.objects.create(carrito=cart, producto=self.product, cantidad=2)

    def test_01_registro_post_vacio(self):
        response = self.client.post(reverse('registro'), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)
        self.assertContains(response, 'Este campo es obligatorio')
        self.assertEqual(Usuario.objects.count(), 2)

    def test_02_correo_invalido(self):
        response = self.client.post(reverse('registro'), {'username':'nuevo', 'email':'correo-invalido'})
        self.assertIn('email', response.context['form'].errors)

    def test_03_precio_letras_admin(self):
        from django.test import RequestFactory
        request = RequestFactory().get('/admin/tienda/producto/add/')
        request.user = self.user
        form_class = site._registry[Producto].get_form(request)
        form = form_class(data={'nombre':'QA','marca':'QA','precio':'abc','stock':'3','activo':True})
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)
        self.assertContainsError(form, 'precio')

    def assertContainsError(self, form, field):
        self.assertTrue(form.errors[field])

    def test_04_stock_letras_admin(self):
        from django.forms import modelform_factory
        form = modelform_factory(Producto, fields=['nombre','marca','precio','stock'])(data={'nombre':'QA','marca':'QA','precio':'20.50','stock':'abc'})
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_05_filtros_invalidos(self):
        for value in ['abc','NaN','Infinity','-1','999999999999999999999999']:
            with self.subTest(value=value):
                response = self.client.get(reverse('productos'), {'precio_min':value})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'El filtro de precio no es válido.')

    def test_06_rango_invertido(self):
        response = self.client.get(reverse('productos'), {'precio_min':'200','precio_max':'10'})
        self.assertContains(response, 'El filtro de precio no es válido.')

    def test_07_navegacion_publica(self):
        for url in [reverse('inicio'), reverse('productos'), reverse('detalle_producto', args=[self.product.pk]), reverse('registro'), reverse('login')]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_08_error_404(self):
        self.assertEqual(self.client.get('/ruta-inexistente-fase4/').status_code, 404)
        self.assertEqual(self.client.get(reverse('detalle_producto', args=[999999])).status_code, 404)

    def test_09_rutas_protegidas(self):
        for name in ['carrito','mis_pedidos','mis_direcciones']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('login')))

    def test_10_login_y_logout(self):
        response = self.client.post(reverse('login'), {'username':'qa_cliente','password':'PruebaFase4!2026'})
        self.assertRedirects(response, reverse('inicio'))
        self.assertEqual(self.client.get(reverse('mis_pedidos')).status_code, 200)
        self.client.get(reverse('logout'))
        self.assertEqual(self.client.get(reverse('mis_pedidos')).status_code, 302)

    def test_11_login_redireccion_externa(self):
        response = self.client.post(reverse('login'), {'username':'qa_cliente','password':'PruebaFase4!2026','next':'https://example.invalid/'})
        self.assertRedirects(response, reverse('inicio'))

    def test_12_direccion_vacia(self):
        self.login()
        response = self.client.post(reverse('direccion_crear'), {})
        self.assertContains(response, 'Este campo es obligatorio')
        self.assertEqual(Direccion.objects.count(), 1)

    def test_13_crud_direccion(self):
        self.login()
        self.client.post(reverse('direccion_crear'), {'calle':'Calle QA nueva','sector':'QA nuevo'})
        address = Direccion.objects.get(calle='Calle QA nueva')
        self.assertEqual(address.usuario_id, self.user.pk)
        self.client.post(reverse('direccion_editar', args=[address.pk]), {'calle':'Calle QA editada','sector':'QA editado'})
        address.refresh_from_db()
        self.assertEqual(address.calle, 'Calle QA editada')
        self.client.post(reverse('direccion_eliminar', args=[address.pk]))
        self.assertFalse(Direccion.objects.filter(pk=address.pk).exists())

    def test_14_direccion_ajena(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse('direccion_editar', args=[self.address.pk])).status_code, 404)

    def test_15_cantidad_invalida(self):
        self.login()
        detail = self.cart()
        response = self.client.post(reverse('actualizar_carrito', args=[detail.pk]), {'cantidad':'abc'}, follow=True)
        self.assertContains(response, 'La cantidad indicada no es válida.')
        detail.refresh_from_db()
        self.assertEqual(detail.cantidad, 2)

    def test_16_stock_insuficiente(self):
        self.login()
        detail = self.cart()
        self.client.post(reverse('actualizar_carrito', args=[detail.pk]), {'cantidad':'99'})
        detail.refresh_from_db()
        self.assertEqual(detail.cantidad, 2)

    def test_17_checkout_direccion_invalida(self):
        self.login()
        self.cart()
        for value in ['abc','-1','999999999999999999999999']:
            with self.subTest(value=value):
                response = self.client.post(reverse('checkout'), {'tipo_entrega':'domicilio','metodo_pago':'efectivo','direccion_id':value}, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Selecciona una dirección de entrega válida.')
        self.assertEqual(Pedido.objects.count(), 0)

    def test_18_checkout_integro(self):
        self.login()
        detail = self.cart()
        response = self.client.post(reverse('checkout'), {'tipo_entrega':'domicilio','metodo_pago':'efectivo','direccion_id':self.address.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        order = Pedido.objects.get()
        self.assertEqual(order.total, Decimal('201.00'))
        self.assertEqual(order.pago.monto, order.total)
        self.assertEqual(order.detalles.get().cantidad, 2)
        self.assertEqual(order.direccion_id, self.address.pk)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertFalse(DetalleCarrito.objects.filter(pk=detail.pk).exists())

    def test_19_checkout_stock_cambiado(self):
        self.login()
        self.cart()
        self.product.stock = 1
        self.product.save()
        response = self.client.post(reverse('checkout'), {'tipo_entrega':'retiro_tienda','metodo_pago':'efectivo'}, follow=True)
        self.assertContains(response, 'Revisa tu carrito.')
        self.assertEqual(Pedido.objects.count(), 0)
        self.assertEqual(Pago.objects.count(), 0)
        self.assertEqual(DetallePedido.objects.count(), 0)

    def test_20_producto_pedido_protegido(self):
        order = Pedido.objects.create(usuario=self.user, direccion=self.address)
        DetallePedido.objects.create(pedido=order, producto=self.product, cantidad=1, precio_unitario=self.product.precio)
        with self.assertRaises(ProtectedError):
            self.product.delete()
        with self.assertRaises(ProtectedError):
            self.address.delete()

    def test_21_carrito_sin_duplicados(self):
        detail = self.cart()
        with self.assertRaises(IntegrityError), transaction.atomic():
            DetalleCarrito.objects.create(carrito=detail.carrito, producto=self.product, cantidad=1)
        self.assertEqual(DetalleCarrito.objects.count(), 1)

    def test_22_transaccion_rollback(self):
        before = Producto.objects.count()
        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                Producto.objects.create(nombre='Rollback QA', marca='QA', precio=1, stock=1)
                raise RuntimeError('Fallo controlado')
        self.assertEqual(Producto.objects.count(), before)

    def test_23_clave_foranea_mysql(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Producto.objects.create(nombre='Referencia inexistente', marca='QA', precio=1, stock=1, categoria_id=99999999)
        self.assertFalse(Producto.objects.filter(nombre='Referencia inexistente').exists())

    def test_24_admin_pedidos_con_registros(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        Pedido.objects.create(usuario=self.user, direccion=self.address, total='100.50')
        self.login()
        response = self.client.get(reverse('admin:tienda_pedido_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '100,50')
