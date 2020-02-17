from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from account.models import Account
from .models import Pet, Care
from dict.models import AnimalDictionary
from .forms import PetCreateForm, CareCreateForm
import logging
import json

logger = logging.getLogger('reptopia.log')

class PetListView(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
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

class PetCreateView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = Pet
    form_class = PetCreateForm
    template_name = 'pet/pet_form.html.j2'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    login_url = settings.LOGIN_URL
    model = Pet
    form_class = PetCreateForm
    template_name = 'pet/pet_form.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
        context['pet'] = pet

        return context


class PetDeleteView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request, userid, pk):
        pet = get_object_or_404(Pet, pk=pk)
        pet.delete()
        return redirect('pet-list', userid=userid)


class PetDetailView(LoginRequiredMixin, DetailView):
    login_url = settings.LOGIN_URL
    model = Pet
    template_name = 'pet/pet_detail.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = get_object_or_404(Pet, pk=self.kwargs['pk']);
        # weight = get_object_or_404(Dictionary, item=reptopia._WEIGHT_)

        """
        from_date = '2019-01-01'
        to_date = '2019-11-13'
        if 'from_date' in self.request.GET and 'to_date' in self.request.GET:
            from_date = self.request.GET['from_date']
            to_date = self.request.GET['to_date']
            care_list = Care.objects.filter(pet=pet).filter(date__range=[from_date, to_date]).order_by('-date', '-created_datetime')
        """
        care_list = Care.objects.filter(pet=pet).order_by('-date', '-created_datetime')
        logger.debug(care_list)

        """
        if 'care_type' in self.request.GET:
            care_list = care_list.filter(type_id=self.request.GET['care_type'])

        weight_list = Care.objects.filter(pet=pet).filter(type=weight).order_by('date')
        care_type_list = Dictionary.objects.filter(category=reptopia._CARE_)
        """

        context['care_list'] = care_list

        """
        context['weight_list'] = weight_list
        context['care_type_list'] = care_type_list
        """
        return context


class CareCreateView(LoginRequiredMixin, CreateView):
    model = Care
    form_class = CareCreateForm
    template_name = 'pet/care_form.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = get_object_or_404(Pet, pk=self.kwargs['petid'])
        context['pet'] = pet
        return context

    """
    def post(self, request, *args, **kwargs):
        if 'weight' in request.POST:
            care = get_object_or_404(Care, pk=self.kwargs['petid'])
            weight = CareWeight(care=care, weight=request.POST.get('weight'))
            weight.save()
        return super().post(self, request, *args, **kwargs)
    """


class CareDeleteView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request, userid, petid, careid):
        care = get_object_or_404(Care, pk=careid)
        care.delete()
        return redirect('pet-detail', userid=userid, pk=petid)



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
