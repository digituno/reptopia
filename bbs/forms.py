from django import forms
from .models import Post, Notice
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


class NoticeCreateForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'content', 'notice_from_date', 'notice_to_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['notice_from_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['notice_to_date'].widget.attrs.update({'class': 'form-control'})

        self.fields['title'].label = "제목"
        self.fields['content'].label = "내용"
