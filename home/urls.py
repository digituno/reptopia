from django.urls import path
from django.views.generic import TemplateView
from . import views as home_views

urlpatterns = [
    path('', home_views.IndexView.as_view(), name='index'),
    path('tag-autocomplete', home_views.TagAutocomplete.as_view(), name='tag-autocomplete'),
]
