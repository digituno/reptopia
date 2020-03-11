from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from django import forms
from .models import Account


class AccountCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ("name", "email", "password1", "password2", "bio", "blog_url", "instagram_url", "facebook_url", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control '})
        self.fields['password1'].help_text = '비밀번호는 숫자와 문자를 이용한 최소 8자 이상이어야 합니다.'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

        self.fields['name'].label = "사용자명"
        self.fields['bio'].label = "소개"
        self.fields['image'].label = "대표사진"
        self.fields['blog_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['instagram_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['facebook_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['blog_url'].label = "블로그주소"
        self.fields['instagram_url'].label = "인스타그램주소"
        self.fields['facebook_url'].label = "페이스북주소"


class AccountChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = Account
        fields = ("email", "name", "bio", "blog_url", "instagram_url", "facebook_url", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'readonly': True})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['blog_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['instagram_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['facebook_url'].widget.attrs.update({'class': 'form-control'})



        self.fields['name'].label = "이름(별명)"
        self.fields['bio'].label = "소개"
        self.fields['image'].label = "대표사진"
        self.fields['blog_url'].label = "블로그주소"
        self.fields['instagram_url'].label = "인스타그램주소"
        self.fields['facebook_url'].label = "페이스북주소"
