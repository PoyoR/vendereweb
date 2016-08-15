from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import *
from ventas.models import Venta_detalle
from catalogo.models import Productos

class VentasMixin(object):
	queryset = Ventas.objects.all().order_by('-fecha')[:30]
	serializer_class = VentasSerializer

class VentasList(VentasMixin, ListAPIView):
	permission_classes = (IsAuthenticated,
		IsAdminUser,)
	pass


class VentaDetalleMixin(object):
	serializer_class = VentaDetalleSerializer

	def get_queryset(self):        
		venta = self.kwargs['pk']
		return Venta_detalle.objects.filter(venta=venta)
	
class VentaDetalleList(VentaDetalleMixin, ListAPIView):
	permission_classes = (IsAuthenticated,
		IsAdminUser,)
	pass


class ProductosMixin(object):
	queryset = Productos.objects.filter(existencia__lte = 3)
	serializer_class = ProductosSerializer

	
class ProductosList(ProductosMixin, ListAPIView):
	permission_classes = (IsAuthenticated,
		IsAdminUser,)
	pass