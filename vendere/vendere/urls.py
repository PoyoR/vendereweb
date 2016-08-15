from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.static import serve

from rest_framework.authtoken import views
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from registration.models import RegistrationProfile

from .views import login_page, dashboard, mas_vendidos, total_ventas

#Necesario para el registro de dispositivo con la api
router = DefaultRouter()
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'device/gcm', GCMDeviceAuthorizedViewSet)

admin.autodiscover()
admin.site.unregister(RegistrationProfile)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_page, name='login'),
    url(r'catalogo/', include('catalogo.urls')),
    url(r'vender/', include('ventas.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^dashboard/', dashboard, name="dashboard"),
    url(r'^mas-vendidos/', mas_vendidos, name="mas_vendidos"),
    url(r'^ganancias/', total_ventas, name="ganancias"),
    url(r'^accounts/logout/$', auth_views.logout,
        {'next_page': '/'}, name='logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/$', views.obtain_auth_token),
    url(r'^', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
