from django.contrib import admin
from bookmarks.models import *

# Register your models here.

admin.site.register(Link)
admin.site.register(Bookmark)
admin.site.register(Tag)
admin.site.register(SharedBookmark)
