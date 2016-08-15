from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import VentasCrear, BusquedaProductoAjaxView, ticket

urlpatterns = [
    url(r'^$', login_required(VentasCrear.as_view()), name='vender'),
    url(r'^busqueda_producto/$', login_required(BusquedaProductoAjaxView.as_view())),
    #url(r'^agregar_producto/$', agregar_producto),
    url(r'^ticket/(?P<pk>\d+)/$',ticket, name='ticket'),
]