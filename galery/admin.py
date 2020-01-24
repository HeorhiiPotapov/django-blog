from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Image, ImageAdmin)
