from django import forms
from dal import autocomplete
from .models import Photo


class PhotoCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'title', 'desc', 'tags')
        widgets = {
            'tags': autocomplete.TagSelect2(url='tag-autocomplete', attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['desc'].widget.attrs.update({'class': 'form-control'})
        # self.fields['tags'].widget.attrs.update({'class': 'form-control'})

        self.fields['image'].label = "사진"
        self.fields['title'].label = "제목"
        self.fields['desc'].label = "내용"
        # self.fields['tags'].label = "태그"
