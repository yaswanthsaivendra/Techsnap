from django.urls import path
from . views import home ,follow, feedback

app_name = 'hashtags'

urlpatterns = [
    path("<str:hashtag>/", home,name='home'),
    path("<str:hashtag>/follow/",follow ,name='follow'),
    path("<str:hashtag>/feedback/",feedback ,name='feedback'),
]