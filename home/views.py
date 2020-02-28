from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
# from bbs.models import Notice
from account.models import Account
from pet.models import Pet, Care
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
