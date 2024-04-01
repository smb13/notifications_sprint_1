from django import forms
from django.contrib import admin

from django_ace import AceWidget
from mailings.admin.task import MailingTaskAdminInline
from mailings.models import MailingTemplate


class MailingTemplateForm(forms.ModelForm):
    source_code = forms.CharField(widget=AceWidget(mode="html", theme="chrome"))

    class Meta:
        model = MailingTemplate
        fields = ("name", "source_code")


@admin.register(MailingTemplate)
class MailingTemplateAdmin(admin.ModelAdmin):
    """Mailing template admin."""

    list_display = ("id", "name")
    inlines = (MailingTaskAdminInline,)
    form = MailingTemplateForm
