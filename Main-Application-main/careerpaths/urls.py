from django.urls import path
from . import views

app_name = 'careerpaths'

urlpatterns = [
    path('', views.CareerListView.as_view(), name='careerslist'),
    path('<slug>/', views.CareerDetailView.as_view(), name='careerdetail'),
    path('<slug>/courses/', views.courses, name='courses')
]
