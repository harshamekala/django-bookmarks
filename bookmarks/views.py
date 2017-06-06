from django.shortcuts import *
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.contrib.auth import *
from bookmarks.models import *
from bookmarks.forms import *

# Create your views here.

ITEMS_PER_PAGE = 3

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
    query_set = user.bookmark_set.order_by('-id')
    #print(request.GET)
    paginator = Paginator(query_set, ITEMS_PER_PAGE)
    try:
        page_number = int(request.GET['page'])
    except(KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404
    bookmarks = page.object_list
    context = {
    'user': request.user,
    'bookmarks': bookmarks,
    'show_tags' : True,
    'show_paginator': paginator.num_pages >1,
    'has_previous': page.has_previous(),
    'has_next': page.has_next(),
    'page': page_number,
    'pages': paginator.num_pages,
    'next_page': page_number + 1,
    'previous_page': page_number - 1,
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
            q = Q()
            for keyword in query:
                q = q | Q(title__icontains = keyword)
            form = bookmarkSearchForm({'query': query})
            bookmarks = Bookmark.objects.filter(q)[:10]
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

@login_required
def friends_page(request, username):
    user = get_object_or_404(User, username= username)
    friends = [friendship.to_friend for friendship in user.to_friend.all()]
    friend_bookmarks = Bookmark.objects.filter(user_id__in = friends).order_by('-id')
    context = {
    'username' : username,
    'friends' : friends,
    'bookmarks' : friend_bookmarks,
    'show_tags': True,
    }
    return render(request, 'friends_page.html', context)

@login_required
def friend_add(request):
    if 'username' in request.GET:
        friend = get_object_or_404(User, username= request.GET['username'])
        friendship = Friendship(from_friend = request.user, to_friend = friend)
        friendhip.save()
        return redirect('/bookmarks/friends/{}/'.format(request.user.username))
    else:
        raise Http404

@login_required
def invite(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            invitation = Invitation(
            name = form.cleaned_data['name'],
            email = form.cleaned_data['email'],
            code = User.objects.make_random_password(20),
            sender = request.user
            )
            invitation.save()
            invitation.send()
            return redirect('/bookmarks/friend/invite')
    form = InviteForm()
    return render(request,'invite_friend.html', {'form':form})

@login_required
def invite_register(request, code):
    print(request)
    print(code)
    return redirect('/bookmarks/registration/')
