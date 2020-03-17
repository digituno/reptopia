from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from dict.models import Dictionary
from .models import Post
from .forms import PostCreateForm
import reptopia

import logging

logger = logging.getLogger('reptopia.log')


class PostListView(TemplateView):
    template_name = 'bbs/post_list.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bbs_type = get_object_or_404(Dictionary, item_name_en=self.kwargs['bbs_type'])
        context['bbs_type'] = bbs_type

        qs_all = Post.objects.filter(board_type_id=bbs_type)
        if bbs_type.item == reptopia._REQUEST_ and not self.request.user.is_staff:
            qs_all.filter(author=self.request.user)
        qs_all.order_by('-created_date')

        paginator = Paginator(qs_all, reptopia._PAGE_CNT_)
        page = self.request.GET.get('page')
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(reptopia._FIRST_PAGE_)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)

        context['post_list'] = post_list
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = Post
    form_class = PostCreateForm
    template_name = 'bbs/post_form.html.j2'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.board_type = get_object_or_404(Dictionary, item_name_en=self.kwargs['bbs_type'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bbs_type = get_object_or_404(Dictionary, item_name_en=self.kwargs['bbs_type'])
        context['bbs_type'] = bbs_type


        if bbs_type.item == reptopia._REQUEST_:
            context['bbs_help_text'] = '등록하고자 하는 개체가 없거나 서비스가 정상적으로 동작하지 못하는 경우 내역을 등록해주세요.' 

        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = settings.LOGIN_URL
    model = Post
    form_class = PostCreateForm
    template_name = 'bbs/post_form.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bbs_type = get_object_or_404(Dictionary, item_name_en=self.kwargs['bbs_type'])
        context['bbs_type'] = bbs_type

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'bbs/post_detail.html.j2'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse_lazy( 'board-list', kwargs={'bbs_type': self.kwargs['bbs_type']})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    """
    def get_queryset(self):
        qs = super(PostDeleteView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])
    """
