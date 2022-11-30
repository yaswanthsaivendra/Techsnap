from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from hashtags.models import *

# Create your models here.
class Blogs(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    banner_img = models.ImageField(upload_to='banners', null=True)
    title = models.CharField(max_length=200)
    body = RichTextUploadingField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    slug = models.SlugField(editable=False,max_length=200)

    user_status = models.BooleanField(default=False)

    feature_status=models.BooleanField(default=False)
    trending1_status=models.BooleanField(default=False)
    trending2_status=models.BooleanField(default=False)
    trending3_status=models.BooleanField(default=False)
    trending4_status=models.BooleanField(default=False)

    recent_status=models.BooleanField(default=False)

    status = models.BooleanField(default=False)
    date_published= models.DateTimeField(auto_now_add=True,null=False)
    date_modified = models.DateTimeField(auto_now=True,null=False)
    tags = models.ManyToManyField(Hashtag, blank=True)

    def __str__(self):
        return str(self.author)+' '+self.title

    def save(self, *args, **kwargs):
        super(Blogs, self).save()
        self.slug = slugify(self.title)
        super(Blogs, self).save()

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blogs:blogdetail', kwargs={'slug': self.slug})

class BlogComments(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='blog_comments')
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    parent_blog = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:10]+'... by '+self.user.username