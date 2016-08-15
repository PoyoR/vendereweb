from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .models import Ventas, Venta_detalle
from catalogo.models import Productos
from empresa.models import Empresa, Cajero, Sucursales
from .forms import VentaForm, VentaDetalleForm, VentaDetalleFormSet

@login_required
def ticket(request, pk):
	empresa = get_object_or_404(Empresa, pk=1)
	venta = get_object_or_404(Ventas, pk=pk)
	productos = Venta_detalle.objects.filter(venta=venta.pk)
	return render(request, "ticket.html", {'venta':venta,'productos':productos, 'empresa':empresa})


class VentasCrear(CreateView):
	template_name = "ventas.html"
	form_class = VentaForm	

	def get_context_data(self, **kwargs):
		context =  super(VentasCrear, self).get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = VentaDetalleFormSet(self.request.POST)
		else:
			context['formset'] = VentaDetalleFormSet()
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():						
			self.object = form.save(commit=False)
			self.object.cajero = self.request.user

			sucursales = Sucursales.objects.all()
			if sucursales:
				cajero = Cajero.objects.get(user=self.request.user)
				self.object.sucursal = cajero.sucursal
				self.object.save()
			else:
				self.object.save()
				
			id_venta = self.object.id
			formset.instance = self.object
			formset.save()
			return redirect('ticket', pk=id_venta)
		else:
			return self.render_to_response(self.get_context_data(form=form))


class BusquedaProductoAjaxView(TemplateView):		

	def get(self, request, *args, **kwargs):
		sucursales = Sucursales.objects.all()
		codigo = request.GET['q']

		if sucursales:
			sucursal = request.user.cajero.sucursal
			producto = Productos.objects.filter(codigo=codigo,sucursal=sucursal)
			
		else:
			producto = Productos.objects.filter(codigo=codigo)
		
		data = serializers.serialize('json', producto)

		return HttpResponse(data, content_type='application/json')