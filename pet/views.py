from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from account.models import Account
from .models import Owned
import logging

logger = logging.getLogger('reptopia.log')

class PetListView(ListView):
    model = Owned
    template_name = 'pet/pet_list.html.j2'
    context_object_name = 'owned_list'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(Account, name=self.kwargs['username'])
        query_set = Owned.objects.filter(user=user) # 사육기간 필터입력추가

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
"""
class PetCreateView(LoginRequiredMixin, CreateView):
    model = Owned
    form_class = PetCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
"""
