import random
import hashlib
import string
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
def get_random_string(desg, user, sd, ed):
    letters = string.ascii_lowercase+string.ascii_uppercase+'0123456789_'
    sdl = str(sd).split('-')
    ssd = sdl[2]+sdl[1]+sdl[0]
    edl = str(ed).split('-')
    eed = edl[2]+edl[1]+edl[0]
    result_str = str(slugify(desg))+'-'+ssd+'-'+eed+'-'
    result_str = result_str + hashlib.sha1((result_str+str(slugify(user))).encode()).hexdigest()[:10]
    return result_str

class Desg(models.Model):
	desg = models.CharField(max_length=30)

	def __str__(self):
		return self.desg

gender_choices = (('M', 'MALE'),
('F', 'FEMALE'))

class File(models.Model):
	name = models.CharField(max_length=50)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	desg = models.ForeignKey(Desg, on_delete=models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()
	course_name = models.CharField(max_length=100)
	gender = models.CharField(choices=gender_choices, max_length=2, default='M')
	#gender1=models.CharField(max_length=100, default='he')
	#gender2=models.CharField(max_length=100, default='his')
	certificates = models.ImageField(upload_to='certificates')
	certificate_pdf = models.FileField(upload_to='certificate_pdf')
	slug = models.SlugField(editable=False,max_length=100)


	def __str__(self):
		return str(self.user)

	def save(self):
		super(File, self).save()
		self.slug = slugify(get_random_string(self.desg.desg, self.user, self.start_date, self.end_date))
		super(File, self).save()

	def get_absolute_url(self):
		return reverse('certificates:certificatedetail', kwargs={'slug': self.slug})
