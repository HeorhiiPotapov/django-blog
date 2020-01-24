from django.urls import path
from . import views


urlpatterns = [
    path('', views.images_list, name='images_list'),
    path('<slug>/', views.image_detail, name='image_detail'),
]
