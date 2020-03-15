from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
# from dal import autocomplete
from taggit.models import Tag
from account.models import Account
from pet.models import Pet, Care
import reptopia
import logging

logger = logging.getLogger('reptopia.log')


class IndexView(TemplateView):
    template_name = 'index.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """
        today = datetime.today().date()
        notice_list = Notice.objects.filter(notice_from_date__lte=today).filter(notice_to_date__gte=today)

        if notice_list:
            context['notice'] = notice_list[0]
        """

        context['account_count'] = Account.objects.count()
        context['pet_count'] = Pet.objects.count()
        context['care_count'] = Care.objects.count()

        return context

class UserCardSearchView(TemplateView):
    model = Account
    template_name = 'home/card_search.html.j2'

    # custom user model 의 paginator 가 정상작동하지않음에 따른 직접구현
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs_all = Account.objects.filter(is_active=True).order_by('date_joined')
        context['user_list'] = qs_all
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
