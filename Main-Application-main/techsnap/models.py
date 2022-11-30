from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    msg = models.TextField()
    def __str__(self):
        return 'Msg from '+self.name

class Contribute(models.Model):
    F_name = models.CharField(max_length=200)
    L_name = models.CharField(max_length=200)
    email = models.EmailField()
    linkedin= models.URLField(max_length=300)
    how=models.CharField(max_length=300)
    msg = models.TextField()
    def __str__(self):
        return 'Msg from '+self.F_name

class sbu(models.Model):
    F_name = models.CharField(max_length=200)
    L_name = models.CharField(max_length=200)
    email = models.EmailField()
    linkedin= models.URLField(max_length=300)
    how=models.CharField(max_length=300)
    msg = models.TextField()
    def __str__(self):
        return 'Msg from '+self.F_name

class Storage_Media(models.Model):
    img = models.ImageField(upload_to='storage')
    name = models.CharField(max_length=200, default='logo', unique=True)
    def __str__(self):
        return str(self.img)

topic_choices = [ ("Account", "Account"), ("Enrollment", "Enrollment"), ("Communication", "Communication"), ("Certification", "Certification"), ("Others", "Others"), ]

class FAQ(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length = 50, choices = topic_choices, default="Others")
    question = models.TextField()
    answer = models.TextField()
    def __str__(self):
        return str(self.topic)