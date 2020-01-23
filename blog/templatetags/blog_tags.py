# import markdown
# from django.utils.safestring import mark_safe
from django.db.models import Count
from ..models import Post
from django import template
from comments.models import Comment

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.filter(status='Published').count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=10):
    latest = Post.objects.filter(status='Published')
    latest_posts = latest.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count
                                 ('comments')).order_by('-total_comments')[:count]


@register.simple_tag
def get_sidebar_tags():
    return Post.tags.all()


# @register.filter(name='markdown')
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_latest_comments(count=10):
    return Comment.objects.all()[:count]
