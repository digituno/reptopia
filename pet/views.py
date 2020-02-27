from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db import transaction
from account.models import Account
from dict.models import AnimalDictionary, Dictionary
from .models import Pet, Care, Feeding
from .forms import PetCreateForm, CareCreateForm
import reptopia
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

    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            form.instance.owner = self.request.user
            pet = form.save(commit=False)
            pet.save()
            form.instance.tags.add(pet.species.common_name_kor)
            form.save_m2m()
            return redirect(pet)
        else:
            return super().form_invalid(form)

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

    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            form.instance.owner = self.request.user
            pet = form.save(commit=False)
            pet.save()
            form.instance.tags.set(pet.species.common_name_kor, clear=True)
            form.save_m2m()
            return redirect(pet)
        else:
            return super().form_invalid(form)


class PetDeleteView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request, userid, pk):
        pet = get_object_or_404(Pet, pk=pk)
        pet.tags.clear()
        pet.delete()
        return redirect('pet-list', userid=userid)


class PetDetailView(LoginRequiredMixin, DetailView):
    login_url = settings.LOGIN_URL
    model = Pet
    template_name = 'pet/pet_detail.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = get_object_or_404(Pet, pk=self.kwargs['pk']);

        care_list = Care.objects.filter(pet=pet).order_by('-date', '-created_datetime')
        context['care_list'] = care_list

        dict_weight = get_object_or_404(Dictionary, pk=6)
        weight_list = Care.objects.filter(pet=pet).filter(type=dict_weight).order_by('-date', '-created_datetime')
        context['weight_list'] = weight_list

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

    @transaction.atomic
    def form_valid(self, form):
        # 사육일지유형이 먹이주기 일 때
        if form.cleaned_data['type'].id == reptopia._CARE_FEEDING_:
            feeding = Feeding()
            feeding.prey_type = get_object_or_404(Dictionary, pk=form.cleaned_data['prey_type'].id)
            feeding.prey_size = get_object_or_404(Dictionary, pk=form.cleaned_data['prey_size'].id)
            feeding.prey_weight = form.cleaned_data['prey_weight']
            feeding.prey_quantity = form.cleaned_data['prey_quantity']
            feeding.save()

            form.instance.feeding = feeding


        return super().form_valid(form)


class CareDeleteView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    @transaction.atomic
    def get(self, request, userid, petid, careid):
        care = get_object_or_404(Care, pk=careid)

        if care.feeding:
            feeding = care.feeding
            feeding.delete()

        care.delete()
        return redirect('pet-detail', userid=userid, pk=petid)


class SpeciesSearchTemplateView(View):
    def get(self, request):
        q = request.GET.get('term', '').capitalize()
        logger.debug(q)
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
