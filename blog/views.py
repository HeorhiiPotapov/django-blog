from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.views.generic import ListView, RedirectView, UpdateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Comment
from .forms import ContactForm, CommentForm
from taggit.models import Tag
from django.db.models import Q
from django.contrib import messages
# for sending emails
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
        'tag': tag,
    }
    return render(request, template_name, context)


def post_detail(request, slug):
    object_list = Post.objects.filter(status='Published')
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                return HttpResponseRedirect(request.path_info)
        else:
            comment_form = CommentForm()
            messages.success(request, f'Authenticate please')
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = object_list.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]
    template_name = 'blog/post/detail.html'
    is_liked = False
    user = request.user
    if user not in post.likes.all():
        is_liked = True
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'is_liked': is_liked,
    }
    return render(request, template_name, context)


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        comment = self.get_object()
        slug = comment.post.slug
        return reverse_lazy('post_detail', kwargs={'slug': slug})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False


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


class LikeRedirect(RedirectView):
    def get_redirect_url(self, slug, *args, **kwargs):
        # slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        # need to add is_liked here if using ajax
        is_liked = False
        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
                is_liked = False
            else:
                post.likes.add(user)
                is_liked = True
        return url_


class CommentLike(RedirectView):
    def get_redirect_url(self, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        url_ = comment.get_absolute_url()
        user = self.request.user
        is_liked = False
        if user.is_authenticated:
            if user in comment.likes.all():
                comment.likes.remove(user)
                comment_is_liked = False
            else:
                comment.likes.add(user)
                comment_is_liked = True
        return url_


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['bayjel13@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('send_mail_success')
    context = {
        'form': form
    }
    return render(request, "blog/contact.html", context)


def send_mail_success(request):
    return render(request, 'blog/send_mail_success.html')


def become_author(request):
    return render(request, 'blog/become_author.html')
