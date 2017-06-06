"""project_bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    # Session Management
    url(r'^login/$', login_view, name ='login'),
    url(r'^logout/$', logout_view, name = 'logout'),
    url(r'^registration/$', registration_view, name = 'registration'),
    #Actual URLS
    url(r'^$', main_page, name= 'index' ),
    url(r'^user/(\w+)/$',user_page, name= 'users'),
    url(r'^addbookmark/$', bookmarks, name = 'bookmark'),
    url(r'^tag/([^\s]+)/$', tag_page, name = 'tags'),
    url(r'^search/$', searchview, name = 'search'),
    url(r'^vote/(?P<id>[0-9]+)/$', voting , name ='vote'),
    url(r'^friends/(\w+)/$', friends_page, name = 'friends'),
    url(r'^friend/add/$', friend_add, name = 'add_friend'),
    url(r'^friend/invite/$', invite, name= 'invite'),
    url(r'^friend/accept/(\w+)/$',invite_register, name = 'register' )
]
