from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Empresa, Sucursales, Metodos_pago, Cajero

class EmpresaAdmin(admin.ModelAdmin):
	
	def has_add_permission(self, request):
		return False

	#def has_change_permission(self, request):
	#	return False

	def has_delete_permission(self, request, obj=None):
		return False	

class SucursalesAdmin(admin.ModelAdmin):
	list_display = ["nombre","direccion"]

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CajeroInline(admin.StackedInline):
    model = Cajero
    can_delete = False
    #verbose_name_plural = 'Usuarios'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (CajeroInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.disable_action('delete_selected')
admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(Metodos_pago)
admin.site.register(Sucursales)