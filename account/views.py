from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

class SignupView(CreateView):
    template_name = 'account/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('create_user_done')


class SignupDoneView(TemplateView): # 회원가입이 완료된 경우
    template_name = 'account/signup_done.html'
