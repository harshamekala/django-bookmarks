from django.contrib import admin
from bookmarks.models import *

# Register your models here.

admin.site.site_header = 'Tejas | Django Bookmarks Web Administration'
admin.site.index_title = 'Tejas | Django Bookmarks Web Administration'

admin.site.register(Link)
admin.site.register(Bookmark)
admin.site.register(Tag)
admin.site.register(SharedBookmark)
admin.site.register(Friendship)
admin.site.register(Invitation)
