from django.db import models
from django.urls import reverse


class Image(models.Model):
    image = models.ImageField(upload_to='galery_images/%Y/%m/%d')
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('image_detail', args=[self.slug])
