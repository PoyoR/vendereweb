from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from push_notifications.models import GCMDevice

from catalogo.models import Productos, Servicios
from empresa.models import Metodos_pago, Sucursales


class Ventas(models.Model):	
	metodo_pago = models.ForeignKey(Metodos_pago)
	fecha = models.DateTimeField(auto_now_add=True,auto_now=False)
	cajero = models.ForeignKey('auth.user')
	sucursal = models.ForeignKey(Sucursales,blank=True,null=True)
	total = models.DecimalField(max_digits=10,decimal_places=2)

	class Meta:
		verbose_name_plural = "Ventas"

	def __unicode__(self):
		return '%s - %s' % (self.fecha, self.cajero.username)


class Venta_detalle(models.Model):
	venta = models.ForeignKey(Ventas)
	producto = models.ForeignKey(Productos)
	cantidad = models.IntegerField()

	class Meta:
		verbose_name_plural = "Productos vendidos"

	def __unicode__(self):
		return self.producto.descripcion

class Devoluciones(models.Model):
	producto = models.ForeignKey(Productos)
	cantidad = models.IntegerField()

	class Meta:
		verbose_name_plural = "Devoluciones"

	def __unicode__(self):
		return self.producto.descripcion


def enviar_alerta(sender, instance=None, **kwargs):
	usuarios = User.objects.filter(is_superuser=True)
	devices = GCMDevice.objects.filter(user_id__in=usuarios)	
	devices.send_message("Nueva venta")


def actualizar_stock_devolucion(sender, instance, **kwargs):
	instance.producto.existencia += instance.cantidad
	instance.producto.save()
		

def actualizar_stock(sender, instance, **kwargs):
	instance.producto.existencia -= instance.cantidad
	instance.producto.save()

post_save.connect(enviar_alerta, sender=Ventas)
post_save.connect(actualizar_stock, sender=Venta_detalle)
post_save.connect(actualizar_stock_devolucion, sender=Devoluciones)