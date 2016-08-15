from django import forms

class LoginForm(forms.Form): #Form para el login
	username = forms.CharField() #Tipo char
	password = forms.CharField(widget=forms.PasswordInput()) #Tipo char para password