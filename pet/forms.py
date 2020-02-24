from django import forms
from django.forms import ModelForm, HiddenInput
from django.shortcuts import get_object_or_404
from dict.models import Dictionary, AnimalDictionary
from .models import Pet, Care, Feeding
import logging

logger = logging.getLogger('reptopia.log')


class PetCreateForm(ModelForm):
    class Meta:
        model = Pet
        fields = ('species', 'name', 'gender', 'bod', 'desc', 'image')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['species'].widget.attrs.update({'style': 'visibility:hidden; width:0px; height:0px;'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['bod'].widget.attrs.update({'class': 'form-control', 'readonly': 'true'})
        self.fields['desc'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

        self.fields['species'].label = "개체종류"
        self.fields['name'].label = "펫 이름"
        self.fields['gender'].label = "성별"
        self.fields['bod'].label = "출생년월일"
        self.fields['image'].label = "대표사진"
        self.fields['desc'].label = "펫 설명"

class CareCreateForm(ModelForm):
    class Meta:
        model = Care
        fields = ('date', 'pet', 'type', 'weight', 'desc', 'image')

    weight = forms.IntegerField(required=False)
    prey_type = forms.ModelChoiceField(queryset=Dictionary.objects.all(), required=False)
    prey_size = forms.ModelChoiceField(queryset=Dictionary.objects.all(), required=False)
    prey_weight = forms.IntegerField(required=False)
    prey_quantity = forms.IntegerField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'readonly': 'true'})
        self.fields['pet'].widget.attrs.update({'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['desc'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

        self.fields['prey_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['prey_size'].widget.attrs.update({'class': 'form-control', 'disabled': True})
        self.fields['prey_weight'].widget.attrs.update({'class': 'form-control', 'placeholder': '그램(gram) 단위로 숫자만 입력해주세요.'})
        self.fields['prey_quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': '먹이 수량을 숫자로 입력해주세요.'})

    def clean(self):
        cleaned_data = super(CareCreateForm, self).clean()

        type = cleaned_data.get("type").id
        weight = cleaned_data.get("weight")
        prey_type = cleaned_data.get("prey_type")
        prey_size = cleaned_data.get("prey_size")
        prey_weight = cleaned_data.get("prey_weight")
        prey_quantity = cleaned_data.get("prey_quantity")

        if type == 6 and weight is None:
            self.add_error('weight', "체중은 필수 입력 항목입니다.")
            raise forms.ValidationError("체육 사육일지에 필수 항목이 누락되었습니다.")
        elif type == 2:
            if prey_type is None:
                self.add_error('prey_type', "먹이 유형이 선택되지 않았습니다.")
            if prey_size is None:
                self.add_error('prey_type', "먹이의 크기가 선택되지 않았습니다.")
            if prey_quantity is None:
                self.add_error('prey_type', "먹이 수량은 필수 입력 항목입니다.")
            raise forms.ValidationError("먹이주기 사육일지에 필수 항목이 누락되었습니다.")

        return cleaned_data
