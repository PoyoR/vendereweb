from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^ventas/$', views.VentasList.as_view(), name="ventas_list"),	
	url(r'^venta_detalle/(?P<pk>[0-9]+)/$', views.VentaDetalleList.as_view(), name="venta_detail"),
	url(r'^productos/$', views.ProductosList.as_view(), name="productos_list"),	
]
urlpatterns = format_suffix_patterns(urlpatterns)