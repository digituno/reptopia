from django.urls import path, include
from . import views as account_views

urlpatterns = [
    path('account/signup/', account_views.SignupView.as_view(), name='signup'),
    path('account/signup/done/', account_views.SignupDoneView.as_view(), name='signup_done'),
]
