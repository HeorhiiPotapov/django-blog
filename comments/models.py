from django.db import models
from blog.models import Post
from django.contrib.auth.models import User
from django.urls import reverse


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[
                           self.post.slug
                       ])
