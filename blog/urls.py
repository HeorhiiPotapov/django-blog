from django.urls import path
from . import views
from .views import SearchView
from .feeds import LatestPostFeed

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<year>/<month>/<day>/<post>/', views.post_detail, name='post_detail'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', SearchView.as_view(), name='search'),
    path('<year>/<month>/<day>/<post>/like/', views.LikeRedirect.as_view(), name='like'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.send_mail_success, name='send_mail_success'),
]
