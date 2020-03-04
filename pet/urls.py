from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views as pet_views

urlpatterns = [
    path('<int:userid>/pets', pet_views.PetListView.as_view(), name='pet-list'),
    path('<int:userid>/pet/add', pet_views.PetCreateView.as_view(), name='pet-add'),
    path('<int:userid>/pet/<int:pk>', pet_views.PetDetailView.as_view(), name='pet-detail'),
    path('<int:userid>/pet/<int:pk>/update', pet_views.PetUpdateView.as_view(), name='pet-update'),
    path('<int:userid>/pet/<int:pk>/delete', pet_views.PetDeleteView.as_view(), name='pet-delete'),
    path('<int:userid>/pet/<int:petid>/care/add', pet_views.CareCreateView.as_view(), name='care-add'),
    path('<int:userid>/pet/<int:petid>/care/<int:careid>/delete', pet_views.CareDeleteView.as_view(), name='care-delete'),
    path('ajax/ajax-search-species', pet_views.SpeciesSearchTemplateView.as_view(), name='ajax-search-species'),
]
