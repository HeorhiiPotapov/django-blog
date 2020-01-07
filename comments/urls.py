from django.urls import path
from . import views


urlpatterns = [
    path('<pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('<pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
]
