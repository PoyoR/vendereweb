from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from .models import Impuestos,Productos,Servicios


class ServiciosAdmin(admin.ModelAdmin):
	list_display = ('descripcion','precio')

class ProductosResource(resources.ModelResource):

	class Meta:
		model = Productos

class ProductosAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
	fields = ('codigo','sucursal','descripcion','precio_venta','precio_final','existencia','impuesto')
	list_display = ('codigo','descripcion','existencia', 'poco_stock', 'sucursal')
	list_filter = ('sucursal',)
	search_fields = ['codigo','descripcion']
	readonly_fields = ('precio_final',)


admin.site.register(Impuestos)
admin.site.register(Productos,ProductosAdmin)
admin.site.register(Servicios, ServiciosAdmin)