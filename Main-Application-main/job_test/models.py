import hashlib
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
def u_code_gen(d, jt, c, pd, jd, v):
    res = d+jt+c+str(pd)+jd+str(v)
    res = hashlib.sha1(res.encode()).hexdigest()[:10]
    return res

class Jobs(models.Model):
    banner1 = models.ImageField(upload_to='banners')
    banner2 = models.ImageField(upload_to='banners')
    company = models.CharField(max_length=100, default='TechSnap')
    desg = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    types = [
        ('FullTime', 'FullTime'),
        ('PartTime', 'PartTime'),
        ('Internship', 'Internship')
    ]
    job_type = models.CharField(max_length=100, choices=types)
    job_mode=models.CharField(max_length=200,default='virtual')
    jd = models.TextField()
    published_date = models.DateField()
    vacancies = models.IntegerField(default=1)
    experience_min = models.IntegerField(default=1)
    experience_max = models.IntegerField(default=1)
    experience_in = models.CharField(max_length=6, choices=[('Months', 'Months'), ('Years', 'Years')], default='Months')
    mustskills=models.CharField(max_length=200,null=False,default=1)
    goodkills=models.CharField(max_length=200,null=False,default=1)
    slug = models.SlugField(editable=False, max_length=100)
    u_code = models.SlugField(editable=False, max_length=100, default='1234567890')
    opened = models.BooleanField(default=False)
    release=models.BooleanField(default=False)
    featured=models.BooleanField(default=False)

    def __str__(self):
        return self.desg

    def get_responsibilites(self):
        return self.responsibilites_set.all()

    def get_requirments(self):
        return self.requirments_set.all()

    def get_perks(self):
        return self.perks_set.all()

    def get_terms(self):
        return self.terms_set.all()

    def save(self):
        super(Jobs, self).save()
        self.slug = slugify(self.desg)
        self.u_code = slugify(u_code_gen(self.desg, self.job_type, self.company, self.published_date, self.jd, self.vacancies))
        super(Jobs, self).save()

    def get_absolute_url(self):
        return reverse('job_test:jobdetail', kwargs={'slug': self.slug, 'u_code': self.u_code})

class Responsibilites(models.Model):
    res = models.TextField()
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.desg

class Requirments(models.Model):
    req = models.TextField()
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.desg

class Perks(models.Model):
    perk = models.TextField()
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.desg

class Terms(models.Model):
    term = models.TextField()
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.desg

class Internships(models.Model):
    internship = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    published_date = models.DateField()
    url = models.URLField()

    def __str__(self):
        return self.internship+' from '+self.company

class Application(models.Model):
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    ph_num = models.CharField(max_length=15)
    linkedin = models.URLField(max_length=200)
    github = models.URLField(max_length=200)
    resume = models.FileField(upload_to='resumes')
    hear = models.CharField(max_length=100)
    current_city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    available_date = models.DateField()
    which_role = models.CharField(max_length=100)
    user = models.CharField(max_length=300, default='techsnap for 1234567890')

    def __str__(self):
        return self.f_name+' '+self.l_name+' for '+self.which_role
