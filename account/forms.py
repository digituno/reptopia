from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from django import forms
from .models import Account


class AccountCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ("name", "email", "password1", "password2", "bio", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control '})
        self.fields['password1'].help_text = '비밀번호는 숫자와 문자를 이용한 최소 8자 이상이어야 합니다.'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

        self.fields['name'].label = "이름"
        self.fields['bio'].label = "소개"
        self.fields['image'].label = "대표사진"
        # self.fields['is_public'].label = "공개여부"

        # self.fields['is_public'].help_text = "공개여부를 체크하시면 다른 사육자에게 해당 펫 및 사육일지가 공개됩니다."
