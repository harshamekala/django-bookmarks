import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    #By default all the fields are mandatory in forms required= True
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", max_length=30,
                           widget=forms.PasswordInput())

class RegistrationForm(forms.Form):
    username = forms.CharField(label= "Username")
    email = forms.EmailField(label = "E-Mail")
    password1 = forms.CharField(label = "Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label = "Confirm Password", widget= forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            return password2
        raise forms.ValidationError("Entered Passwords Don't Match")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Username can only contain alphanumeric characters and the underscore")
        try:
            User.objects.get(username='username')
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username is already taken")

class BookmarksForm(forms.Form):
    url = forms.URLField(label= "URL")
    title = forms.CharField(label="Title")
    tags = forms.CharField(label= "Tags")
    share = forms.BooleanField(label= "Share on the Main Page", required = False)

class bookmarkSearchForm(forms.Form):
    query = forms.CharField(label="Search")

class InviteForm(forms.Form):
    name = forms.CharField(label= "Name")
    email = forms.EmailField(label= "E-Mail")
