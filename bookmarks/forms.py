from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required= True)
    password = forms.CharField(label="Password", required=True, max_length=30,
                           widget=forms.PasswordInput())
