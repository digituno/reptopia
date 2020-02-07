from django.urls import path, include
from django.conf.urls import url
from . import views as account_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', account_views.SignupView.as_view(), name='signup'),
    path('signup/done/', account_views.SignupDoneView.as_view(), name='signup_done'),
    path('activate/<uidb64>/<token>/', account_views.UserActivateView.as_view(), name='user_activate'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html.j2'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(email_template_name='account/password_reset_email.html.j2'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html.j2'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html.j2'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html.j2'), name='password_reset_complete'),
]
