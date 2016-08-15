from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ventas.models import Ventas, Venta_detalle
from catalogo.models import Productos

class VentasSerializer(serializers.ModelSerializer):	
	cajero = serializers.ReadOnlyField(source='cajero.username')
	sucursal = serializers.ReadOnlyField(source='sucursal.nombre')
	metodo_pago = serializers.ReadOnlyField(source='metodo_pago.metodo')
	fecha = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

	class Meta:
		model = Ventas
		fields = ('pk','fecha','sucursal','cajero','metodo_pago','total')


class VentaDetalleSerializer(serializers.ModelSerializer):
	producto = serializers.ReadOnlyField(source='producto.descripcion')

	class Meta:
		model = Venta_detalle
		fields = ('producto','cantidad')

class ProductosSerializer(serializers.ModelSerializer):
	sucursal = serializers.ReadOnlyField(source='sucursal.nombre')

	class Meta:
		model = Productos
		fields = ('codigo','descripcion','sucursal','existencia')