from django.conf.urls import url
from django.contrib.auth.decorators import login_required
 
from . import views
from .models import Like
from account.models import Account
 
app_name = 'ajax'
urlpatterns = [
    url(r'^article/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Account, like_type=Like._LIKE_)),
        name='account_like'),
    url(r'^article/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Account, like_type=Like._DISLIKE_)),
        name='account_dislike'),
]
