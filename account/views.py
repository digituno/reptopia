from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .forms import AccountCreationForm

class SignupView(CreateView):
    template_name = 'account/signup.html.j2'
    form_class = AccountCreationForm
    success_url = reverse_lazy('signup_done')


class SignupDoneView(TemplateView):
    template_name = 'account/signup_done.html.j2'
