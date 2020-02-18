from django.forms import ModelForm, HiddenInput
from .models import Pet, Care, CareWeight
# from home.models import Dictionary
# import reptopia


class PetCreateForm(ModelForm):
    class Meta:
        model = Pet
        fields = ('species', 'name', 'gender', 'bod', 'desc', 'image')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['species'].widget.attrs.update({'style': 'visibility:hidden; width:0px; height:0px;'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['bod'].widget.attrs.update({'class': 'form-control datepicker', 'readonly': 'true'})
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
        fields = ('date', 'pet', 'type', 'desc', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control datepicker', 'readonly': 'true'})
        self.fields['pet'].widget.attrs.update({'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['desc'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class CareWeightCreateForm(ModelForm):
    class Meta:
        model = CareWeight
        fields = ('date', 'pet', 'type', 'weight', 'desc', 'image')
