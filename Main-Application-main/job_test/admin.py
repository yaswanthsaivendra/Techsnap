from django.contrib import admin
from .models import Jobs, Requirments, Responsibilites, Perks, Internships, Application, Terms

# Register your models here.
class RequirmentsInline(admin.TabularInline):
	model = Requirments

class ResponsibilitesInline(admin.TabularInline):
	model = Responsibilites

class PerksInline(admin.TabularInline):
	model = Perks

class TermsInline(admin.TabularInline):
	model = Terms

class JobsAdmin(admin.ModelAdmin):
	inlines = [RequirmentsInline, ResponsibilitesInline, PerksInline, TermsInline]
admin.site.register(Requirments)
admin.site.register(Responsibilites)
admin.site.register(Perks)
admin.site.register(Terms)
admin.site.register(Jobs, JobsAdmin)
admin.site.register(Internships)
admin.site.register(Application)
