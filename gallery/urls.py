from django.urls import path

from . import views as gallery_views


urlpatterns = [
    path('', gallery_views.PhotoListView.as_view(), name='photo-list'),
    path('add/', gallery_views.PhotoCreateView.as_view(), name='photo-add'),
    path('<int:pk>/delete', gallery_views.PhotoDeleteView.as_view(), name='photo-delete'),
]
