from django.contrib import admin
from .models import Subscribe, NEWS_Letter

# Register your models here.
def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

send_newsletter.short_description = "Send selected Newsletters to all subscribers"

class NEWS_Letter_Admin(admin.ModelAdmin):
    actions = [send_newsletter]

admin.site.register(Subscribe)
admin.site.register(NEWS_Letter, NEWS_Letter_Admin)
