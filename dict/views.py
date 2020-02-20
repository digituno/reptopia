from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Dictionary
import reptopia
import logging


class DictionaryItemTemplateView(View):
    def get(self, request):
        category = get_object_or_404(Dictionary, pk=request.GET.get('item'))
        dict_list = Dictionary.objects.filter(category=category.item)

        option_list = ""
        if len(dict_list):
            option_list += "<option> --------- </option>"
            for dict in dict_list:
                option_list += "<option value='" + str(dict.pk) + "'>" + dict.item_name + "</option>"

        return HttpResponse(option_list)
