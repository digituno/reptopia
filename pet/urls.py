from django.urls import path, include
from . import views as pet_views

urlpatterns = [
    path('<int:userid>/pets', pet_views.PetListView.as_view(), name='pet-list'),
    path('<int:userid>/pets/add', pet_views.PetCreateView.as_view(), name='pet-add'),
    path('<int:userid>/pets/<int:pk>', pet_views.PetDetailView.as_view(), name='pet-detail'),
    path('<int:userid>/pets/<int:pk>/update', pet_views.PetUpdateView.as_view(), name='pet-update'),
    path('ajax/ajax-search-species', pet_views.SpeciesSearchTemplateView.as_view(), name='ajax-search-species'),
]
