from django.urls import path
from . import views

app_name = 'job_test'
urlpatterns = [
    path('', views.JobsView.as_view(), name='jobs'),
    path('all', views.JobsListView.as_view(), name='jobslist'),
    path('<slug>/<u_code>', views.JobDetailView.as_view(), name='jobdetail'),
    path('<slug>/<u_code>/apply', views.apply, name='apply'),
]
