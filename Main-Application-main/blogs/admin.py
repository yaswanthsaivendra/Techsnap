from django.contrib import admin
from .models import Blogs, BlogComments

readonly_fields = ("created_at", "updated_at")
# Register your models here.
admin.site.register(Blogs)
admin.site.register(BlogComments)