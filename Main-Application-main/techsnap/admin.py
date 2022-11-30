from django.contrib import admin
from .models import Contact, Contribute, Storage_Media, FAQ,sbu

# Register your models here.
class Storage_Media_Admin(admin.ModelAdmin):
  list_display = ('name', 'img')

admin.site.register(Contact)
admin.site.register(Storage_Media, Storage_Media_Admin)
admin.site.register(FAQ)
admin.site.register(Contribute)

admin.site.register(sbu)
