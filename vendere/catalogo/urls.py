from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ProductosView, BusquedaAjaxView

urlpatterns = [
    url(r'^$', login_required(ProductosView), name='catalogo'),
    url(r'^busqueda_ajax/$', login_required(BusquedaAjaxView.as_view())),
]