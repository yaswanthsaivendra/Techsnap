from django.contrib import admin
from .models import Course, Lessons, Topic, UserCourses, UserTopics, UserLessons

# Register your models here.
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Lessons)
admin.site.register(UserCourses)
admin.site.register(UserTopics)
admin.site.register(UserLessons)