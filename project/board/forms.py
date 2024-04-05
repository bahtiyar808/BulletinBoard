from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError

from .models import Announcement, Response, News


class AnnouncementForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Announcement
        fields = ['heading', 'text', 'choice']

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get('heading')
        text = cleaned_data.get('text')
        if heading == text:
            raise ValidationError('Текст объявления не должен быть идентичен заголовку')
        return cleaned_data


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['heading', 'text']
