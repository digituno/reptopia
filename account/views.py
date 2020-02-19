from django.views.generic.edit import CreateView
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from .forms import AccountCreationForm
from django.http import HttpResponse
from .models import Account
from dict.models import AnimalDictionary
import logging
import json

logger = logging.getLogger('reptopia.log')

class SignupView(CreateView):
    template_name = 'account/signup.html.j2'
    form_class = AccountCreationForm
    success_url = reverse_lazy('signup_done')

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False

        user.save()

        current_site = get_current_site(self.request)
        subject = (('Welcome To %s! Confirm Your Email') % current_site.name)
        message = render_to_string('account/user_activate_email.html.j2', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': PasswordResetTokenGenerator().make_token(user),
        })
        email = EmailMessage(subject, message, to=[user.email])
        email.send()

        return redirect('signup_done')


class SignupDoneView(TemplateView):
    template_name = 'account/signup_done.html.j2'


class UserActivateView(TemplateView):
    # logger = logging.getLogger(__name__)
    template_name = 'account/user_activate_complete.html.j2'

    def get(self, request, *args, **kwargs):
        # self.logger.debug('UserActivateView.get()')

        uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
        token = self.kwargs['token']

        # self.logger.debug('uid: %s, token: %s' % (uid, token))

        try:
            user = Account.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            # self.logger.warning('User %s not found' % uid)
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            # self.logger.info('User %s(pk=%s) has been activated.' % (user, user.pk))

        return super(UserActivateView, self).get(request, *args, **kwargs)


class EmailCheckTemplateView(View):
    def get(self, request):
        email = Account.objects.filter(email=request.GET.get('item'))
        return HttpResponse(not email.exists())
