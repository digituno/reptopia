from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from account.models import Account
from .models import Pet
from dict.models import AnimalDictionary
from .forms import PetCreateForm
import logging
import json

logger = logging.getLogger('reptopia.log')

class PetListView(ListView):
    model = Pet
    template_name = 'pet/pet_list.html.j2'
    context_object_name = 'pet_list'
    paginate_by = 10

    def get_queryset(self):
        current_user = get_object_or_404(Account, pk=self.kwargs['userid'])
        query_set = Pet.objects.filter(owner=current_user) # 사육기간 필터입력추가

        """
        if 'speciesid' in self.request.GET:
            species = get_object_or_404(AnimalDictionary, pk=self.request.GET['speciesid'])
            query_set = query_set.filter(species=species)
        """
        return query_set

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = get_object_or_404(Account, pk=self.kwargs['userid'])
        have_species_list = Pet.objects.values_list('species', flat=True).distinct()
        species_list = AnimalDictionary.objects.filter(id__in=have_species_list)

        context['owner'] = owner
        context['species_list'] = species_list

        return context
    """

class PetCreateView(CreateView):
    model = Pet
    form_class = PetCreateForm
    template_name = 'pet/pet_form.html.j2'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_absolute_url(self):
        return reverse('pet-detail', kwargs={'pk': self.pk})


class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet/pet_detail.html.j2'


class SpeciesSearchTemplateView(View):
    def get(self, request):
        q = request.GET.get('term', '').capitalize()
        logger.debug(q)
        # animal_dict_list = AnimalDictionary.objects.filter(Q(common_name_kor_icontains=item)|Q(common_name_kor_icontains=item))
        search_qs = AnimalDictionary.objects.filter(common_name_kor__icontains=q)

        results  = []
        for r in search_qs:
            value = {}
            value['id'] =r.id
            value['label'] =r.common_name_kor
            results.append(value)
        logger.debug(results)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
