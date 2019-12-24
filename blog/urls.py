from django.urls import path
from . import views
from .feeds import LatestPostFeed

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('tag/<tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('become_author/', views.become_author, name='become_author'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.send_mail_success, name='send_mail_success'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<str:slug>/', views.post_detail, name='post_detail'),
    path('<str:slug>/like/', views.LikeRedirect.as_view(), name='like'),
    path('updete_comment/<pk>/', views.CommentUpdate.as_view(), name='comment_update'),
    path('delete_comment/<pk>/', views.CommentDelete.as_view(), name='comment_delete'),
]
