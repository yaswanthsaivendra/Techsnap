from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogsListView.as_view(), name='blogslist'),
    path('create/', views.BlogCreateView.as_view(), name='blogcreate'),
    path('postcomment/', views.post_comment, name='postcomment'),
    path('<slug>/', views.BlogDetailView.as_view(), name='blogdetail'),
    path('<slug>/edit/', views.BlogUpdateView.as_view(), name='blogedit'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
