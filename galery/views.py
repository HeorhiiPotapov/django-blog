from django.shortcuts import render, get_object_or_404
from .models import Image


def images_list(request):
    images = Image.objects.all()
    template_name = 'blog/images_list.html'
    context = {'images': images}
    return render(request, template_name, context)


def image_detail(request, slug):
    image = get_object_or_404(Image, slug=slug)
    template_name = 'blog/image_detail.html'
    context = {'image': image}
    return render(request, template_name, context)
