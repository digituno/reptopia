from django.urls import path, include
from . import views as pet_views

urlpatterns = [
    path('<username>/', pet_views.PetListView.as_view(), name='pet-list'),
    path('<username>/add', pet_views.PetCreateView.as_view(), name='pet-add'),
    path('<username>/<int:pk>', pet_views.PetDetailView.as_view(), name='pet-detail'),
    path('ajax/ajax-search-species', pet_views.SpeciesSearchTemplateView.as_view(), name='ajax-search-species'),
]
