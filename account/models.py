from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField('Photo', default='default.jpg',
                              upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} profile'
