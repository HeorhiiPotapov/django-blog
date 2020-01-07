from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# need to pipenv install pytz
class Post(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique_for_date='publish')
    # unique_for_date make slug unique adding a publish date to url
    author = models.ForeignKey(User, on_delete=models.CASCADE,)  # related_name='blog_posts'
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft')
    tags = TaggableManager()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[
                           self.slug
                       ])

    def get_like_url(self):
        return reverse('like',
                       args=[
                           self.slug
                       ])

