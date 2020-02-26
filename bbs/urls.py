from django.urls import path, include

from . import views as bbs_views


urlpatterns = [
    path('post/', bbs_views.PostListView.as_view(), name='post-list'),
    path('post/add/', bbs_views.PostCreateView.as_view(), name='post-add'),
    path('post/<int:pk>/', bbs_views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/delete', bbs_views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update', bbs_views.PostUpdateView.as_view(), name='post-update'),
    path('notice/', bbs_views.PostListView.as_view(template_name='bbs/notice_list.html.j2'), name='notice-list'),
    path('notice/add/', bbs_views.NoticeCreateView.as_view(), name='notice-add'),
    path('notice/<int:pk>/', bbs_views.NoticeDetailView.as_view(), name='notice-detail'),
    path('notice/<int:pk>/delete', bbs_views.NoticeDeleteView.as_view(), name='notice-delete'),
    path('notice/<int:pk>/update', bbs_views.NoticeUpdateView.as_view(), name='notice-update'),
]
