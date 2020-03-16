from django.urls import path, include
from . import views as bbs_views

urlpatterns = [
    path('bbs/<bbs_type>/list', bbs_views.PostListView.as_view(), name='board-list'),
    path('bbs/<bbs_type>/add', bbs_views.PostCreateView.as_view(), name='board-add'),
    path('bbs/<bbs_type>/<int:pk>/', bbs_views.PostDetailView.as_view(), name='board-detail'),
    path('bbs/<bbs_type>/<int:pk>/delete', bbs_views.PostDeleteView.as_view(), name='board-delete'),
    path('bbs/<bbs_type>/<int:pk>/update', bbs_views.PostUpdateView.as_view(), name='board-update'),
]
