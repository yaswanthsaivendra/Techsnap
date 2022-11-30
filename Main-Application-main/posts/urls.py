from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostsList.as_view(), name='posts_list'),
    path('all-posts/', views.get_all_posts, name='all_posts'),
    path('post-details/<str:postslug>', views.post_details, name='post-details'),
    path('add-imgs/', views.add_imgs, name='add_imgs'),
    path('add-pdf/', views.add_pdf, name='add_pdf'),
    path('add-comment/', views.create_comment, name='add-comment'),
    path('add-reply/', views.create_reply, name='add-reply'),
    path('<slug>/', views.PostsDetail.as_view(), name='post_detail'),

    path('like/<str:postslug>/<str:unlike>/', views.like, name='post-like'),
    path('dislike/<str:postslug>/<str:undislike>/', views.dislike, name='post-dislike'),
    path('follow/<str:postslug>/<str:unfollow>/', views.follow, name='post-follow'),
    path('bookmark/<str:postslug>/<str:unmark>/', views.bookmark, name='post-bookmark'),

    path('report/<str:postslug>/', views.report, name='post-report'),
    path('delete/<str:slug>/', views.delete, name='delete-post'),
    path('update/img-post/<str:slug>/', views.update_img_post, name='update-img-post'),
]
