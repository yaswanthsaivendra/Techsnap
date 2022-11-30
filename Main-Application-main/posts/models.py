from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.utils.text import slugify
import string
import random
from hashtags.models import *

# Create your models here.
class Posts(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    slug = models.SlugField(max_length=255)
    tags = models.ManyToManyField(Hashtag, blank=True)
    reports = models.IntegerField(default=0, null=True)
    is_archived = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField(User, blank=True, related_name='bookmarks')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Posts, self).save()
        self.slug = slugify(self.title)
        super(Posts, self).save()
        
    def get_post_imgs(self):
        return self.post_imgs.all().order_by('position')
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'slug': self.slug})

class Report(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200) 

        
class PostImage(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_imgs')
    img_url = models.URLField(max_length=512)
    position = models.IntegerField()
    
    def __str__(self):
        return self.post.title + '-' + str(self.position)


class PostComment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_comments')
    by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.post.title + '-' + str(self.by.user.username)

def reply_generate_code():
    length=18
    base = string.ascii_lowercase+string.ascii_uppercase+string.digits
    while True:
        code = ''.join(random.choices(base, k=length))
        if PostReply.objects.filter(code=code).count()==0:
            break
    return code

class PostReply(models.Model):
    code = models.CharField(max_length=20, default=reply_generate_code)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, null=True)
    reply_to_reply_code = models.CharField(max_length=20, default=None, null=True)

    def __str__(self):
        return self.comment.post.title + '-' + str(self.comment.by.user.username) + '-' + str(self.by.user.username)