from django.contrib import admin

from posts.models import Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
