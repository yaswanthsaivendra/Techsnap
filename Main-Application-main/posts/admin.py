from django.contrib import admin
from .models import *

# Register your models here.
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class PostsAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]

admin.site.register(Posts, PostsAdmin)
admin.site.register(PostImage)
admin.site.register(PostComment)
admin.site.register(PostReply)
admin.site.register(Report)