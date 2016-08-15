from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

#from django.views.generic import ListView, TemplateView, DeleteView
from .forms import LoginForm
from empresa.models import Empresa
from ventas.models import Ventas, Venta_detalle
from catalogo.models import Productos

#class DashView(TemplateView):
#	template_name = "dashboard.html"

@staff_member_required
def total_ventas(request):
	ventas = Ventas.objects.aggregate(Sum('total'))
	ventas_sucursal = Ventas.objects.values('sucursal__nombre').annotate(Sum('total')).order_by('-total__sum')
	ventas_fecha = Ventas.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(c=Count('id')).annotate(Sum('total'))
	
	ventas_cajero = Ventas.objects.values('cajero__username').annotate(Sum('total')).order_by('-total__sum')

	return render(request, 'total_ventas.html', 
		{'ventas':ventas, 'ventas_sucursal':ventas_sucursal,'ventas_cajero':ventas_cajero, 'ventas_fecha': ventas_fecha})

@staff_member_required
def mas_vendidos(request):
	productos = Venta_detalle.objects.values('producto__descripcion').annotate(Sum('cantidad')).order_by('-cantidad__sum')[:30]

	return render(request, 'mas_vendidos.html', {'productos': productos})

@staff_member_required
def dashboard(request):	
	ventas = Ventas.objects.all()

	return render(request, 'dashboard.html', {'ventas': ventas})	

def login_page(request): 
	if request.user.is_authenticated(): #Si el usuario esta autenticado se redirige al dashboard
		if request.user.is_staff:
			return HttpResponseRedirect('dashboard')
		else:
			return HttpResponseRedirect('vender')
	else:
		message = None
		empresa = get_object_or_404(Empresa, pk=1)
		if request.method == "POST": #Si el metodo es POST
			form = LoginForm(request.POST) #Se guarda el form en la variable form
			if form.is_valid(): #Si es valido
				username = request.POST['username'] #Se obtienen los datos ingresados
				password = request.POST['password'] # y se guardan en variables
				user = authenticate(username=username, password=password) #Se crea variable user y seejecuta metodo para autenticar
				if user is not None: #Si el usuario existe
					if user.is_active: # y si el usuario no esta desactivado
						login(request, user) #Se ejecuta metodo de logueo
						if user.is_staff:
							return HttpResponseRedirect('dashboard') #y se redirige a dashboard
						else:
							return HttpResponseRedirect('vender') #y se redirige a dashboard
					else:
						message = "Usuario inactivo"
				else:
					message = "Usuario y/o password incorrecto"
		else:
			form = LoginForm() 
	return render(request, 'index.html', {'message': message, 'empresa': empresa, 'form': form}) #Devolver objeto a template