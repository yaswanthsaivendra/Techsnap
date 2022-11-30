from django.shortcuts import render
from .models import Jobs, Internships, Application
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

class JobsView(ListView):
    model = Jobs
    template_name = 'jobs.html'

class JobsListView(ListView):
    model = Jobs
    template_name = 'jobs_list.html'

class JobDetailView(DetailView):
	model = Jobs
	template_name = 'job_detail.html'

@login_required
def apply(request, slug, u_code):
    content = Jobs.objects.filter(slug=slug).get()
    user = str(request.user)+' for '+u_code
    if Application.objects.filter(user=user).exists():
        return render(request, 'apply.html', {'jobs': content, 'exist': True})
    else:
        if request.method == 'POST':
            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            gender = request.POST['gender']
            email = request.POST['email']
            ph_num = request.POST['ph_num']
            linkedin = request.POST['linkedin']
            github = request.POST['github']
            resume = request.FILES['file']
            hear = request.POST['hear']
            if hear=='others':
                hear = request.POST['other']
            current_city = request.POST['city']
            postal_code = request.POST['code']
            available_date = request.POST['date']
            which_role = slug
            check = request.POST['scales']
            if check:
                app = Application.objects.create(f_name=f_name, l_name=l_name, gender=gender,
                                            email=email, ph_num=ph_num, linkedin=linkedin,
                                            github=github, resume=resume, hear=hear, current_city=current_city,
                                            postal_code=postal_code, available_date=available_date, which_role=which_role,user=user)
                app.save()
            return render(request, 'apply.html', {'jobs':content, 'f_name': f_name, 'exist': False})
        return render(request, 'apply.html', {'jobs': content, 'exist': False})