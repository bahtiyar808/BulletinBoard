from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Announcement, News, Response

admin.site.register(News)
admin.site.register(Response)


class AnnouncementAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Announcement
        fields = '__all__'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    form = AnnouncementAdminForm
