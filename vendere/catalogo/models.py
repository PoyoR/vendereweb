from __future__ import unicode_literals

from django.db import models

from empresa.models import Sucursales

class Impuestos(models.Model):
	nombre = models.CharField(max_length=100)
	porcentaje = models.IntegerField(help_text="Ejemplo: IVA es el 16 % - Por lo tanto colocar 16 ")

	class Meta:
		verbose_name_plural = "Impuestos"

	def __unicode__(self):
		return self.nombre

class Productos(models.Model):
	codigo = models.CharField(max_length=80)
	sucursal = models.ForeignKey(Sucursales,blank=True,null=True)
	descripcion = models.TextField()	
	precio_venta = models.DecimalField(max_digits=10,decimal_places=2)
	precio_final = models.DecimalField(max_digits=10,decimal_places=2, help_text="Precio de venta (+ impuesto)")
	existencia = models.IntegerField()
	impuesto = models.ForeignKey(Impuestos,blank=True,null=True)

	def save(self, *args, **kwargs):
		if self.impuesto is not None:
			precio = self.precio_venta
			impuesto = self.impuesto.porcentaje
			preciof = (impuesto*precio)/100
			preciofinal = precio+preciof
			self.precio_final = preciofinal
			super(Productos, self).save(*args, **kwargs)
		else:
			precio = self.precio_venta
			self.precio_final = precio
			super(Productos, self).save(*args, **kwargs)

	def poco_stock(self):
		return self.existencia > 3
	poco_stock.boolean = True
	poco_stock.short_description = 'Stock mayor a 3'

	class Meta:
		verbose_name_plural = "Productos"

	def __unicode__(self):
		return self.descripcion


class Servicios(models.Model):
	descripcion = models.TextField()
	precio = models.DecimalField(max_digits=10,decimal_places=2)

	class Meta:
		verbose_name_plural = "Servicios"

	def __unicode__(self):
		return self.descripcion