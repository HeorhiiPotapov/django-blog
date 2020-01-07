# from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comment
from django.views.generic import UpdateView, DeleteView


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
