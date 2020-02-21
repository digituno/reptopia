from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from .models import Post
from .forms import PostCreateForm

import logging

logger = logging.getLogger('reptopia.log')


class PostListView(ListView):
    model = Post
    template_name = 'bbs/post_list.html.j2'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all()


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = Post
    form_class = PostCreateForm
    template_name = 'bbs/post_form.html.j2'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = settings.LOGIN_URL
    model = Post
    form_class = PostCreateForm
    template_name = 'bbs/post_form.html.j2'


class PostDetailView(DetailView):
    model = Post
    template_name = 'bbs/post_detail.html.j2'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    """
    def get_queryset(self):
        qs = super(PostDeleteView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])
    """
