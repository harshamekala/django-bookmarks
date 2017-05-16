from django.shortcuts import *
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import *
from bookmarks.models import *
from bookmarks.forms import *

# Create your views here.

def main_page(request):
    context = {
    'title' : "Django Bookmarks",
    'page_title' : "Welcome django Bookmarks",
    'page_body' : "Where you can store and share Bookmarks"
    }
    return render(request, 'mainpage.html', context)

def user_page(request, username):
    user= get_object_or_404(User, username=username)
    bookmarks= Bookmark.objects.all()
    context = {
    'user': request.user,
    'bookmarks': bookmarks
    }
    return render(request, 'userpage.html', context)

def login_view(request):
    form = LoginForm()
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
# if username and password doesn't match authenticate method will return None
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {
            'message': "Please Enter Valid Credeintials",
            'form': form
            }
            return render(request,'login.html',context)
    return render(request, 'login.html',{'form':form})

def logout_view(request):
    logout(request)
    context = {
    'message': "You have been Successfully Logged Out"
    }
    return render(request, 'login.html', context)
