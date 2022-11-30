from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('<topic_id>/<id>/topiccomplete/', views.topiComp, name='topic_complete'),
    path('', views.CourseListView.as_view(), name='course_list'),
    path('payment/<slug>', views.payment, name='payment'),
    path('buy/<slug>/', views.buy_techsnap_cash, name='buy_techsnap_cash'),
    path('<slug>/getdata/', views.lesson_data, name='lesson_data'),
    path('<slug>/enroll/', views.course_enroll, name='course_enroll'),
    path('<slug>/reflect/', views.reflect, name='reflect'),
    path('<slug>', views.CourseDetailView.as_view(), name='course_detail'),
    path('<course_slug>/<slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('<course_slug>/<topic_slug>/<lesson_slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('mycourses/', views.mycourses, name='mycourses'),
]
