import email
import hashlib
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.contrib.auth.models import User, auth
from .models import Subscribe
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.contrib import messages
from django.template.loader import render_to_string

# Create your views here.
def get_unique_string(email):
    result_str = hashlib.sha1((str(slugify(email))).encode()).hexdigest()[:10]
    return result_str

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        if Subscribe.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return redirect('subscribe')
        else:
            sub = Subscribe(email=email, name=name, U_code=get_unique_string(email))
            sub.save()
            link = 'https://www.techsnap.in/newsletter/confirm/'+'?email='+sub.email+'&U_code='+sub.U_code
            #link = '{}?email={}&U_code='.format(request.build_absolute_uri('/newsletter/confirm/'),sub.email,sub.U_code)
            #message = 'Thank you for signing up for my email newsletter! Please complete the process by <a href="{}?email={}&U_code={}"> clicking here to confirm your registration</a>.'.format(request.build_absolute_uri('/newsletter/confirm/'),sub.email,sub.U_code)
            html_message = render_to_string('newsletterconfirmemail.html', { 'context': link })
            plain_msg = strip_tags(html_message)
            send_mail('Techsnap NewsLetter Confirmation', plain_msg, settings.EMAIL_HOST_USER, [sub.email], html_message=html_message)
            return render(request, 'newsletterdone.html')
    else:
        return render(request, 'subscribe.html')

def confirm(request):
    sub = Subscribe.objects.get(email=request.GET['email'])
    if sub.U_code == request.GET['U_code']:
        sub.status = True
        sub.save()
        return render(request, 'newslettersubscribed.html', {'email': sub.name, 'action': 'confirmed'})
    else:
        return render(request, 'subscribe.html', {'email': sub.email, 'action': 'denied'})

def delete(request):
    sub = Subscribe.objects.get(email=request.GET['email'])
    if sub.U_code == request.GET['U_code']:
        sub.status = False
        sub.save()
        return render(request, 'subscribe.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})

def add_sub(request):
    users = User.objects.filter(is_active=True).exclude(email='')
    for user in users:
        sub = Subscribe(email=user.email, name=user.username, U_code=get_unique_string(user.email), status=False)
        sub.save()
    return HttpResponse('done')

def change(request):
    subs = Subscribe.objects.all()
    for sub in subs:
        sub.status = True
        sub.save()
    return HttpResponse('done')

