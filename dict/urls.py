from django.urls import path
from . import views as dict_views

urlpatterns = [
    path('ajax/ajax-dict-item-list', dict_views.DictionaryItemTemplateView.as_view(), name='ajax-dict-item-list'),
]

