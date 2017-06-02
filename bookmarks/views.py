from django.shortcuts import *
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from bookmarks.models import *
from bookmarks.forms import *

# Create your views here.

@login_required
def main_page(request):
    context = {
    'title' : "Django Bookmarks",
    'page_title' : "Welcome django Bookmarks",
    'page_body' : "Where you can store and share Bookmarks"
    }
    shared_bookmarks = SharedBookmark.objects.order_by('-date')[:10]
    context['shared_bookmarks'] = shared_bookmarks
    return render(request, 'mainpage.html', context)

@login_required
def user_page(request, username):
    user= get_object_or_404(User, username=username)
    bookmarks= user.bookmark_set.all()
    context = {
    'user': request.user,
    'bookmarks': bookmarks,
    'show_tags' : True,
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
    return redirect('/bookmarks/login/')

def registration_view(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                        username= form.cleaned_data['username'],
                        email = form.cleaned_data['email'],
                        password = form.cleaned_data['password1'])
            return redirect('login')
    else:
        form = RegistrationForm()
        context = {
            'form' : form
            }
        return render(request, 'registration.html', context)

@login_required
def bookmarks(request):
    if request.method =='POST':
        form = BookmarksForm(request.POST)
        if form.is_valid():
            link, created = Link.objects.get_or_create(url= form.cleaned_data['url'])
            bookmark, created = Bookmark.objects.get_or_create(user_id= request.user, link_id=link)
            bookmark.title = form.cleaned_data['title']
            if not created:
                bookmark.tag_set.clear()
                tag_names = form.cleaned_data['tags'].split()
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name = tag_name)
                    bookmark.tag_set.add(tag)
                    bookmark.save()
            if form.cleaned_data['share']:
                shared, created = SharedBookmark.objects.get_or_create(bookmark=bookmark)
                if created:
                    shared.users_voted.add(request.user)
            return redirect('/bookmarks/user/%s' %request.user)
    else:
        form = BookmarksForm()
        return render(request, 'add_bookmark.html', {'form': form})

@login_required
def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.all()
    context ={
    'bookmarks': bookmarks,
    'show_tags': True,
    'show_user' : True,
    'tag_name': tag_name
    }
    return render(request,'tag.html', context)

@login_required
def searchview(request):
    form = bookmarkSearchForm()
    bookmarks = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        print(request.GET)
        query = request.GET['query'].split()
        print("Query after the split is {0}".format(query))
        if query:
            query = query[0]
            form = bookmarkSearchForm({'query': query})
            bookmarks = Bookmark.objects.filter(title__icontains= query)[:10]
            print (bookmarks)
    context = {
    'form': form,
    'bookmarks': bookmarks,
    'show_results': show_results,
    'show_user': True,
    'show_tags': True
    }
    if 'ajax' in request.GET.keys():
        return render(request, 'bookmark_list.html', context)
    else:
        return render(request, 'search.html', context)

@login_required
def voting(request, id):
    shared_bookmark = get_object_or_404(SharedBookmark, id=id)
    user_voted = shared_bookmark.users_voted.filter(username= request.user.username)
    if not user_voted:
        shared_bookmark.votes += 1
        shared_bookmark.users_voted.add(request.user)
        shared_bookmark.save()
    return redirect('index')
