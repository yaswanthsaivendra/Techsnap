from django.urls import include, path
from django import urls
from django.conf import settings
from django.conf.urls.static import static
from .views.course import *
from .views.creator_form import *

urlpatterns = [
    path('', index, name='course-ash'),
    path('logout/', logout, name='logout'),

    path('courses/', course_list, name='course-list'),
    path('payment/<str:slug>', CoursePaymentView.as_view(), name='course-payment'),
    path('<str:slug>', course_description, name='course-description'),
    path('enroll/<str:slug>', enroll_in_course, name='course-enrollment'),
    path('update/<str:slug>', update_course, name='update-course'),
    path('reset/<str:slug>', ResetCourse.as_view(), name='reset-course'),
    path('exit-course/<str:slug>', log_out_course, name='exit-course'),
    path('lesson-completed/<str:slug>', lesson_completed_or_redo, name='lesson-completed'),
    path('lesson/<str:course_slug>/<str:slug>', lesson_view, name='lesson-view'),
    # Creator Form urls 
    path('creators-panel/<str:code>', course_form, name='admin-panel'),
    path('creators-panel/course-desc-form/<str:slug>', course_desc_form, name='course-desc-form'),
    path('release-course/<str:slug>', release_course, name='release-course'),
    path('release-to-all-course/<str:slug>', release_to_all_course, name='release-to-all-course'),
    # Course Stats page
    path('creators-panel/course-stats/<str:slug>', stats_page, name='course-stats'),
    # Lesson Stats page
    path('creators-panel/lesson-stats/<str:slug>', lesson_stats_page, name='lesson-stats'),
    # Delete urls 
    path('delete-course/<str:slug>', delete_course, name='delete-course'),
    path('delete-unit/<int:pk>', delete_unit, name='delete-unit'),
    path('delete-anouncement/<int:pk>', delete_anouncement, name='delete-anouncement'),
    path('delete-review/<int:pk>', delete_review, name='delete-review'),
    path('delete-testimonial/<int:pk>', delete_testimonial, name='delete-testimonial'),
    path('delete-faq/<int:pk>', delete_faq, name='delete-faq'),
    path('delete-lesson/<str:slug>', delete_lesson, name='delete-lesson'),
    # Restore and archives
    path('creator-panel/archive', get_archives, name='get-archives'),
    path('creator-panel/restore/<str:slug>', restore, name='restore'),
    # Create objects 
    path('create/<str:slug>/<str:obj>', create_obj, name='create-obj'),
    path('create-review/<str:slug>/<str:lesson_slug>', create_review, name='create-review'),
    # Update objects
    path('update/<str:slug>/<str:obj>/<int:pk>', update_obj, name='update-obj'),
    # Update for unit, anouncement and create for lesson
    path('update/<str:slug>/<str:unit_slug>', update_unit, name='update-unit'),
    # Course Settings
    path('update-course-details/<str:slug>', update_course_details, name='update-course-details'),
    path('update-course-desc/<str:slug>', update_course_desc, name='update-course-desc'),
    path('update-course-info/<str:slug>', update_course_info, name='update-course-info'),
    # hr panel
    path('hr-panel/', hr_panel, name='hr-panel'),
    path('hr-view-creator/<str:code>', get_creator_panel, name='hr-view-creator'),
    # Logs
    path('logs/<str:slug>/<str:username>', get_history, name='get-user-course-history'),
    # timer update 
    path('timer-update/<int:pk>', lesson_timer_update, name='lesson-timer-update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)