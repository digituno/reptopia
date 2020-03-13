from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
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
    paginate_by = reptopia._PAGE_CNT_ 

    def get_queryset(self):
        current_user = get_object_or_404(Account, pk=self.kwargs['userid'])
        query_set = Pet.objects.filter(owner=current_user) # 사육기간 필터입력추가

        if 'speciesid' in self.request.GET:
            species = get_object_or_404(AnimalDictionary, pk=self.request.GET['speciesid'])
            query_set = query_set.filter(species=species)

        query_set.order_by('created_date')
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = get_object_or_404(Account, pk=self.kwargs['userid'])
        have_species_list = Pet.objects.values_list('species', flat=True).distinct()
        species_list = AnimalDictionary.objects.filter(id__in=have_species_list)

        context['owner'] = owner
        context['species_list'] = species_list

        return context

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

            current_pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
            form_pet = form.save(commit=False)
            if current_pet.id == form_pet.id and current_pet.image != form_pet.image:
                current_pet.image.delete()

            pet.save()
            form.instance.tags.set(pet.species.common_name_kor, clear=True)
            form.save_m2m()
            return redirect(pet)
        else:
            return super().form_invalid(form)


class PetDeleteView(LoginRequiredMixin, DeleteView):
    login_url = settings.LOGIN_URL
    model = Pet 

    def get_success_url(self):
        owner = self.object.owner
        return reverse_lazy('pet-list', kwargs={'userid': owner.id})

    """
    @transaction.atomic
    def get(self, request, userid, pk):
        pet = get_object_or_404(Pet, pk=pk)
        # pet.tags.clear()
        pet.delete()
        return redirect('pet-list', userid=userid)
    """

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet/pet_detail.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        care_type_list = Dictionary.objects.filter(category=reptopia._CARE_)
        context['care_type_list'] = care_type_list

        pet = get_object_or_404(Pet, pk=self.kwargs['pk']);
        care_list_all = Care.objects.filter(pet=pet).order_by('-date', '-created_datetime')

        if 'care_type' in self.request.GET:
            care_list_all = care_list_all.filter(type_id=self.request.GET['care_type'])

        paginator = Paginator(care_list_all, reptopia._PAGE_CNT_)
        page = self.request.GET.get('page')
        try:
            care_list = paginator.page(page)
        except PageNotAnInteger:
            care_list = paginator.page(reptopia._FIRST_PAGE_)
        except EmptyPage:
            care_list = paginator.page(paginator.num_pages)
        context['care_list'] = care_list

        dict_weight = get_object_or_404(Dictionary, item=reptopia._WEIGHT_)
        weight_list = Care.objects.filter(pet=pet).filter(type=dict_weight).order_by('-date', '-created_datetime')
        context['weight_list'] = weight_list[:10]

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
        # if form.cleaned_data['type'].id == reptopia._CARE_FEEDING_:
        care_feeding = get_object_or_404(Dictionary, item=reptopia._FEEDING_)
        if form.cleaned_data['type'].id == care_feeding.id:
            feeding = Feeding()
            feeding.eat_type = get_object_or_404(Dictionary, pk=form.cleaned_data['eat_type'].id)
            feeding.prey_type = get_object_or_404(Dictionary, pk=form.cleaned_data['prey_type'].id)
            if form.cleaned_data['prey_size'] is not None:
                feeding.prey_size = get_object_or_404(Dictionary, pk=form.cleaned_data['prey_size'].id)
            feeding.prey_weight = form.cleaned_data['prey_weight']
            feeding.prey_quantity = form.cleaned_data['prey_quantity']
            feeding.save()
            form.instance.feeding = feeding

        return super().form_valid(form)


class CareDeleteView(LoginRequiredMixin, DeleteView):
    login_url = settings.LOGIN_URL
    model = Care

    def get_success_url(self):
        pet = self.object.pet
        return reverse_lazy('pet-detail', kwargs={'userid': pet.owner.id, 'pk':pet.id})


class SpeciesSearchTemplateView(View):
    def get(self, request):
        q = request.GET.get('term', '').capitalize()
        logger.debug(q)
        search_qs = AnimalDictionary.objects.filter(Q(common_name_kor__icontains=q)|Q(common_name__icontains=q))

        results  = []
        for r in search_qs:
            value = {}
            value['id'] = r.id
            value['label'] = '[' + r.common_name + '] '+ r.common_name_kor
            results.append(value)
        logger.debug(results)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
