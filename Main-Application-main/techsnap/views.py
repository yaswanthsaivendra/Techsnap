from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact, Contribute, Storage_Media,sbu
from plans.models import *
from accounts.models import *

# Create your views here.
def index(request):
	return render(request, 'index.html')

def aboutus(request):
	return render(request, 'abouts.html')

def services(request):
	return render(request, 'services.html')

@login_required
def projects(request):
	return render(request, 'projects.html', {'section':projects})

@login_required
def tutorials(request):
	return render(request, 'tutorials.html', {'section':tutorials})

def careerpath(request):
	return render(request, 'careerpath_blog.html')

def error(request):
	return render(request, '404.html')

def cookies(request):
	return render(request, 'cookies.html')

def privacy(request):
	return render(request, 'privacy.html')

def security(request):
	return render(request, 'security.html')

def terms(request):
	return render(request, 'terms.html')

def design(request):
	return render(request, 'design.html')

@login_required
def contact(request):
	if request.method=='POST':
		message = request.POST['message']
		name = request.POST['name']
		email = request.POST['email']
		message += '\n\nfrom\n'+name+'\n'+email
		subject = 'Mail from '+name
		c = Contact.objects.create(name=name, email=email, msg=message)
		c.save()
		send_mail(subject, message, settings.EMAIL_HOST_USER, ['snapthetechqueries@gmail.com'], fail_silently=False)
	return render(request, 'contact.html')

def contribute(request):
	if request.method=='POST':
		info= request.POST['info']
		fname = request.POST['fname']
		email = request.POST['email']
		lname=request.POST['lname']
		linkedin=request.POST['linkedin']
		how=request.POST['how']

		info+= '\n\nfrom\n'+fname+'\n'+email
		subject = 'Mail from '+fname
		f= sbu.objects.create(F_name=fname,L_name=lname,linkedin=linkedin,how=how,email=email,msg=info)
		f.save()
		send_mail(subject,info, settings.EMAIL_HOST_USER, ['snapthetechqueries@gmail.com'], fail_silently=False)
	return render(request, 'get_involved.html')

from django.contrib import messages
def sbuform(request):
	if request.method=='POST':
		info= request.POST['info']
		fname = request.POST['fname']
		email = request.POST['email']
		lname=request.POST['lname']
		linkedin=request.POST['linkedin']
		how=request.POST['how']

		subject1= 'Sucessfully registered'
		info1='Dear  '+fname+'\n\nThank you for registering to the AI and ML event By MLSnap.\nThis email serves as a confirmation that your registration is successful and that you are officially a part of the event as well the Techsnap Family.Enjoy!\n\nWe Look forward to seeing you there,\n\nRegards,\nTechsnap Team'
		f= Contribute.objects.create(F_name=fname,L_name=lname,linkedin=linkedin,how=how,email=email,msg=info)
		f.save()
		messages.success(request, 'succesfully registered to ML Event')
		send_mail(subject1,info1, settings.EMAIL_HOST_USER, [email], fail_silently=False)
	return render(request,'sbuform.html')

def learnerstories(request):
	return render(request, 'learnerstories.html')

def ourpeople(request):
	return render(request, 'ourpeople.html')

@login_required
def invest(request):
	return render(request, 'invest.html')

def passwordgenerator(request):
    return render(request, 'passgen.html')

def qrcodegenerator(request):
    return render(request, 'qrcode.html')

def old(request):
    return render(request, 'old.html')

def storage(request):
    store = Storage_Media.objects.all()
    return render(request, 'storage.html', {'content': store})

def tasks(request):
    return render(request, 'tasks.html')

def faq(request):
    return render(request, 'faq1.html')

def community(request):
    return render(request, 'community.html')

def accessdenied(request):
    return render(request, 'accessdenied.html')

def path(request):
    return render(request, 'path.html')

def learner(request):
    return render(request, 'learnerstory.html')

def nextpage(request):
    if request.method=="POST":
        email = request.POST['email']
        return render(request, 'subscribe.html', {'email': email})

def desc(request):
    return render(request, 'course_description.html')

def reso(request):
    return render(request, 'resources.html')

def price(request):
	current_price = Profile.objects.get(user=request.user).plan.price
	monthly = Plan.objects.filter(is_dummy=False, duration=30, price__gt=current_price)
	half_yearly = Plan.objects.filter(is_dummy=False, duration=180, price__gt=current_price)
	yearly = Plan.objects.filter(is_dummy=False, duration=364, price__gt=current_price)
	payload = {
		'monthly': monthly,
		'half_yearly': half_yearly,
		'yearly': yearly
	}
	return render(request,'pricing.html', payload)

def datablog(request):
    return render(request,'datasnap.html')

def foumlist(request):
    return render(request,'forum_list.html')

def forumposts(request):
    return render(request,'forum_posts.html')

def sitemaps(request):
	return render(request, 'sitemap.xml', content_type='text/xml')

from django.views.generic.list import ListView
from .models import FAQ

class FaqList(ListView):
    model = FAQ
    template_name = 'faq1.html'

'''def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "400.html", {})'''
