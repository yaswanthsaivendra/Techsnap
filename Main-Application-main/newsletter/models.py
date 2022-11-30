from pandas import DataFrame as df
import os
from django.db import models
from django.http.response import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# Create your models here.
def replace_relatve_path_with_Absolute_url(request, message):
        search_pattern = settings.MEDIA_URL + settings.CKEDITOR_UPLOAD_PATH
        replace_with = request.build_absolute_uri(search_pattern)
        message = message.replace(search_pattern, replace_with)
        return message

class Subscribe(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, default='TechGeek')
    U_code = models.CharField(max_length=200)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.email+' '+str(self.status)

class NEWS_Letter(models.Model):
    subject = models.CharField(max_length=200)
    body = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.subject

    def send(self, request):
        body = self.body
        subscribers = Subscribe.objects.filter(status=True)
        subs = {}
        subs['name'] = []
        subs['email'] = []
        subs['status'] = []
        subs['u_code'] = []
        for sub in subscribers:
            try:
                message = replace_relatve_path_with_Absolute_url(request, body) + '<br><a href="{}?email={}&U_code={}">Unsubscribe</a>.'.format(request.build_absolute_uri('/newsletter/delete/'),
                                                    sub.email,
                                                    sub.U_code)
                html_message = render_to_string('newsletter.html', { 'context': message, 'name':sub.name })
                plain_msg = strip_tags(html_message)
                send_mail(self.subject, plain_msg, settings.EMAIL_HOST_USER, [sub.email], html_message=message)
            except:
                subs['name'] = sub.name
                subs['email'] = sub.email
                subs['status'] = sub.email
                subs['u_code'] = sub.U_code
                
        df(subs).to_csv('media/subs.csv', index=False)
        with open('media/subs.csv', 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition']='inline;filename=subs.csv'
        os.remove('media/subs.csv')
        return response