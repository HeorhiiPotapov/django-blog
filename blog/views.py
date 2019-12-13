from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Q


def post_list(request, tag_slug=None):
    # desable to show posts with status='Draft'
    object_list = Post.objects.filter(status='Published')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    template_name = 'blog/post/list.html'
    context = {
        'page': page,
        'posts': posts,
        'tag': tag
    }
    return render(request, template_name, context)


# class PostListView(ListView):
#     queryset = Post.objects.filter(status='Published')
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    object_list = Post.objects.filter(status='Published')
    post = get_object_or_404(Post, slug=post,
                             status='Published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = object_list.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]
    template_name = 'blog/post/detail.html'
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }
    return render(request, template_name, context)


class SearchView(ListView):
    model = Post
    template_name = 'blog/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        posts = Post.objects.filter(status='Published')
        object_list = posts.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return object_list
