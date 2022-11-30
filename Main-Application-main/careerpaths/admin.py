from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CareerPath, Career_Lessons, Paths, People,peopledescription,lookingfor

# Register your models here.
class InLineCareer_Lessons(admin.StackedInline):
    model = Paths
    extra = 1

class InLinePaths(admin.TabularInline):
    model = Career_Lessons
    extra = 1

class InLinePeople(admin.TabularInline):
    model = People
    extra = 1

class InLinePeopledesc(admin.TabularInline):
    model = peopledescription
    extra = 1

class InLinePeoplelooking(admin.TabularInline):
    model = lookingfor
    extra = 1

class CareerPathAdmin(admin.ModelAdmin):
    inlines = [InLinePaths, InLineCareer_Lessons,InLinePeople,InLinePeopledesc,InLinePeoplelooking]

admin.site.register(CareerPath, CareerPathAdmin)
