from django.urls import path, include

from . import views as bbs_views


urlpatterns = [
    path('post/', bbs_views.PostListView.as_view(), name='post-list'),
    path('post/add/', bbs_views.PostCreateView.as_view(), name='post-add'),
    path('post/<int:pk>/', bbs_views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/delete', bbs_views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update', bbs_views.PostUpdateView.as_view(), name='post-update'),
]
