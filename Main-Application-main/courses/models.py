from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from accounts.models import Profile
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.
level = (('Beginner', 'Beginner'),
('Intermidiate', 'Intermidiate'),
('Advanced', 'Advanced'))

class Course(models.Model):
    users = models.ManyToManyField(Profile, blank=True, related_name='course_profile')
    pic = models.ImageField(upload_to='course_pics')
    slug = models.SlugField(max_length=200, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(choices=level, max_length=20)
    cost = models.IntegerField(null=True)
    gst = models.IntegerField(null=True)
    total = models.IntegerField(null=True, editable=False)
    release_status = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.slug

    def save(self):
        super(Course, self).save()
        self.slug = slugify(self.title)
        self.total = self.cost + self.gst
        super(Course, self).save()

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={'slug': self.slug})

    def get_course_topics(self):
        return self.course_topics.all().order_by('position')

    def get_course_lessons(self):
        return self.course_lessons.all().order_by('position')

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_topics')
    title = models.CharField(max_length=100, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    min_time = models.IntegerField(null=True, blank=True)
    num_lessons = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(max_length=100, editable=False, null=True, blank=True)

    def __str__(self):
        try:
            return self.course.title + '-' + self.title + str(self.position)
        except:
            return self.slug

    def save(self):
        super(Topic, self).save()
        self.slug = slugify(self.title)
        super(Topic, self).save()

    def get_absolute_url(self):
        return reverse("courses:topic_detail", kwargs={'course_slug': self.course.slug, "slug": self.slug})

    def get_topic_lessons(self):
        return self.topic_lessons.all().order_by('position')


class Lessons(models.Model):
    slug = models.SlugField(max_length=200, editable=False)
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_lessons', null=True)
    body = RichTextUploadingField(blank=True, null=True)
    position = models.IntegerField()
    resources = models.URLField(max_length=1024, null=True, blank=True)
    min_time = models.IntegerField(default=1)
    xp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        try:
            return self.course.title + '-' + self.topic.title + '-' + self.title + '-' + str(self.position)
        except:
            return self.slug

    def save(self):
        super(Lessons, self).save()
        self.slug = slugify(self.title)
        super(Lessons, self).save()

    def get_lesson_resources(self):
        return self.lesson_resources.all()

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", kwargs={'course_slug': self.topic.course.slug, 'topic_slug': self.topic.slug, 'lesson_slug': self.slug})

class Resources(models.Model):
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='lesson_resources')
    file = models.FileField(upload_to='lesson_resources')

    def __str__(self):
        return self.lesson.title

class UserCourses(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserCourses')
    courses = models.ManyToManyField(Course, related_name='user_courses', blank=True)

    def __str__(self):
        return self.user.username

class UserLessons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courselesson  = models.ForeignKey(Lessons, on_delete=models.CASCADE, null=True)
    position = models.IntegerField(default=0, null=True, blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.user.username + "-" + self.courselesson.slug
        except:
            return self.user.username

def update_user_lesson(sender, instance, *args, **kwargs):
    lesson = instance
    if UserLessons.objects.filter(courselesson=lesson).exists():
        UserLessons.objects.filter(courselesson=lesson).update(position=lesson.position)

class UserTopics(models.Model):
    coursetopic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_com_lessons = models.IntegerField(default=0, null=True, blank=True)
    position = models.IntegerField(default=0, null=True, blank=True)
    courselessons = models.ManyToManyField(UserLessons, blank=True)

    def __str__(self):
        try:
            return self.user.username + "-" + self.coursetopic.slug
        except:
            return self.user.username

def update_user_topic(sender, instance, *args, **kwargs):
    topic = instance
    if UserTopics.objects.filter(coursetopic=topic).exists():
        UserTopics.objects.filter(coursetopic=topic).update(position=topic.position)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserCourses.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.UserCourses.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
post_save.connect(update_user_topic, sender=Topic)
post_save.connect(update_user_lesson, sender=Lessons)