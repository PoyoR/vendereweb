from django import forms
from django.forms.models import inlineformset_factory
from .models import Ventas, Venta_detalle

class VentaForm(forms.ModelForm):
	
	class Meta:
		model = Ventas
		fields = ['metodo_pago','total']


class VentaDetalleForm(forms.ModelForm):

	class Meta:
		model = Venta_detalle
		fields = ['producto','cantidad']


VentaDetalleFormSet = inlineformset_factory(Ventas, Venta_detalle, form=VentaDetalleForm)