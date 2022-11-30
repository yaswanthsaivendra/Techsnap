from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('confirm/', views.confirm, name='confirm'),
    path('delete/', views.delete, name='delete'),
    path('add_sub/', views.add_sub, name='add_sub'),
    path('change/', views.change, name='change')
]
