from django.urls import path
from django.views.generic import TemplateView
from . import views as home_views

urlpatterns = [
    path('', home_views.IndexView.as_view(), name='index'),
    path('cards/users', home_views.UserCardSearchView.as_view(), name='card-user'),
    path('cards/pets', home_views.PetCardSearchView.as_view(), name='card-pet'),
    path('cards/cares', home_views.CareCardSearchView.as_view(), name='card-care'),
    # path('tag-autocomplete', home_views.TagAutocomplete.as_view(), name='tag-autocomplete'),
]
