from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
# from dal import autocomplete
from taggit.models import Tag
from account.models import Account
from pet.models import Pet, Care
from dict.models import Dictionary
from bbs.models import Post
import reptopia
import logging

logger = logging.getLogger('reptopia.log')


class IndexView(TemplateView):
    template_name = 'index.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bbs_type = get_object_or_404(Dictionary, item=reptopia._NOTICE_)
        notice_list = Post.objects.filter(board_type_id=bbs_type).order_by('-created_date')[:3]
        context['notice_list'] = notice_list


        context['account_count'] = Account.objects.filter(is_active=True).count()
        context['pet_count'] = Pet.objects.count()
        context['care_count'] = Care.objects.count()

        return context

class UserCardSearchView(TemplateView):
    template_name = 'home/user_card_search.html.j2'

    # custom user model 의 paginator 가 정상작동하지않음에 따른 직접구현
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs_all = Account.objects.filter(is_active=True).order_by('-date_joined')[:100]
        paginator = Paginator(qs_all, reptopia._PAGE_CNT_*2)
        page = self.request.GET.get('page')


        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            user_list = paginator.page(reptopia._FIRST_PAGE_)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages)
        context['user_list'] = user_list

        return context


class PetCardSearchView(TemplateView):
    template_name = 'home/pet_card_search.html.j2'

    # custom user model 의 paginator 가 정상작동하지않음에 따른 직접구현
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs_all = Pet.objects.order_by('-created_date')[:100]
        paginator = Paginator(qs_all, reptopia._PAGE_CNT_*2)
        page = self.request.GET.get('page')


        try:
            pet_list = paginator.page(page)
        except PageNotAnInteger:
            pet_list = paginator.page(reptopia._FIRST_PAGE_)
        except EmptyPage:
            pet_list = paginator.page(paginator.num_pages)
        context['pet_list'] = pet_list

        return context


class CareCardSearchView(TemplateView):
    template_name = 'home/care_card_search.html.j2'

    # custom user model 의 paginator 가 정상작동하지않음에 따른 직접구현
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs_all = Care.objects.order_by('-created_datetime')[:100]
        paginator = Paginator(qs_all, reptopia._PAGE_CNT_*2)
        page = self.request.GET.get('page')

        try:
            care_list = paginator.page(page)
        except PageNotAnInteger:
            care_list = paginator.page(reptopia._FIRST_PAGE_)
        except EmptyPage:
            care_list = paginator.page(paginator.num_pages)
        context['care_list'] = care_list

        return context

"""
class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
"""
