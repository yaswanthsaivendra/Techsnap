from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

app_name = 'certificates'

urlpatterns = [
    path('', views.CertificatesListView.as_view(), name='certificateslist'),
    path('<slug>', views.CertificateDetailView.as_view(), name='certificatedetail'),
    url(r'^download/(?P<path>.*)&',serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^download_pdf/(?P<path>.*)&',serve,{'document_root':settings.MEDIA_ROOT})
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
