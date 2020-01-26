from django.urls import path
from . import views
from .feeds import LatestPostFeed

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('tag/<tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
    path('success/', views.send_mail_success, name='send_mail_success'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<str:slug>/', views.post_detail, name='post_detail'),
    path('<str:slug>/like/', views.LikeRedirect.as_view(), name='like'),
]
