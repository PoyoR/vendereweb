from django.shortcuts import render
from django.views.generic import TemplateView
from django.core import serializers
from django.http import HttpResponse
from .models import Productos
from empresa.models import Sucursales

def ProductosView(request):
	productos = Productos.objects.all()
	sucursales = Sucursales.objects.all()
	
	return render(request, "catalogo.html", {'productos': productos,'sucursales': sucursales})


class BusquedaAjaxView(TemplateView):

	def get(self, request, *args, **kwargs):
		codigo = request.GET['q']
		productos = Productos.objects.filter(codigo__icontains = codigo)
		data = serializers.serialize('json', productos)

		return HttpResponse(data, content_type='application/json')