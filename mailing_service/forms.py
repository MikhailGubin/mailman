from django import forms

from mailing_service.models import Client, Mailing, Message
from mixin_form import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = "__all__"


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ("finished_at",)
