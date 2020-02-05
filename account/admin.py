from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import AccountCreationForm
from .models import Account


class AccountAdmin(UserAdmin):
    model = Account
    add_form = AccountCreationForm
    # form = AccountChangeForm
    ordering = ('email',)

admin.site.register(Account, AccountAdmin)
