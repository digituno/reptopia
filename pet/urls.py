from django.urls import path, include
from . import views as pet_views

urlpatterns = [
    path('<username>/', pet_views.PetListView.as_view(), name='pet-list'),
    # path('<username>/pet/add', views.PetCreateView.as_view(), name='pet-add'),
]
