from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})

        self.fields['title'].label = "제목"
        self.fields['content'].label = "내용"
