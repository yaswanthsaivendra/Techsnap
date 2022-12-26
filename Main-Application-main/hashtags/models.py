from django.db import models

# Create your models here.


class Hashtag(models.Model):
    title = models.CharField("hashtag name", max_length=100)
    is_active = models.BooleanField(default=False)
    followers = models.PositiveBigIntegerField(default=0, editable=False)
    image = models.ImageField(upload_to='hashtag_images/')
    description = models.TextField()



    def __str__(self) :
        return self.title


class Feedback(models.Model):
    FEEDBACK_CHOICES = (
        ('IP', "Intellectual Property Violation"),
        ('VODO', "Violence or Dangerous organizations"),
        ('BOH', "Bullying or Harassment"),
    )
    text = models.CharField(max_length=200, choices=FEEDBACK_CHOICES)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.hashtag.title} - {self.text} "