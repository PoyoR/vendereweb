from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered

class Empresa(models.Model):
	nombre = models.CharField(max_length=100)
	logo = models.ImageField(upload_to='logo')
	direccion = models.CharField(max_length=200)
	horario = models.CharField(max_length=100,blank=True,null=True)
	telefono = models.CharField(max_length=50)
	rfc = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural = "Empresa"

	def __unicode__(self):
		return self.nombre


class Metodos_pago(models.Model):
	metodo = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "Metodos de pago"

	def __unicode__(self):
		return self.metodo


class Sucursales(models.Model):
	nombre = models.CharField(max_length=50,default="")
	direccion = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "Sucursales"

	def __unicode__(self):
		if self.nombre:		
			return self.nombre
		else: 
			return self.direccion

class Cajero(models.Model):    
    user = models.OneToOneField(User)
    sucursal = models.ForeignKey(Sucursales,blank=True,null=True)

    def __unicode__(self):
		return self.user.username

def user_registered_callback(sender, user, request, **kwargs):
    profile = Cajero(user = user)    
    profile.sucursal = Sucursales.objects.get(pk=request.POST["sucursal"])
    profile.save()
 
user_registered.connect(user_registered_callback)
