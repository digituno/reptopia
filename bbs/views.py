from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Post
from .forms import PostCreateForm

import logging

logger = logging.getLogger('reptopia.log')


class PostListView(ListView):
    model = Post
    template_name = 'bbs/post_list.html.j2'
    context_object_name = 'posts'
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
