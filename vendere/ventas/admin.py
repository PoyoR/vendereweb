from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from import_export import fields
from .models import Ventas, Venta_detalle, Devoluciones
from catalogo.models import Productos


class DevolucionesAdmin(admin.ModelAdmin):
	list_display = ('producto', 'cantidad')	


class ProductosInline(admin.TabularInline):

	model = Venta_detalle
	extra = 3


class ProductosResource(resources.ModelResource):	

	class Meta:
		model = Venta_detalle
		fields = ('producto__descripcion','cantidad',)


class Venta_detalleAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin):
	def has_add_permission(self, request):
		return False

	list_display = ('producto','cantidad')
	resource_class = ProductosResource


class VentasResource(resources.ModelResource):	

	class Meta:

		model = Ventas
		fields = ('fecha','metodo_pago','total',)
		export_order = ('fecha','total',)


class VentasAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin):
	list_display = ('pk','fecha','nombre_cajero','total')
	list_search = ['fecha']
	list_filter = ['fecha','sucursal']
	inlines = [ProductosInline]
	resource_class = VentasResource

	def nombre_cajero(self, obj):
		if obj.cajero.get_full_name():
			return obj.cajero.get_full_name()
		else:
			return obj.cajero.username


admin.site.register(Venta_detalle,Venta_detalleAdmin)
admin.site.register(Ventas,VentasAdmin)
admin.site.register(Devoluciones,DevolucionesAdmin)