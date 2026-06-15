from django.contrib import admin

from posts.models import Category, Post

admin.site.register(Post)
admin.site.register(Category)