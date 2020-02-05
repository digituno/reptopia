from django.urls import path, include
from django.conf.urls import url
from . import views as account_views

urlpatterns = [
    path('account/signup/', account_views.SignupView.as_view(), name='signup'),
    path('account/signup/done/', account_views.SignupDoneView.as_view(), name='signup_done'),
    url(r'^activate/(?P<uid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', account_views.UserActivateView.as_view(), name='user_activate'),
]
