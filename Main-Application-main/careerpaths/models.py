from django.db import models
from courses.models import Course
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from hashtags.models import Hashtag

# Create your models here.
class CareerPath(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    jobs_in=models.CharField(max_length=10,null=True)
    salary=models.CharField(max_length=15,null=True)
    learners=models.CharField(max_length=15,null=True)
    banner_img = models.ImageField(upload_to='career')
    bloglink = models.URLField(max_length=100)
    webinar_link = models.URLField(max_length=100)
    career_pdf = models.FileField(upload_to='career')
    slug = models.CharField(max_length=50, editable=False, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(CareerPath, self).save()
        self.slug = slugify(self.title)
        super(CareerPath, self).save()

    def careerpaths(self):
        return self.career_paths.all()

    def careerlessons(self):
        return self.career_lesson.all()

    def people(self):
        return self.career_people.all()

    def peopledes(self):
        return self.peopledesc.all()

    def get_absolute_url(self):
        return reverse("careerpaths:careerdetail", kwargs={"slug": self.slug})


class Paths(models.Model):
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='career_paths')
    path_name = models.CharField(max_length=50)
    path_description = models.TextField(max_length=300)
    path_color = models.CharField(max_length=20)
    path_icon = models.ImageField(upload_to='career')
    body = RichTextUploadingField(blank=True, null=True)
    path_updated = models.DateField()

    def __str__(self):
        return self.path_name + ' ' + self.career.title

class Career_Lessons(models.Model):
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='career_lesson')
    lesson_name = models.CharField(max_length=100)
    lesson_description = models.CharField(max_length=500)
    position = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.lesson_name + ' ' + self.career.title

class People(models.Model):
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='career_people')
    people_name = models.CharField(max_length=100)
    people_pic = models.ImageField(upload_to='career')
    people_from = models.ImageField(upload_to='career')

    def __str__(self):
        return self.people_name + ' ' + self.career.title

class peopledescription(models.Model):
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE,related_name='peopledesc')
    desc_people_name = models.CharField(max_length=100)
    desc_people_pic = models.ImageField(upload_to='career')
    desc_people_from = models.CharField(max_length=100)
    desc_people_desc=models.TextField(max_length=500)

    def __str__(self):
        return self.desc_people_name + ' ' + self.career.title

class lookingfor(models.Model):
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='peopledescription')
    company_pic = models.ImageField(upload_to='career')


    def __str__(self):
        return self.career.title