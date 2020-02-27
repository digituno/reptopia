from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views as like_views
from .models import Like
from account.models import Account

app_name = 'ajax'
urlpatterns = [
    path('like/account/<int:pk>', login_required(like_views.LikesView.as_view(model=Account, like_type=Like._LIKE_)), name='account-like'),
    path('dislike/account/<int:pk>', login_required(like_views.LikesView.as_view(model=Account, like_type=Like._DISLIKE_)), name='account-dislike'),
]
