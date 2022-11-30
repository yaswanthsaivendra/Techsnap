from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import CareerPath

class CareerListView(ListView):
	model = CareerPath
	template_name = 'careerpath.html'

class CareerDetailView(DetailView):
	model = CareerPath
	template_name = 'path.html'
 
def courses(request, slug):
    career_path = get_object_or_404(CareerPath, slug=slug)
    context = {'object_list': career_path.courses.all()}
    print(career_path.courses.all())
    return render(request, 'courses.html', context)