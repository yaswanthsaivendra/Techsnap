from django.shortcuts import render
from .models import File
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

class CertificatesListView(ListView):
	model = File
	template_name = 'certificates_list.html'

class CertificateDetailView(DetailView):
	model = File
	template_name = 'certificate_detail.html'

def download(request, path):
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read())
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response
	raise Http404

def download_pdf(request, path):
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read())
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response
	raise Http404
