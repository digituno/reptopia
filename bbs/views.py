from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from dict.models import Dictionary
from .models import Post, Notice
from .forms import PostCreateForm, NoticeCreateForm
import reptopia

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

class NoticeListView(ListView):
    model = Notice
    template_name = 'bbs/notice_list.html.j2'
    context_object_name = 'notice_list'
    paginate_by = 10

    def get_queryset(self):
        return Notice.objects.all()


class NoticeCreateView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = Notice
    form_class = NoticeCreateForm
    template_name = 'bbs/notice_form.html.j2'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.board_type =  get_object_or_404(Dictionary, item=reptopia._NOTICE_)
        form.instance.board_status = get_object_or_404(Dictionary, item=reptopia._BBS_NORM_)

        return super().form_valid(form)


class NoticeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = settings.LOGIN_URL
    model = Notice
    form_class = NoticeCreateForm
    template_name = 'bbs/notice_form.html.j2'


class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'bbs/notice_detail.html.j2'


class NoticeDeleteView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        notice.delete()
        return redirect('notice-list')
