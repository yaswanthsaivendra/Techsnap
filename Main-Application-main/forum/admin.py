from django.contrib import admin
from .models import Category, ForumPost, Comment, Reply

admin.site.register(Category)
admin.site.register(ForumPost)
admin.site.register(Comment)
admin.site.register(Reply)
