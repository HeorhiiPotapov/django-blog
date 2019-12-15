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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft')
    tags = TaggableManager()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    class Meta:  # sort ol Post Model by publish parameter
        ordering = ['-publish']

    def __str__(self):  # readeble show this model in admin
        return self.title

    def get_absolute_url(self):  # absolute url adress fo this model what include all arguments from view
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug
                             ])

    def get_like_url(self):
        return reverse('like',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug
                             ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=80)
    # email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

        def __str__(self):
            return 'Comment by {} on {}'.format(self.name, self.post)
