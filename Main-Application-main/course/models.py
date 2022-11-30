from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import string
import random
from django.utils.text import slugify
from accounts.models import Profile
from hashtags.models import *

# Create your models here.

def generate_code():
    length=6
    while True:
        code = ''.join(random.choices(string.ascii_lowercase,k=length))
        if Lesson.objects.filter(slug=code).count()==0:
            break
    return code

def generate_creator_code():
    length=9
    while True:
        code = ''.join(random.choices(string.ascii_lowercase,k=length))
        if Profile.objects.filter(code=code).count()==0:
            break
    return code

class Course(models.Model):
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    course_title = models.CharField(max_length=100)
    course_img = models.ImageField(upload_to="courses/", null=True)
    course_overview = models.TextField(max_length=500)
    course_duration = models.IntegerField(null=False) # in hours
    course_price = models.CharField(default='FREE', max_length=100)
    slug = models.SlugField(null=True, max_length=300, unique=True)
    course_level = models.CharField(max_length=20, choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced')
        ],
        default='Beginner'
    )
    updates_pre = models.IntegerField(default=1)
    updates_post = models.IntegerField(default=1)
    tags = models.ManyToManyField(Hashtag, blank=True)
    version = models.IntegerField(default=1)
    archive = models.BooleanField(default=False)
    released = models.BooleanField(default=False)

    def __str__(self):
        return self.course_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_title)
        super(Course, self).save(*args, **kwargs)

class Description(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = RichTextField(null=True)
    prerequisites = models.CharField(max_length=300)
    certificate = models.ImageField()
    no_of_learners = models.IntegerField(null=True)

    def __str__(self):
        return self.title

class WhatYouGet(models.Model):
    description = models.ForeignKey(Description, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Testimonial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Anonymous')
    thoughts = models.TextField()
    image = models.ImageField(upload_to='user/', null=True)

    def __str__(self):
        return self.name

class FrequentlyAskedQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=300)

    def __str__(self):
        return self.question

def generate_unit_code():
    length=9
    while True:
        code = ''.join(random.choices(string.ascii_lowercase,k=length))
        if Unit.objects.filter(slug=code).count()==0:
            break
    return code

class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    brief = models.TextField()
    due = models.DateField(null=True)
    slug = models.CharField(default=generate_unit_code , max_length=50, null=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    order = models.IntegerField(null=False, default=1)
    slug = models.SlugField(null=True, max_length=300, unique=True, default=generate_code)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration_Seconds = models.IntegerField(null=False, default=0)
    duration_Minutes = models.IntegerField(null=False, default=0)
    body = RichTextField(null=True)
    xp = models.IntegerField(null=False, default=0)
    resource = models.FileField(upload_to='resources/', null=True, blank=True)
    resource_name = models.CharField(max_length=100, null=False, default='Resource')
    resource_link = models.URLField(max_length=300, null=True, blank=True)
    
    def __str__(self):
        return self.title

class UserCourseMap(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    percentage_completion = models.FloatField(default=0)
    total_xp = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    total_lessons_completed = models.IntegerField(default=0)
    once_completed = models.BooleanField(default=False)
    reset_count = models.IntegerField(default=0)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.user.username} with {self.course.course_title}"

class UserLessonCompletion(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    unlocked = models.BooleanField(default=False)
    timer_min_left = models.IntegerField(default=0)
    timer_sec_left = models.IntegerField(default=0)
    completed_on = models.DateField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return f"{self.user.user.username} with {self.lesson.title}"

class Anouncement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = RichTextField()
    posted_on = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.posted_on

class Comment(models.Model):
    anouncement = models.ForeignKey(Anouncement, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    added_on = models.DateField(auto_now_add=True, null=True)
    thoughts = models.TextField(null=False)
    img = models.ImageField(upload_to='user/', null=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    five = models.IntegerField(default=0)
    four = models.IntegerField(default=0)
    three = models.IntegerField(default=0)
    two = models.IntegerField(default=0)
    one = models.IntegerField(default=0)
    
    def get_total(self):
        return self.five + self.four + self.three + self.two + self.one
    
    def get_average(self):
        star_sum = 5*self.five + 4*self.four + 3*self.three + 2*self.two + 1*self.one
        if self.get_total()==0:
            return 0
        return star_sum / self.get_total()
    
    def __str__(self):
        return self.course.course_title

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='user/', null=True)
    stars = models.IntegerField(default=1)
    body = models.TextField()

    def __str__(self):
        return self.name
    
class EnrollmentHistory(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    log = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"USER [{self.user.user.username}] LOG [{self.log}] DATE [{self.date}]"

class CourseBuildHistory(models.Model):
    log = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"COURSE [{self.course.course_title}] LOG [{self.log}] DATE [{self.date}]"
