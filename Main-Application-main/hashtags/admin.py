from django.contrib import admin
from .models import Hashtag, Feedback 
# Register your models here.


class HashtagAdmin(admin.ModelAdmin):
    list_display=('title','is_active')
    list_editable=('is_active',)

admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Feedback)
